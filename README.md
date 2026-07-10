# Personal website for Matt Baughman

[![Deploy](https://github.com/mattebaughman/mattebaughman.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/mattebaughman/mattebaughman.github.io/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mattebaughman/mattebaughman.github.io/main.svg)](https://results.pre-commit.ci/latest/github/mattebaughman/mattebaughman.github.io/main)

Static files and code for generating my personal website at [mattebaughman.com](https://mattebaughman.com).
The page design is based on [ericswallace.com](https://www.ericswallace.com/), and the static site compilation is done in Python using Jinja.

## Structure

| Directory    | Description |
| ------------ | ----------- |
| `builder/`   | Python package that compiles the static site with Jinja.      |
| `config/`    | Data files for generating various sections of the site.       |
| `static/`    | Static files to include in the site (CSS, files, images).     |
| `templates/` | HTML Jinja templates compiled to produce final rendered site. |

## Build Locally

```bash
$ virtualenv venv
$ . venv/bin/activate
$ pip install -e .
$ python -m builder --open
```

The output is written to `_site/` by default, and `_site/index.html` can be opened in your browser to view.
The `--open` flag will automatically open the page after the build completes if your terminal is configured to open links.

The build and content are configured in the `config/config.toml` file.
See `python -m builder --help` for more details.

## Updating

To add a new publication:
1. Add the BibTeX entry to `static/publications/baughman.bib`.
2. Create a new JSON file for the publication in `config/publications/` and fill out all of the fields
   (see `config/publications/README.md`; the `bibtex` field must match the entry ID in `baughman.bib`,
   and `category` must be one of the keys in `[publications.categories]` in `config/config.toml`).
3. Optionally add the paper PDF to `static/publications/` and point the JSON's `paper` field at it.

To add a new presentation:
1. Add the slides PDF to `static/slides/` (or a poster to `static/posters/`, creating that directory if needed).
2. Create a new JSON file for the presentation in `config/presentations/` and fill out all of the fields.

Projects are edited inline in `config/config.toml` under `[projects].links`
(each entry needs `name`, `link`, and `description`).

## Deploying

The website is built and deployed from HEAD weekly and on each push to `main`.

## Fixing BibTeX

The `builder` package also includes a CLI utility for formatting BibTeX files.
The formatter will do many things: sort by entry IDs, sort keys within entries, clean up indents, use uniform formatting, fix casing in titles, and more.

The `builder` package must first be installed in your Python environment if not already.
```bash
$ virtualenv venv
$ . venv/bin/activate
$ pip install .
```

To format:
```bash
$ python -m builder.publications --input INPUT_BIB_FILE --output OUTPUT_BIB_FILE
```
Use `python -m builder.publications --help` for additional options.
