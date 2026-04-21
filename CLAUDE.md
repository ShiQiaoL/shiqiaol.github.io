# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static academic personal website for Xiaoqing Liu (computational materials scientist). No build step, no bundler — plain HTML + CSS served directly.

## Running Locally

```sh
python -m http.server 8000
```

## Updating Publications from Google Scholar

```sh
pip install scholarly
SCHOLAR_ID=<id> python scripts/update_scholar.py
```

On Windows PowerShell: `$env:SCHOLAR_ID = "<id>"` before running.

The script prints either "Updated publications.html with N publications." or "No publication changes detected." On CI, this runs weekly via `.github/workflows/update_scholar.yml` using `SCHOLAR_ID` from GitHub Secrets.

## Architecture

Three HTML pages (`index.html`, `research.html`, `publications.html`) share a single stylesheet (`style.css`) and a consistent header/nav structure.

**Auto-generated content**: In `publications.html`, the block between `<!-- AUTO-GENERATED:START -->` and `<!-- AUTO-GENERATED:END -->` is written exclusively by `scripts/update_scholar.py` (uses the `scholarly` library). Never hand-edit this block — it will be overwritten by the next Scholar sync.

**Profile photo**: Embedded as a base64 data URI in `index.html`. If replacing, keep it inline or move to `assets/` and update `src`.

## Key Conventions

**HTML**: All pages share the same header/nav structure — keep it consistent. Use `aria-current="page"` on the active nav link. Fonts are Google Fonts: Source Sans 3 (body) and Source Serif 4 (headings).

**CSS**: Single file `style.css`, no preprocessor. Design tokens are defined as CSS custom properties in `:root` — always use them (`--bg`, `--paper`, `--text`, `--muted`, `--line`, `--accent`, `--accent-soft`, `--max-width`, `--radius`). Responsive layout uses `clamp()` and `min()` — no media queries for sizing; maintain this pattern.
