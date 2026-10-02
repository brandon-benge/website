"""Exercise release boundaries using real temporary Git checkouts."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.build_site import build_site, read_pin


class BuildSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "company"
        self.source = Path(self.temp.name) / "website"
        self.root.mkdir()
        self.source.mkdir()
        for name in ("CNAME", ".nojekyll", "favicon.svg", "og.png", "robots.txt", "sitemap.xml", "index.html", "styles.css"):
            (self.root / name).write_text("company-" + name)
        for name in ("assets", "projects", "how-i-operate", "makeitours", ".git"):
            (self.root / name).mkdir()
            (self.root / name / "example.txt").write_text(name)
        (self.root / "README.md").write_text("private development notes")
        for name in ("index.html", "styles.css", "install-mac.sh", ".nojekyll", "AGENTS.md", "README.md"):
            (self.source / name).write_text("website-" + name)
        for name in ("assets", "MakeItOurs-AppIcon", "__pycache__"):
            (self.source / name).mkdir()
            (self.source / name / "example.txt").write_text(name)
        (self.source / "MakeItOurs-AppIcon/__pycache__").mkdir()
        (self.source / "MakeItOurs-AppIcon/__pycache__/cache.pyc").write_bytes(b"cache")
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=contact@bengesoftwarellc.com", "commit", "-qm", "fixture")
        self.pin = {"makeitours": {"repository": "brandon-benge/makeitours-website", "ref": self.git("rev-parse", "HEAD")}}
        self.write_pin()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.source), *args], text=True).strip()

    def write_pin(self):
        (self.root / "site-sources.json").write_text(json.dumps(self.pin))

    def test_release_preserves_paths_and_excludes_workspace_and_metadata(self):
        output = build_site(self.root, self.source)
        self.assertEqual((output / "index.html").read_text(), "company-index.html")
        self.assertEqual((output / "makeitours-website/index.html").read_text(), "website-index.html")
        self.assertTrue((output / "makeitours-website/install-mac.sh").is_file())
        self.assertTrue((output / "makeitours-website/MakeItOurs-AppIcon/example.txt").is_file())
        self.assertEqual((output / "CNAME").read_bytes(), (self.root / "CNAME").read_bytes())
        self.assertTrue((output / ".nojekyll").exists())
        for name in ("makeitours", ".git", "README.md", "site-sources.json", "makeitours-website/AGENTS.md", "makeitours-website/README.md", "makeitours-website/MakeItOurs-AppIcon/__pycache__"):
            self.assertFalse((output / name).exists(), name)

    def test_missing_source_fails(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            build_site(self.root, self.source / "missing")

    def test_wrong_revision_fails(self):
        self.pin["makeitours"]["ref"] = "0" * 40
        self.write_pin()
        with self.assertRaisesRegex(ValueError, "does not match"):
            build_site(self.root, self.source)

    def test_dirty_release_fails_but_preview_uses_edits(self):
        (self.source / "index.html").write_text("edited")
        with self.assertRaisesRegex(ValueError, "dirty"):
            build_site(self.root, self.source)
        output = build_site(self.root, self.source, release=False)
        self.assertEqual((output / "makeitours-website/index.html").read_text(), "edited")

    def test_untracked_content_fails_release(self):
        (self.source / "draft.html").write_text("uncommitted")
        with self.assertRaisesRegex(ValueError, "dirty"):
            build_site(self.root, self.source)

    def test_ignored_drafts_are_excluded_from_release_but_available_in_preview(self):
        (self.source / ".git/info/exclude").write_text("draft.html\n")
        for name in ("draft.html", "assets/draft.html"):
            (self.source / name).write_text("private draft")
        self.assertEqual(self.git("status", "--porcelain"), "")
        output = build_site(self.root, self.source)
        for name in ("draft.html", "assets/draft.html"):
            self.assertFalse((output / "makeitours-website" / name).exists())
        output = build_site(self.root, self.source, release=False)
        self.assertTrue((output / "makeitours-website/assets/draft.html").exists())

    def test_mutable_ref_and_output_injection_rejected(self):
        for value in ("main", "abcd", "a" * 40 + "\nextra=value"):
            self.pin["makeitours"]["ref"] = value
            self.write_pin()
            with self.assertRaises(ValueError):
                read_pin(self.root)

    def test_source_symlink_fails_without_replacing_previous_artifact(self):
        output = build_site(self.root, self.source)
        (self.source / "assets/leak").symlink_to(self.root / "README.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            build_site(self.root, self.source, release=False)
        self.assertEqual((output / "makeitours-website/index.html").read_text(), "website-index.html")

    def test_output_symlink_fails_without_touching_target(self):
        (self.root / "_site").symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            build_site(self.root, self.source)
        self.assertTrue((self.source / "index.html").exists())

    def test_source_checkout_symlink_fails(self):
        alias = self.root / "website-link"
        alias.symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            build_site(self.root, alias)

    def test_rebuild_removes_stale_output(self):
        output = build_site(self.root, self.source)
        (output / "stale.html").write_text("old")
        build_site(self.root, self.source)
        self.assertFalse((output / "stale.html").exists())


if __name__ == "__main__":
    unittest.main()
