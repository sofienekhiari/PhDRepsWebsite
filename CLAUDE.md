# PhD Reps Pharmazentrum website

## What this is

The website of the PhD Representatives of the Department of Pharmaceutical Sciences,
University of Basel. Twenty-one elected representatives: three on the board and
eighteen delegates drawn from nine research groups. The site carries who they are,
the events they run (Science Lunch, Lunch Lottery, Pharm Apéro, the retreat, the
career lecture series, the seminar, merchandise), a news index, and the resources a
doctoral student tends to need.

It replaces the pages the reps have been keeping on the Biozentrum WordPress site at
`phdstudents.biozentrum.unibas.ch`, which is where most of the archived content and
several of the outbound links still point.

Sofiene is one of the delegates (Computational Pharmacy, listed with the Website
portfolio), which is why this repository is his.

## Status

Draft, but the content is now real. On 11 September 2026 both live sites were
crawled and everything on this page was rewritten against them, so the people,
the activities, the retreat and the links are what the Pharmazentrum actually
publishes rather than what the design brief guessed. What is still missing is
photographs, a few verified details, and any sign-off from the committee.

Scope: the old site is shared between the Biozentrum and the Pharmazentrum
representatives, and the two are separating. This site carries the Pharmazentrum
and the genuinely joint activities (the Science Lunch, the Lunch Lottery, the
Career Lecture Series, the retreat, the shared social events) and leaves the
Biozentrum's own roster and history behind.

## How it is published

GitHub Pages serves `docs/` on `main`, so `docs/index.html` is the live page.
Remote: `git@github.com:sofienekhiari/PhDRepsWebsite.git`.

There is no build step. The three files in `docs/` are the entire site, and pushing
to `main` is what publishes. Verified on 2026-09-11 that the page renders correctly
when served as a directory index at `/`, which is the shape GitHub Pages will use.

## Layout

```
docs/            the website, and the only thing GitHub Pages publishes
  index.html     the whole site: markup, styles, data and logic in one file
  support.js     the Claude Design runtime (vendored, generated, never hand-edit)
  image-slot.js  the drop-an-image-here placeholder component (vendored)
decisions/       the decision record for this project, one JSON file per set of rulings
README.md        the public-facing description
CLAUDE.md        this file
.claude-no-record  marks the project as non-research, so the end-of-turn record check stays quiet
```

## Local preview

```
python3 -m http.server 8610 --bind 127.0.0.1 --directory docs
```

Then open <http://127.0.0.1:8610/>. Opening `docs/index.html` over `file://` is not
enough: the runtime re-fetches its own source at load, and Chrome blocks that on
`file://`.

An internet connection is required. React and ReactDOM are pulled from unpkg at
boot, so the page is blank without them.

## How the page works

`docs/index.html` is a Claude Design component file. It has three parts:

1. A `<helmet>` block (lines 10 to 45) holding the page title, the Figtree web font,
   and the whole stylesheet, which is a set of CSS custom properties for the
   teal-and-ink palette plus a handful of base rules. Everything else is styled with
   inline `style` attributes on the elements themselves.
2. The template, inside `<x-dc>` (lines 9 to 714). Plain HTML with four extra
   things: `{{ expr }}` interpolation, `<sc-if value="{{ … }}">` for conditionals,
   `<sc-for list="{{ … }}" as="x">` for repeats, and `style-hover="…"` which mints a
   real CSS rule for the hover state that an inline style cannot express.
3. The logic, in `<script type="text/x-dc">` (lines 715 to 1120), a
   `class Component extends DCLogic` holding every dataset as a constant, a small
   hash router, and a `renderVals()` that hands the template its values.

`support.js` finds `<x-dc>`, compiles the template, fetches React 18.3.1 and
ReactDOM 18.3.1 from unpkg (both pinned with subresource integrity), and renders the
result client-side. Nothing is prerendered, so a crawler with JavaScript disabled
sees an empty body.

The `data-props` attribute on the script tag (line 715) is the editor's props panel.
Served standalone, the runtime applies its declared defaults, so the home page uses
the `Event-first` hero and the reps page uses `Portrait cards`. Note that the class
itself falls back to `Statement hero` (line 1044) if that attribute ever goes away,
which would silently switch the home page to a different hero.

### Routes

Hash routing, parsed at lines 975 to 980, re-read on every `hashchange`.

| Hash | Page |
|---|---|
| `#/` | Home |
| `#/events` | Calendar, with Show and Series filters |
| `#/events/<id>` | One event, 14 ids defined in `EVENTS` |
| `#/people` | Board, delegates, and a collapsible alumni list |
| `#/news` | Nine dated entries, all outbound links |
| `#/resources` | Four themed cards plus the confidential routes |
| `#/merch` | The hoodie |

An unrecognised top-level hash renders the navigation bar and nothing else. An
unrecognised event id falls back to the calendar.

### Where the content lives

Every dataset is a constant on the class in `docs/index.html`:

| Constant | Line | Entries | What it is |
|---|---|---|---|
| `PALETTE` | 738 | 7 | avatar colours |
| `SERIES_COLOR` | 740 | 7 | one colour per activity series; the key must match a `series` value exactly |
| `SOURCE_COLOR` | 744 | 3 | news source badges |
| `BOARD` | 749 | 3 | president, secretary, treasurer, with the only three published email addresses |
| `DELEGATES` | 755 | 18 | the assembly, with no address, because none is published |
| `ALUMNI` | 776 | 26 | past representatives |
| `STATS` | 791 | 4 | the figure strip |
| `HERO_LOGOS` | 799 | 5 | the institutes the assembly keeps a contact person for |
| `STANDING` | 803 | 7 | what runs all year, with a `cadence` and no date |
| `EVENTS` | 907 | 8 | only things with a published date |
| `NEWS` | 982 | 7 | the shared site's news feed |
| `RESOURCES` | 992 | 4 | the resource cards |

**`STANDING` versus `EVENTS` is the important distinction.** Almost nothing the
representatives run has a published date: the Science Lunch, the Apéro, the BBQ
and the career talks come round and are announced by email a couple of weeks
ahead. Those live in `STANDING` with a `cadence` string and no date at all, and
`decorateStanding` (line 1061) fills the date-shaped fields with that cadence so
the event page needs no branching. `EVENTS` holds only what was actually
announced on a date, which today is the 2026 retreat and seven archived items.
Do not put a guessed date in `EVENTS` to make something appear in the calendar.

Two things are still derived rather than stored, and both are traps when editing:

- **Board portrait slot ids** are `v4-board-portrait-<array index>` (line 1122),
  so an image follows the position, not the person. Reorder `BOARD` and the
  portraits swap.
- **Board avatar colours** index `PALETTE` without a modulo, so a fourth board
  member would get `undefined`. The delegate version wraps correctly.

The counts in the prose are no longer hardcoded: `repCount`, `boardCount`,
`delegateCount`, `groupCount` and `alumniCount` are computed from the arrays, so
editing the roster updates the copy.

## Known defects

Ranked by how much damage each does if it ships as is. Line numbers are
`docs/index.html`.

1. **Five empty image slots** render their prompt text to visitors: the group
   photo (line 208), three board portraits (line 508) and the hoodie (line 690).
   They cannot be filled by putting a file on the server. `<image-slot>` persists
   a dropped image through `window.omelette.writeFile` into a
   `.image-slots.state.json` sidecar, and that function exists only inside the
   Claude Design host. On a static server the slots are permanently empty and
   read-only, and the component hardcodes `alt=""` with no way to set it.
   Replacing them with plain `<img>` tags and real files is the right move, and
   it is a decision rather than a chore.
2. **Accessibility.** Colour contrast is fixed: the palette replaced in
   September 2026 was measured, and every series ink carries white text at 5:1 or
   better while `--body` and `--muted` clear 4.5:1 on the paper ground. `--faint`
   #868d9c is 3.03:1 and is decorative only. The `lang` attribute is set. What is
   left is structural: section labels are `<span>` rather than headings, so the
   visual hierarchy is invisible to a screen reader, and the three board members
   sit at `<h2>` alongside the section holding the other eighteen; the alumni
   toggle has no `aria-expanded`; and there is no `prefers-reduced-motion` guard
   on the `lift` animation (line 43) or the global smooth scrolling (line 28).
3. **Client-render fragility.** `support.js` hides the template before it fetches
   React. If unpkg is blocked, the visitor gets a blank white page with no
   message; if `support.js` itself fails to load, they get raw markup full of
   literal `{{ leadTitle }}`. There is no `<noscript>`. One static `<title>`, no
   meta description, no Open Graph tags and no favicon, so every shared link
   previews identically, which undercuts a site whose distribution model is
   pasting links into chat.
4. **Narrow-phone overflow, unmeasured.** Four row layouts use fixed grid columns
   with nowrap content. One resize test at 320 px and 390 px would settle it.
5. **CSP.** The runtime uses `new Function`, runtime `insertRule`, and inline
   styles on nearly every element, so any strict Content Security Policy needs
   `unsafe-eval` and `unsafe-inline`. Worth raising before the hosting
   conversation with university IT, not after.

The two console errors on load are benign: a 404 for the image-slot sidecar,
which the component swallows, and a 404 for a favicon that does not exist.

## What the content rests on

Everything on the page now traces to one of two live sites, crawled on
11 September 2026. Where a fact was not published, the page says so rather than
inventing one.

- **The roster** comes from the shared site's Pharmazentrum page, which is headed
  "Spring 2025" over a block headed "Board members 2024". The reps page says so,
  so a stale list does not read as current.
- **Only the board publishes an address** (`diell.aliu@`, `alessandra.cavegn@`,
  `jannes.felsch@`, all `unibas.ch`). The eighteen delegates publish none, so this
  site prints none: the earlier draft generated them from names, which is how
  Natasha Marion Bärenzung's would have been wrong. The two department deputies
  are named without addresses and messages route through the board.
- **The retreat** comes from `phd-retreat.unibas.ch`: the 17th edition, Hotel La
  Palma au Lac, 27 to 29 August 2026, registration open 7 April to 14 May, run
  since 2009 and cancelled only in 2020, more than eighty attendees, every
  participant presents, 1 CP for a successful participation.
- **The activities** keep the live site's own wording for how a person takes
  part, because that is the thing most easily got wrong.
- **The social accounts** are real and taken from the live pages. The LinkedIn
  page is the Pharmazentrum's; Instagram and Bluesky are the shared Biozentrum
  accounts, and the footer says so.
- **Sofiene Khiari holds the Computational Pharmacy seat** with the Website
  portfolio. Roman Aschwanden had it before him, from the same research group,
  and has since graduated, so he moved to the alumni list rather than out of the
  roster. Confirmed by Sofiene on 11 September 2026.

## Open questions, his to rule

- Consent. Twenty-one current representatives are named and twenty-six alumni
  are named, some with roles and several long gone. Is there a university policy,
  and should the three board addresses be replaced by a single alias?
- The roster is dated Spring 2025 and one seat has already turned over since.
  Who is actually on the board and in the assembly now?
- Is the Career Lecture Series still run with the Postdoc Club, and are Dibya
  Saha, Daan Overwijn, Camila Pulido Barrera and Máté Balajti still its contacts?
  The site currently points speaker offers at the first of them.
- The Pharm Apéro, the Summer BBQ and the Seminar in Drug Sciences have almost no
  published content: a name and a portfolio each. Anything you can add is more
  than the live site has.
- Is the hoodie order still open? The live page gives 25 November with no year.
- Architecture. Keeping the Claude Design runtime costs resilience, SEO, link
  previews, CSP compatibility and the ability to fill the image slots. A
  prerendered static build would fix all five and cost the round trip back to the
  design tool. This is the largest fork in the project and it has not been
  decided.

## How Sofiene wants to work on this

Ruled 11 September 2026. There are two channels, and they are for different sizes
of change.

**Comments on the artifact, for a specific edit.** The site is published as a
Claude Artifact at
<https://claude.ai/code/artifact/24c45dd7-a3e3-4097-91df-9bdc24a3e984>. He reads
the page there and comments on the thing he wants changed, which is faster than
describing where it is. A comment only reaches a running session if he sends it
to Claude from the thread; a plain comment sits there silently until someone
reads it with the artifact tool's `comments` action.

**Chat, for a bigger change.** Anything someone else has asked him to do, or a
change that touches the structure rather than the wording, he says here instead.

**What happens on either.** Edit `docs/index.html`, rebuild the artifact,
republish it to the same URL, commit, and push. That is the whole loop and it is
not something to check back about each time: he has asked for it as the standing
routine. Reply on the comment thread saying what changed and resolve it, so the
page shows what was acted on.

```
python3 build-artifact.py        # regenerates artifact/index.html from docs/
```

Then republish `artifact/index.html`, passing `docs/support.js` and
`docs/image-slot.js` as the supporting files.

**The palette lives in one place.** The `:root` block at the top of
`docs/index.html` holds every colour, named by role (`--accent`, `--deep`,
`--body`) rather than by hue, so a swap is a one-line edit. The two categorical
sets, `PALETTE` and `SERIES_COLOR`, are the exception and sit with the data:
seven flat inks, each measured to carry white text at 5:1 or better. Keep that
property if you change one.

**`docs/index.html` is the source.** `artifact/index.html` is generated and is
never hand-edited: an edit made there is lost at the next build. The build strips
the document wrapper the artifact host supplies itself, and prepends a
`window.__resources` map that redirects the runtime's React loads from unpkg,
which the artifact content security policy blocks, to cdnjs, which it allows.
Without that map the artifact is a blank white page with nothing in the console,
because the runtime hides the template before it fetches React.

**The live subscription is session-local.** The session that publishes the
artifact is notified when it is republished elsewhere and when a comment is sent
to Claude, and that dies with the session. In a fresh session either he pastes
the artifact link, or the artifact is republished, before comments reach anyone.

## Working in this repository

- The design lives in Claude Design project `473998c6-788d-40f2-864b-26e900bdb3a5`,
  where the source file is `PhD Reps Pharmazentrum v4.dc.html`. This repository
  holds a copy renamed to `docs/index.html`, and it has since diverged
  substantially. **This repository is now the source.** Re-importing from the
  canvas would throw away the content pass.
- `support.js` and `image-slot.js` are generated bundles. Never hand-edit them.
- The crawled text of both live sites is not committed. Re-crawling is cheap:
  a breadth-first fetch of both hosts, saved as one text file per page, is how
  the content pass was grounded.
- This is not a research repository. There is no `LOG.jsonl`, no `STAGE.yaml` and
  no hypothesis register, and `.claude-no-record` records that ruling (see
  `decisions/round-01.answers.json`, D1). Decision ownership still applies: a
  choice with a defensible why is surfaced and recorded in `decisions/` like
  anywhere else.
- Pushing to `main` publishes. The page names real people, so treat a push the
  way you would treat sending an email on their behalf.
