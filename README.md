# Benge Software LLC Website

Static company website for [bengesoftwarellc.com](https://bengesoftwarellc.com),
hosted with GitHub Pages. Python 3 and Git assemble the publication artifact;
there are no third-party build dependencies.

## Repository layout

The MakeItOurs website has its own public repository:
[brandon-benge/makeitours-website](https://github.com/brandon-benge/makeitours-website).
Its development checkout is the `makeitours/makeitours-website/` submodule inside
the private product workspace. Its published URL remains `/makeitours-website/`.
`site-sources.json` pins the exact website commit released by this company repo.

## Local preview

If you have product workspace access, initialize only the required submodules:

```sh
git submodule update --init makeitours
git -C makeitours submodule update --init makeitours-website
python3 scripts/build_site.py --preview --serve --open-browser
```

The existing VS Code **Preview Benge Software website** task runs this preview
and also allows home-network access on port 8000. The command above binds to
loopback. Stop with Ctrl-C. Restart after edits to rebuild the preview snapshot.
Preview includes local website edits, without enforcing the published SHA.

Without private workspace access, clone only the public website:

```sh
git clone https://github.com/brandon-benge/makeitours-website.git .site-source/makeitours-website
python3 scripts/build_site.py --source .site-source/makeitours-website --preview --serve
```

Serve the generated `_site/` directory; serving the source root directly no longer
provides the complete URL layout. No symlink or duplicate source folder is needed.

## Publishing and rollback

GitHub Pages uses `.github/workflows/deploy-pages.yml`, triggered on pushes to
`main` or manually. Keep the Pages publishing source set to **GitHub Actions**.
The workflow checks out the public website directly at the manifest SHA, builds
`_site/`, and uploads only that directory. It never clones the private workspace.
The assembled root includes `CNAME` and `.nojekyll`; the domain and relative links
are unchanged. The script explicitly selects public content and omits repository
metadata, private workspace files and caches.

To release a website change:

1. Commit and push the website changes to its independent repository.
2. Change `makeitours.ref` in `site-sources.json` to the full 40-character commit
   SHA. Ensure the local source checkout is at that revision and clean.
3. Verify with the commands below and review the assembled site.
4. Commit and merge the central change to `main` to deploy through Pages.

```sh
python3 -m unittest discover -s tests -p 'test_build_site.py'
python3 scripts/build_site.py
```

Use `--source .site-source/makeitours-website` for a standalone public checkout.
Release builds reject a missing source, wrong SHA or dirty website checkout.
Only tracked website files enter release artifacts; ignored local drafts are excluded.
Revert the manifest SHA to roll back. A source push or workspace submodule update
alone does not publish; the central manifest is the release authority. Record the
workspace submodule update separately when advancing its development checkout.

The assembly and preview commands also include company-site working edits.
CI takes those files from its checked-out central commit.
