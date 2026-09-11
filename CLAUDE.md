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

Draft, and it should not be treated as the department's authoritative calendar yet.
The page was designed in Claude Design and imported; nothing has been through a
committee sign-off, five resource links are visible placeholders, five image slots
are empty, and the upcoming/past split runs off a frozen date. See *Known defects*.

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

| Constant | Line | Entries |
|---|---|---|
| `PALETTE` | 720 | 7 |
| `SERIES_COLOR` | 722 | 7 |
| `SOURCE_COLOR` | 726 | 3 |
| `BOARD` | 728 | 3 |
| `DELEGATES` | 734 | 18 |
| `ALUMNI` | 755 | 26 |
| `STATS` | 770 | 4 |
| `HERO_LOGOS` | 777 | 4 |
| `EVENTS` | 779 | 14 |
| `NEWS` | 926 | 9 |
| `RESOURCES` | 938 | 4 |

Three things are derived rather than stored, and each is a trap when editing:

- **Delegate email addresses** are generated from the name by `mail()` (line 986):
  lowercase, transliterate the umlauts, strip the remaining accents, then join the
  first and last token with a dot before `@unibas.ch`. `DELEGATES` carries no email
  field. Board addresses are stored literally and are the escape hatch.
- **Board portrait slot ids** are `v4-board-portrait-<array index>` (line 1094), so
  an image follows the position, not the person. Reorder `BOARD` and the portraits
  swap.
- **Board avatar colours** index `PALETTE` without a modulo (line 1094), so a fourth
  board member would get `undefined`. The delegates version wraps correctly.

Every count in the prose is a hardcoded word or numeral, not read from the arrays:
"Twenty-one elected representatives" (line 69), "21" (line 194 and `STATS`), "Meet
all twenty-one" (line 211), "Three on the board, eighteen in the assembly" (line
472), "Eighteen delegates" (line 501), "Nine research groups" (line 189), and
"Twenty-six names" (line 1105). All are right today. After the next election they
will not be, and nothing will complain.

## Known defects

Ranked by how much damage each does if it ships as is. Line numbers are
`docs/index.html` unless stated.

1. **The clock is frozen.** `const now = new Date('2026-07-31T00:00:00')` at line
   1015 decides what counts as upcoming. Today is well past that, so events that
   have already happened are still filed as upcoming and the home page can headline
   one of them. The Past filter will never show them. The fix is one line, but the
   page silently ages until someone makes it.
2. **The mailing-list form is a stub.** `onSubscribe` (line 1114) calls
   `preventDefault()` and sets local state. The address is never sent anywhere, yet
   the visitor is told "You're on the list" at lines 75, 310 and 649. Three copies
   of the form exist, at lines 70, 304 and 643. Either wire it to the list manager
   or replace it with a mailto link before this is public.
3. **Eighteen of the twenty-one email addresses are guesses.** See `mail()` above.
   The likeliest to bounce is Natasha Marion Bärenzung, where the rule drops the
   middle name and produces `natasha.baerenzung@unibas.ch`. The page's own caveat
   about the address format only renders in the Searchable-directory layout, which
   is not the default, so the caveat is invisible while the links are live.
4. **Five dead resource links** carrying a visible "— link to add" hint: doctoral
   regulations (line 943), annual progress report (944), the university ombuds
   office (952), psychological counselling (953), and travel and conference grants
   (960). Two of those five are the safeguarding routes, so a student in difficulty
   follows the site's own escalation list and lands back on the same page.
5. **Five empty image slots** render their prompt text to visitors: the group photo
   (line 207), three board portraits (482) and the hoodie (686). They cannot be
   filled by putting a file on the server either. `<image-slot>` persists a dropped
   image through `window.omelette.writeFile` into a `.image-slots.state.json`
   sidecar, and that function only exists inside the Claude Design host. On a static
   server the slots are permanently empty and read-only. The component also
   hardcodes `alt=""` with no way to set it. Replacing them with plain `<img>` tags
   and real files is probably the right move, and it is a decision rather than a
   chore.
6. **Accessibility.** No `lang` attribute on `<html>` (line 2). Several declared
   colours fail WCAG AA: `--muted` #86a0a9 is 2.76:1 on white and is used for event
   times, places, dates and group names; `--faint` #b7c9cf is 1.71:1 and is every
   form placeholder; `--teal` #2a8f98 is 3.83:1 and is the background of every
   primary button with white text at 14.5 to 15.5 px. Section labels are `<span>`
   rather than headings, so the visual hierarchy is invisible to a screen reader,
   and the three board members sit at `<h2>` alongside the section holding the other
   eighteen. The alumni toggle (line 569) has no `aria-expanded`. No
   `prefers-reduced-motion` guard on the `lift` animation (line 43) or the global
   smooth scrolling (line 28).
7. **Client-render fragility.** `support.js` hides the template before it fetches
   React. If unpkg is blocked, the visitor gets a blank white page with no message;
   if `support.js` itself fails to load, they get raw markup full of literal
   `{{ leadTitle }}`. There is no `<noscript>`. One static `<title>`, no meta
   description, no Open Graph tags and no favicon, so every shared link previews
   identically, which undercuts a site whose distribution model is pasting event
   links into chat.
8. **Two prose claims contradict the data.** The alumni panel says "the fifteen who
   started the thing" (line 576) against thirteen entries annotated Co-founder. The
   reps page says one delegate per research group (line 472) while Molecular and
   Systems Toxicology has five and Pharmaceutical Technology has one.
9. **Narrow-phone overflow, unmeasured.** Four row layouts use fixed grid columns
   with nowrap content (lines 225, 377, 516, 603). The events row is estimated at
   about 320 px minimum against about 284 px of usable width at a 320 px viewport.
   One resize test would settle it.
10. **CSP.** The runtime uses `new Function`, runtime `insertRule`, and inline styles
    on nearly every element, so any strict Content Security Policy needs
    `unsafe-eval` and `unsafe-inline`. Worth raising before a hosting conversation
    with university IT, not after.

The two console errors on load are benign: a 404 for the image-slot sidecar, which
the component swallows, and a 404 for a favicon that does not exist.

## Open questions, his to rule

- Consent. Twenty-one current reps are published with clickable addresses and
  twenty-six alumni are named, some with roles, several long gone. Is there a
  university policy, and would a single `phd-reps@unibas.ch` alias be better than
  twenty-one individual mailtos?
- Are the eighteen derived addresses correct? Someone with the real list has to
  confirm them, or `DELEGATES` should carry explicit email fields.
- Is `lunch-lottery@unibas.ch` (line 816) a real alias? It is the only non-personal
  address on the site and the sole signup route for that event.
- Should the Instagram and Bluesky links point at the Biozentrum accounts (lines
  336, 337, 597)? The LinkedIn one is the Pharmazentrum's. Either they are shared
  channels and the labels should say so, or they are a carry-over.
- Where should the mailing-list form post?
- Is the autumn 2026 calendar confirmed? Six of the eight future events carry
  `provisional: true` and the retreat still says "Venue to be confirmed".
- Architecture. Keeping the Claude Design runtime costs resilience, SEO, link
  previews, CSP compatibility and the ability to fill the image slots. A prerendered
  static build would fix all five and cost the round trip back to the design tool.
  This is the largest fork in the project and it has not been decided.

## Working in this repository

- The design lives in Claude Design project `473998c6-788d-40f2-864b-26e900bdb3a5`,
  where the source file is `PhD Reps Pharmazentrum v4.dc.html`. This repository holds
  a copy renamed to `docs/index.html`. There is no sync in either direction: editing
  here does not update the canvas, and re-importing would overwrite whatever has been
  fixed here. Decide which one is the source before doing either.
- `support.js` and `image-slot.js` are generated bundles. Never hand-edit them.
- This is not a research repository. There is no `LOG.jsonl`, no `STAGE.yaml` and no
  hypothesis register, and `.claude-no-record` records that ruling (see
  `decisions/round-01.answers.json`, D1). Decision ownership still applies: a choice
  with a defensible why is surfaced and recorded in `decisions/` like anywhere else.
- Pushing to `main` publishes. The page names real people, so treat a push the way
  you would treat sending an email on their behalf.
