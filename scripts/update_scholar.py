from __future__ import annotations

import html
import os
import re
import sys
import textwrap
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scholarly import scholarly


ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS_FILE = ROOT / "publications.html"
START_MARKER = "<!-- AUTO-GENERATED:START -->"
END_MARKER = "<!-- AUTO-GENERATED:END -->"


@dataclass(frozen=True)
class Publication:
    title: str
    authors: str
    venue: str
    year: int | None


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set.")
    return value


def parse_year(raw_year: Any) -> int | None:
    if raw_year is None:
        return None
    match = re.search(r"\d{4}", str(raw_year))
    return int(match.group(0)) if match else None


def first_non_empty(*values: Any) -> str:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return "Venue unavailable"


def fetch_publications(scholar_id: str) -> list[Publication]:
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["publications"])

    publications: list[Publication] = []
    for raw_publication in author.get("publications", []):
        publication = scholarly.fill(raw_publication)
        bib = publication.get("bib", {})
        title = first_non_empty(bib.get("title"), "Untitled publication")
        authors = first_non_empty(bib.get("author"), "Authors unavailable").replace(" and ", ", ")
        venue = first_non_empty(
            bib.get("journal"),
            bib.get("conference"),
            bib.get("booktitle"),
            bib.get("citation"),
            bib.get("publisher"),
            bib.get("venue"),
        )
        publications.append(
            Publication(
                title=title,
                authors=authors,
                venue=venue,
                year=parse_year(bib.get("pub_year")),
            )
        )

    publications.sort(
        key=lambda item: (
            item.year or 0,
            item.title.lower(),
        ),
        reverse=True,
    )
    return publications


def render_publications(publications: list[Publication]) -> str:
    if not publications:
        return textwrap.dedent(
            """
            <div class="publication-empty">
                <p>No publications were returned from Google Scholar for the configured profile.</p>
            </div>
            """
        ).strip()

    groups: "OrderedDict[str, list[Publication]]" = OrderedDict()
    for publication in publications:
        year_label = str(publication.year) if publication.year else "Undated"
        groups.setdefault(year_label, []).append(publication)

    parts: list[str] = []
    for year, items in groups.items():
        parts.append('<section class="publication-year-group">')
        parts.append(f'    <h3 class="publication-year">{html.escape(year)}</h3>')
        parts.append('    <ol class="publication-list">')
        for item in items:
            parts.append('        <li class="publication-item">')
            parts.append(f'            <h4 class="publication-title">{html.escape(item.title)}</h4>')
            parts.append(f'            <p class="publication-authors">{html.escape(item.authors)}</p>')
            parts.append(
                f'            <p class="publication-meta">{html.escape(item.venue)}'
                + (f" · {item.year}" if item.year else "")
                + "</p>"
            )
            parts.append("        </li>")
        parts.append("    </ol>")
        parts.append("</section>")
    return "\n".join(parts)


def update_publications_page(generated_html: str) -> bool:
    content = PUBLICATIONS_FILE.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(?P<start>[ \t]*{re.escape(START_MARKER)}\r?\n)(?P<body>.*?)(?P<end>[ \t]*{re.escape(END_MARKER)})",
        re.DOTALL,
    )

    match = pattern.search(content)
    if not match:
        raise RuntimeError(f"Could not locate auto-generated block in {PUBLICATIONS_FILE}.")

    end_line = match.group("end")
    indent = end_line[: end_line.index(END_MARKER)]
    replacement = match.group("start") + textwrap.indent(generated_html.strip(), indent) + "\n" + end_line
    updated = content[: match.start()] + replacement + content[match.end() :]

    if updated == content:
        return False

    PUBLICATIONS_FILE.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    scholar_id = require_env("SCHOLAR_ID")
    publications = fetch_publications(scholar_id)
    generated_html = render_publications(publications)
    changed = update_publications_page(generated_html)

    if changed:
        print(f"Updated {PUBLICATIONS_FILE.name} with {len(publications)} publications.")
    else:
        print(f"No publication changes detected in {PUBLICATIONS_FILE.name}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - failure path for CLI execution
        print(f"Scholar update failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
