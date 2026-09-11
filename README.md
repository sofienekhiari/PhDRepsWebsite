# PhD Representatives, Pharmazentrum

The website of the PhD Representatives of the Department of Pharmaceutical Sciences
at the University of Basel. It replaces the pages the reps have been keeping on the
old Biozentrum WordPress site.

The site is a single self-contained page. It carries who the representatives are,
what they organise (the Science Lunch, the Lunch Lottery, the Pharm Apéro, the
retreat, the career lecture series and the rest), a news index, the resources a
doctoral student tends to need, and the merchandise order.

## Status

Draft. The page was designed in Claude Design and imported here, so several links
are still placeholders and the photographs have not been added. Nothing has been
signed off by the committee.

## How it is published

GitHub Pages serves the `docs/` folder on the default branch, so `docs/index.html`
is the live page and everything beside it is what the browser loads. There is no
build step and no framework to install: the three files in `docs/` are the whole
site.

## Running it locally

The page fetches its own source at load time, so opening the file directly with
`file://` will not work. Serve the folder instead:

```
python3 -m http.server 8610 --directory docs
```

Then open <http://127.0.0.1:8610/>. An internet connection is needed, because the
page pulls React and Babel from a CDN when it starts.

## Layout

```
docs/            the website, and the only thing GitHub Pages publishes
  index.html     the whole site: markup, styles and data in one file
  support.js     the Claude Design runtime that compiles the page
  image-slot.js  the drop-an-image-here placeholder component
decisions/       the decision record for this project
CLAUDE.md        working notes for whoever picks this up next, human or model
```

## Licence

Not settled yet.
