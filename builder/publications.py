from __future__ import annotations

import argparse
import calendar
import glob
import json
import os
import sys
from collections import defaultdict
from collections.abc import Sequence
from typing import NamedTuple

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter


class Publication(NamedTuple):
    title: str
    authors: str
    venue: str
    tldr: str
    awards: str | None
    paper: str
    bibtex_id: str
    bibtex: str
    year: int
    month: int
    date_str: str
    category: str
    code: str | None = None
    website: str | None = None
    poster: str | None = None
    slides: str | None = None
    preprint: str | None = None
    publisher: str | None = None
    selected: bool = False


def get_bibtex_writer() -> BibTexWriter:
    bib_writer = BibTexWriter()
    bib_writer.indent = "    "
    bib_writer.order_entries_by = ("ID",)
    bib_writer.display_order = ["title", "author"]
    return bib_writer


def parse_publication_json(pub_file: str) -> Publication:
    with open(pub_file) as f:
        attrs = json.load(f)

    required = (
        "title",
        "authors",
        "venue",
        "tldr",
        "bibtex",
        "year",
        "month",
        "category",
    )
    missing = [key for key in required if attrs.get(key) is None]
    if missing:
        raise ValueError(
            f"Publication file {pub_file} is missing required "
            f"field(s): {', '.join(missing)}.",
        )

    if not isinstance(attrs["month"], int) or not 1 <= attrs["month"] <= 12:
        raise ValueError(
            f"Publication file {pub_file} has invalid month "
            f"{attrs['month']!r}; expected an integer from 1 to 12.",
        )

    if isinstance(attrs["authors"], list):
        authors = ", ".join(attrs["authors"])
    elif isinstance(attrs["authors"], str):
        authors = attrs["authors"]
    else:
        raise ValueError(f"Unable to parse authors field of {pub_file}.")

    attrs = defaultdict(lambda: None, attrs)

    return Publication(
        title=attrs["title"],
        authors=authors,
        venue=attrs["venue"],
        tldr=attrs["tldr"],
        awards=attrs["awards"],
        paper=attrs["paper"],
        bibtex_id=attrs["bibtex"],
        bibtex="",
        code=attrs["code"] if "code" in attrs else None,
        website=attrs["website"] if "website" in attrs else None,
        poster=attrs["poster"] if "poster" in attrs else None,
        slides=attrs["slides"] if "slides" in attrs else None,
        publisher=attrs["publisher"] if "publisher" in attrs else None,
        preprint=attrs["preprint"] if "preprint" in attrs else None,
        year=attrs["year"],
        month=attrs["month"],
        date_str=f"{calendar.month_abbr[attrs['month']]} {attrs['year']}",
        selected=attrs["selected"] if "selected" in attrs else False,
        category=attrs["category"],
    )


def load_bibtex(bib_file: str) -> BibDatabase:
    parser = BibTexParser()

    with open(bib_file) as bf:
        bibs = bibtexparser.load(bf, parser)

    return bibs


def load_publications(
    pub_dir: str,
    bib_file: str,
    categories: Sequence[str] | None = None,
) -> list[Publication]:
    bibs = load_bibtex(bib_file).entries_dict
    bib_writer = get_bibtex_writer()

    pubs: list[Publication] = []
    for pub_name in glob.glob("*.json", root_dir=pub_dir):
        pub_file = os.path.join(pub_dir, pub_name)
        pub = parse_publication_json(pub_file)

        if pub.bibtex_id not in bibs:
            raise ValueError(
                f"Publication file {pub_file} references BibTeX entry "
                f"'{pub.bibtex_id}' which does not exist in {bib_file}.",
            )
        if categories and pub.category not in categories:
            raise ValueError(
                f"Publication file {pub_file} has category "
                f"'{pub.category}' which is not one of the configured "
                f"categories: {', '.join(categories)}.",
            )
        bib = bibs[pub.bibtex_id]

        temp_database = BibDatabase()
        temp_database.entries = [bib]
        bib_str = bib_writer.write(temp_database)

        pubs.append(pub._replace(bibtex=bib_str))

    pubs.sort(key=lambda x: (x.year, x.month), reverse=True)

    return pubs


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="BibTeX Parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="python -m builder.publications",
    )
    parser.add_argument(
        "--input",
        help="BibTeX file to format",
    )
    parser.add_argument(
        "--output",
        help="Path to output file",
    )
    parser.add_argument(
        "--indent",
        default="    ",
        help="indent format",
    )

    args = parser.parse_args(argv)

    print(f"loading file at {args.input}")
    bibs = load_bibtex(args.input)
    bib_writer = get_bibtex_writer()
    bib_writer.indent = args.indent

    with open(args.output, "w") as f:
        f.write(bib_writer.write(bibs))

    print(f"wrote formatted bib to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
