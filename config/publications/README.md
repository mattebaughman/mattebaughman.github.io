# Publications

Each file in this directory is JSON with the following fields.
The files will be automatically parsed to generate the static page.

Required fields: `title`, `authors`, `venue`, `bibtex` (must match an entry
ID in `static/publications/baughman.bib`), `year`, `month`, and `category`
(must be one of the keys in `[publications.categories]` in
`config/config.toml`, e.g. `systems`, `ml`, or `science`).

```json
{
    "title": "Paper Title",
    "authors": [
        "Author 1",
        "Author 2"
    ],
    "venue": "FunConf 2022",
    "awards": null,
    "tldr": "Two sentence TLDR.",
    "paper": "publications/*.pdf",
    "bibtex": "bibtex entry name",
    "category": "systems",
    "code": null,
    "website": null,
    "poster": null,
    "slides": null,
    "publisher": null,
    "preprint": null,
    "year": 2020,
    "month": 11,
    "selected": false
}
```
