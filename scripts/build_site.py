#!/usr/bin/env python3
"""Assemble the central Pages artifact or preview the nested website checkout."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
COMPANY_FILES = ("CNAME", ".nojekyll", "favicon.svg", "og.png", "robots.txt", "sitemap.xml")
COMPANY_DIRS = ("assets", "projects", "how-i-operate")
WEBSITE_DIRS = ("assets", "MakeItOurs-AppIcon")


def read_pin(root):
    pin = json.loads((root / "site-sources.json").read_text())["makeitours"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", pin["repository"]):
        raise ValueError("Website repository must be an owner/repository name")
    if not re.fullmatch(r"[0-9a-f]{40}", pin["ref"]):
        raise ValueError("Website ref must be a full lowercase 40-character commit SHA")
    return pin


def git(source, *args):
    return subprocess.check_output(["git", "-C", str(source), *args], text=True).strip()


def copy_public(source, destination, tracked=None):
    if source.is_symlink():
        raise ValueError(f"Public source cannot be a symlink: {source}")
    if source.name in {".git", "__pycache__", ".DS_Store", "AGENTS.md"} or source.suffix == ".pyc":
        return
    if source.is_dir():
        destination.mkdir(parents=True, exist_ok=True)
        for child in sorted(source.iterdir()):
            copy_public(child, destination / child.name, tracked)
    else:
        if tracked is not None and source not in tracked:
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_site(root, source, release=True):
    if Path(source).is_symlink():
        raise ValueError("Website source must not be a symlink")
    root, source = Path(root).resolve(), Path(source).resolve()
    pin = read_pin(root)
    if not (source / "index.html").is_file():
        raise ValueError(f"Website checkout missing at {source}; see README.md setup instructions")
    tracked = None
    if release:
        if Path(git(source, "rev-parse", "--show-toplevel")).resolve() != source:
            raise ValueError("Website source must be an independent Git checkout")
        if git(source, "rev-parse", "HEAD") != pin["ref"]:
            raise ValueError("Website checkout does not match site-sources.json; use --preview for local edits")
        if git(source, "status", "--porcelain", "--untracked-files=all"):
            raise ValueError("Website checkout is dirty; use --preview for local edits")
        names = subprocess.check_output(
            ["git", "-C", str(source), "ls-files", "-z"], text=True
        ).split("\0")
        tracked = {source / name for name in names if name}
    output = root / "_site"
    if output.is_symlink():
        raise ValueError("_site must not be a symlink")
    # Validate and assemble before replacing the previous usable preview.
    with tempfile.TemporaryDirectory(prefix=".site-build-", dir=root) as temporary:
        stage = Path(temporary) / "site"
        stage.mkdir()
        company = list(COMPANY_FILES) + list(COMPANY_DIRS)
        company += [p.name for pattern in ("*.html", "*.css") for p in root.glob(pattern)]
        for name in company:
            copy_public(root / name, stage / name)
        website = [".nojekyll", *WEBSITE_DIRS]
        website += [p.name for pattern in ("*.html", "*.css", "*.sh") for p in source.glob(pattern)]
        for name in website:
            copy_public(source / name, stage / "makeitours-website" / name, tracked)
        if output.exists():
            shutil.rmtree(output)
        stage.rename(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "makeitours/makeitours-website")
    parser.add_argument("--preview", action="store_true", help="Allow local website edits instead of enforcing the release pin")
    parser.add_argument("--serve", action="store_true", help="Serve the assembled snapshot; restart after edits")
    parser.add_argument("--open-browser", action="store_true")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    try:
        output = build_site(ROOT, args.source, release=not args.preview)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Site build failed: {error}\n")
    print(f"Assembled site: {output}", flush=True)
    if args.serve:
        handler = partial(SimpleHTTPRequestHandler, directory=str(output))
        with ThreadingHTTPServer((args.bind, args.port), handler) as server:
            url = f"http://localhost:{server.server_port}/"
            print(f"Preview: {url} (restart after edits)", flush=True)
            if args.open_browser:
                webbrowser.open(url)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
