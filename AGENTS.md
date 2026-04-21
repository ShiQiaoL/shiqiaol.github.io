# Agent Instructions — Xiaoqing Liu Academic Website

## Project Overview

Static academic personal website for Xiaoqing Liu (computational materials scientist). No build step, no bundler — plain HTML + CSS served directly.

## Structure

| Path | Purpose |
|---|---|
| `index.html` | Homepage (bio, contact, links) |
| `research.html` | Research directions |
| `publications.html` | Publication list (partially auto-generated) |
| `style.css` | Single shared stylesheet (CSS custom properties in `:root`) |
| `assets/` | CV files (HTML & PDF) |
| `scripts/update_scholar.py` | Python script that fetches publications from Google Scholar and rewrites a section of `publications.html` |
| `.github/workflows/update_scholar.yml` | GitHub Actions workflow — runs `update_scholar.py` weekly (Saturday) or on manual dispatch |

## Key Conventions

### HTML

- All pages share the same header/nav structure. Keep it consistent across files.
- Navigation uses `aria-current="page"` on the active link.
- Fonts loaded from Google Fonts: **Source Sans 3** (body) and **Source Serif 4** (headings).

### CSS

- Single file `style.css`, no preprocessor.
- Design tokens defined as CSS custom properties in `:root` — always use them (`--bg`, `--paper`, `--text`, `--muted`, `--line`, `--accent`, `--accent-soft`, `--max-width`).
- Responsive layout via `clamp()` and `min()` — no media queries for sizing. Keep this approach.

### Auto-generated Publications

- In `publications.html`, the block between `<!-- AUTO-GENERATED:START -->` and `<!-- AUTO-GENERATED:END -->` is **machine-written**. Do not edit it by hand; changes will be overwritten by the next Scholar sync.
- The generation logic lives in `scripts/update_scholar.py` (uses `scholarly` library).
- The script requires the `SCHOLAR_ID` environment variable (stored as a GitHub secret).

### Images

- The profile photo in `index.html` is embedded as a base64 data URI. If replacing, keep it inline or move to `assets/` and update the `src`.

## Running Locally

Open any `.html` file directly in a browser, or use a simple local server:

```sh
python -m http.server 8000
```

## Running the Scholar Update Script

```sh
pip install scholarly
SCHOLAR_ID=<id> python scripts/update_scholar.py
```
