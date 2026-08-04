# Resume here

State of the consistency programme as of **2026-08-05**. Read this, then
`_standards/STANDARDS.md`, which is the contract everything else follows.

**In one line:** all nineteen plugins are green, the pre-revamp tags are cut and
pushed, every migrating plugin now has a browser test of its migration, and
**two items are open** — the WP-CLI/REST/blocks phase, which needs a scope call
from Lester, and a screenshot recapture Lester is doing himself. **There is no
grind left on this list.**

**The bug backlog is empty and every rule the spec states now has something
behind it.** 2026-08-04 closed the §7.6.1 release blocker, the spec-against-checks
audit and a capability audit that fell out of it. `bin/verify.py` grew from 93
checks to 127, and 41 of the spec's 48 sections are mechanically enforced, up
from 31. "Closed on 2026-08-04" has the findings.

**Read this before writing another migration test.** §7.6.1 was overstated in
this file for a week, and the correction is the difference between a useful test
and one that passes without proving anything. Core's `update_option()` already
falls back to `add_option()` when the `default_option_*` filter is what answered
`$old_value`, **so the write half is mostly core's problem**. The read half is
the real defect and always was: a bare `get_option()` behind an `is_array()`
guard skips the fold-in while the legacy row is deleted regardless. Aim at the
read. Measured, not assumed — see "Rules earned the hard way". The eleven suites
written on 2026-08-05 are all built on it.

**Green tools were not enough, and that is the lesson of the week.** Nineteen
suites, `verify.py` at zero and CI green across the board, while a data-loss
migration sat one hook-ordering accident away from firing — because §7.6.1 was a
rule the spec stated and nothing checked. The audit that found it worked by
reading the *spec* and asking "what enforces this?", never by re-reading the
plugins. It found four live defects and six sections that were themselves wrong.
**A rule nothing checks is a rule that is probably also wrong**, not merely
unenforced.

**Trust the tools over this file.** At the start of a session run
`python3 bin/verify.py --quiet` and `git log --oneline -3` in each repo. Between
them they tell you the true state without believing a word written here.

## What this is

Bringing all 19 plugins in this folder to a single written standard, so they
read as though one person wrote them on the same afternoon. The only permitted
differences between two plugins are name, features and capability.

## Decisions already made — do not re-litigate

| Question | Decision |
|---|---|
| Public identifier renames | Full canonicalisation **with** migration. The current major is unreleased in 17 of 19 cases, so renames retarget the migration that already exists rather than adding a second one. |
| Class naming | Prefix everything: `WP_Email_Admin`, `WP_Print_Admin`. `freemyinternet` keeps `FreeMyInternet_*`. |
| CI matrix | **6 PHPUnit rows — every supported stack in both modes:** WP 6.8/PHP 8.2, WP latest/PHP 8.2, WP latest/PHP 8.5, each single **and** multisite. Plus phpcs and JS jobs, so 8 checks on a JS plugin and 7 without. Multisite runs on the floor too: that is where it breaks. |
| Admin UI | Full Settings API rewrite everywhere, one menu rule (§4.1), `WP_List_Table` for all tabular screens. |
| Renamed hooks that were public in the last SVN release | **Dropped outright.** No `apply_filters_deprecated()` shims. Every one documented under `## Upgrade Notice`. |
| Versioning | Fold this work into the existing unreleased major — **except** wp-dbmanager and wp-useronline, see §14. |
| TinyMCE (wp-downloadmanager, wp-polls) | Classic Editor buttons stay; rewrite `plugin.js` vanilla. |
| Root of this folder | Tracked since 2026-08-01: `github.com/lesterchan/wordpress-plugins`, branch `main`, holding `_standards/`, `bin/`, `.wp-env.json` only. The 19 plugin directories are gitignored **by name** — a pattern would also swallow `_standards/` and `bin/`. Each is its own repo on `master`. |
| Commit signing | **None.** Use `git commit --no-gpg-sign`, despite the global `commit.gpgsign = true`. Existing history is unsigned and stays that way. |
| Supported floors | **WordPress 6.8, PHP 8.2** — raised from 6.0 / 7.4 on 2026-07-28. See §1.1. Delete any now-dead back-compat shim rather than leaving it unreachable. |
| Version markers | Own row `{{UNDER}}_version` = `array( 'plugin' => …, 'db' => … )`, **never** inside the settings array. See §2.1. |
| RTL | No `*-rtl.css` anywhere; CSS logical properties instead (§5.1). |
| README Contributors | Exactly `GamerZ`, every plugin. wp-pagenavi loses `scribu`. |
| FSF address in the GPL block | `51 Franklin Street` — confirmed by Lester 2026-08-03. Neither original group was right: sixteen carried the address the FSF left in 2005, three had the right building abbreviated. §3.1 spells the tail out and `verify.py` compares byte for byte. |
| Assertion failure messages | **Every** assertion carries one, not only the ones PHPUnit would report opaquely. Lester's call, 2026-08-03. freemyinternet is the reference. |

## What exists

* `_standards/STANDARDS.md` — the spec. **15 numbered sections, 48 including
  subsections** (this line said 17 until 2026-08-03, and nothing had counted).
  41 of the 48 have something mechanical behind them; see "Is the collection
  compliant?".
* `_standards/templates/` — the files each plugin copies verbatim, placeholders
  `{{SLUG}}` `{{NAME}}` `{{CLASS}}` `{{UNDER}}` `{{UPPER}}` `{{L10N}}`
  `{{DESCRIPTION}}`.
* `.wp-env.json` — all 19 plugins in one WordPress on 8888/8889.
* `bin/verify.py` — mechanical checker, **127 `check()` call sites**, not all of
  which apply to every plugin. `python3 bin/verify.py [slug…] [--quiet]`; exit
  status is the failure count. (This line said "~40 rules per plugin" and the
  compliance section below said 86; neither had been counted. Recount with
  `grep -c '\.check(' bin/verify.py` rather than trusting either.)
* `bin/test-all.sh` — every plugin's PHPUnit suite in one container.
  `--multisite` for the network run. Keeps going past failures.
* `bin/seed-demo.sh` — fills the root harness at http://localhost:8888
  (admin / password) with the fixtures the suites use. Re-runnable; clears only
  what it made.
* `bin/measure_assertions.py` — how many PHPUnit assertions carry a failure
  message. Parses the argument list rather than counting commas, because
  `$message` sits at a different position for every assertion.
* `bin/triage_assertions.py` — the same set split into messages that are owed
  and messages that would be filler.

Each plugin also has its own `bin/test.sh`, `bin/test-multisite.sh` and
`bin/test-e2e.sh`.

## Current state — verified 2026-08-05

* `verify.py` is 0 across all 19.
* **Eleven repositories gained a commit on 2026-08-05 that has not been pushed**
  — the migration suites. `git log --oneline -1` in each says which.
* Playwright green on every `upgrade.spec.js` written that day, and on the whole
  file for wp-dbmanager (56 tests) and wp-email (9), which were run entire.
  **The other suites' older specs were not re-run** — this line is the one in
  this file most likely to be stale by the time you read it, so re-check rather
  than trust it.
* PHPUnit was **not** re-run on 2026-08-05. Nothing that day touched shipped
  code — the eleven commits are `tests/e2e/` only — but that is an argument, not
  a run.
* **Every assertion in the collection carries a failure message** — the total
  moves with every commit, so the ratio is the claim:
  `python3 bin/measure_assertions.py /path/to/plugins/*` re-derives both.
* The permalink audit of the E2E suites is complete — see below.
* **No known plugin bug is outstanding.** wp-dbmanager's was fixed on
  2026-08-04 and now has both a rule and a test behind it. The lesson stands
  even though the line has flipped: it was latent rather than firing, every
  suite was green, and nothing here caught it because `verify.py` had no rule
  for it and no test took the admin path.

## Remaining work, in order

**Two items are open**, and neither is a grind. Item 1 is waiting on a scope
decision from Lester; item 2 is Lester's to schedule. Everything else that was
on this list is done — see the two "Closed on" sections below, which keep the
findings and drop the instructions.

1. **WP-CLI, REST API and Gutenberg blocks across the collection.** The only
   substantial item left, and a phase of its own rather than a cleanup.
   `wp-sweep` already has `WP_Sweep_Command` and `WP_Sweep_API` and is the
   reference.

   **The naming is settled** (§13.3, reversed by Lester 2026-08-04): the slug
   **without** the `wp-` prefix — `wp sweep`, `sweep/v1`, not `wp wp-sweep`. The
   `wp-` prefix is a wordpress.org directory convention rather than a naming rule
   for what a plugin registers, the ecosystem norm is the brand (`wp wc`,
   `wp yoast`), and these are the names the released 1.2.0 already shipped — so
   the change *deleted* a breaking change this campaign had invented and
   documented.

   **Three names are deliberately left open**: `email`, `print` and `stats` are
   bare nouns a dozen plugins might want, and §13.3 says in terms that it does
   not settle them. Decide each if and when it earns a command — a qualified
   name, or a shared `wp lc <plugin>` parent.

   **What is still open, and is Lester's:** the scope. Which plugins earn a
   command, a namespace or a block, and whether a block wraps the existing
   shortcode or replaces it. §13.3 pins only the naming.

2. **Recapture every plugin's wordpress.org screenshots.** Asked for by Lester
   on 2026-08-04, which is what puts it on this list at all — see the note below
   about SVN. **Lester is doing this himself, on a day of his choosing.** Do not
   run it while anything else wants Playwright and a seeded WordPress: this
   file's own E2E lesson is what concurrent runs do to a 7.6 GiB Docker.

   **Every screenshot in the collection is pre-revamp.** The admin UI was rebuilt
   wholesale — Settings API everywhere, `WP_List_Table` on every tabular screen,
   one menu rule, renamed settings headings — so the images no longer show the
   software. That is the reason to redo all nineteen rather than only the five
   that fail the count check below. wp-sweep's are the most out of date of all:
   its sweep screen gained group headings and icons on 2026-08-04.

   Counted 2026-08-04, `## Screenshots` lines in each repo's `README.md` against
   `screenshot-*` files in `~/svn/wordpress_plugins/<slug>/assets/`. **Fourteen
   agree and five do not**, and the five disagreeing is the smaller problem:

   | Plugin | README lines | assets | |
   |---|---|---|---|
   | freemyinternet | 3 | 1 | two described and never shipped |
   | wp-polls | 9 | 10 | one shipped and never described |
   | wp-postratings | 5 | 6 | one shipped and never described |
   | wp-sweep | 3 | 2 | one described and never shipped |
   | wp-useronline | 4 | 3 | one described and never shipped |

   The rule wordpress.org applies is positional: `screenshot-N.png` is captioned
   by the Nth line of the `Screenshots` list, so a missing file silently shifts
   every caption after it onto the wrong image. **The count matching is necessary
   and not sufficient** — the fourteen that agree have never been checked for
   whether each line still *describes* its image, and after a UI rebuild the safe
   assumption is that none of them do.

   How many to take is a judgement per plugin, not a number to preserve. Lester's
   brief was explicit that the current count is stale and the new one is ours to
   choose.

   Notes for whoever runs it. `bin/seed-demo.sh` fills the root harness at
   http://localhost:8888 (admin / password) with the fixtures the suites use,
   which is the site to photograph — a separate wp-env from any plugin's tests
   environment. Read
   https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/ for the
   naming and size rules first. **Write only into
   `~/svn/wordpress_plugins/<slug>/assets/`**, touch nothing else in those
   checkouts, and do not `svn add`, commit or push — Lester commits the assets
   with the release. The checkouts are otherwise stale 2022-era trees (see
   Traps).

**Off this list on purpose:** the SVN release itself. Lester does it by hand.
Nothing here pushes, tags or touches SVN — **except item 2**, which Lester
explicitly asked for on 2026-08-04 and which writes screenshots into `assets/`
and nothing else.

**Reading the diffs for voice is no longer on this list**, and that is a
decision rather than an oversight. The mechanical half is done and checked on
every push; what was left was a human read with nothing to hand off, and it sat
here for a week as a task nobody could pick up. What it *measured* is worth
keeping and is under "Rules earned the hard way" — comment density is not a
defect signal in this collection, and two successive attempts to make it one
were both wrong.

## Closed on 2026-08-05 — the eleven migration suites

**Every migrating plugin now has a browser test of its migration.** Fifteen
migrate; all fifteen have a green `tests/e2e/upgrade.spec.js`. The eleven
written on 2026-08-05 were wp-commentnavi (7 tests), wp-pagenavi (7),
wp-dbmanager (6), wp-email (9), wp-downloadmanager (6), wp-draftsforfriends (8),
wp-useronline (6), wp-polls (8), wp-stats (6), wp-postratings (7) and
wp-postviews (8) — 78 tests, each run to green before it was committed.

The findings, all of which are now in the E2E lessons and none of which reading
the code would have produced:

* **A `wp eval` call is a full WordPress request**, so for the five plugins that
  migrate on `plugins_loaded` or `init` it *is* the upgrade. Seeding the legacy
  rows in one call and reading them back in a second finds them already
  migrated: the browser request that follows has nothing left to do and the
  suite is testing WP-CLI. Seed and read back inside one call.
* **A scalar legacy row reads back as a string.** Arrays keep their types, being
  serialised. Every reader casts, so it has never mattered — but four suites
  asserted integers on the first run and were wrong about every install there is.
* **wp-downloadmanager's legacy row wins over an existing current row**, which
  is the opposite of what its test assumed and what the migration means. Pinned
  in both directions now, because the wrong reading is the plausible one.
* **A blocking `execFileSync` inside a test cannot be interrupted by Playwright's
  timeout**, so a slow helper reads as a hang rather than a failure. Two runs
  were abandoned on that before the machine turned out to be the cause; a single
  `wp eval` answers in 2.3s on an idle box and the same suite that took an hour
  under load took two minutes without it.

wp-commentnavi's and wp-pagenavi's were confirmed by mutation, run separately
rather than one assumed from the other: three of seven tests went red in each.
The other nine rest on the collection's usual guard — every one of them failed
at least once on its first run and was fixed, which is the same evidence in a
less deliberate form.

## Closed on 2026-08-04

The instructions are gone; the findings are kept. Everything here was an item on
the list above and is now either shipped or written into a check.

* **The §7.6.1 release blocker** (was item 1a/1b). wp-dbmanager's migration read
  its settings row bare — the read half of §7.6.1, the half core does not cover.
  Fixed, and `verify.py` fails any shipped file reading the plugin's own settings
  row through a one-argument `get_option()`. The legacy row is deliberately not
  covered: `register_setting()` names the *current* row, so no `default_option`
  filter exists for the old one and a bare read of it is correct, which is what
  five plugins do. Shipped code only, by allow list, because tests read the row
  bare on purpose — about sixty times, every one of them right.
* **Stock-defaults fixtures** (was item 1d), eight plugins. They are the
  fixtures the eleven E2E migration suites were built from — a customised row
  cannot see §7.6.1 at all.
* **wp-polls' `save()`** (was item 1e) hardened to add the row itself. The
  premise was wrong — no data was ever at risk — and it is committed as
  hardening.
* **Three false docblocks** (was item 1f). Exactly three plugins pass no
  `default` to `register_setting()` — freemyinternet, wp-commentnavi,
  wp-pagenavi — and all three carried a docblock claiming they did. One wrong
  sentence, copied to precisely the set of plugins it was wrong about.
* **The spec-against-checks audit** (was item 2). Nine sections gained a rule,
  plus §7.6.1 and the two §2.7 rules: **41 of 48 sections have something
  mechanical behind them**, up from 31, and `verify.py` went from 93 `check()`
  sites to 127. Six sections were found to be simply wrong and were corrected.
  The six sections still without a check are listed under "Is the collection
  compliant?".
* **The capability audit**, which fell out of it. Four plugins invent a
  capability and three of the four granted something other than what they check.
  Written up under "Rules earned the hard way".
* **wp-sweep's WP-CLI and REST names** (part of item 2's fallout) restored to
  what 1.2.0 shipped, deleting a documented breaking change.
* Items 5, 6 and 7 closed on 2026-08-03: the wp-draftsforfriends API question,
  the literal-assertion sweep, and routing administrator creation through a
  helper. Their lessons are under "Rules earned the hard way" and "Tests that
  cannot fail".

## The pre-revamp tags — done 2026-08-03

**All nineteen are tagged and pushed**, so every plugin now has a ref for "as it
shipped before this work". Verified against each remote afterwards rather than
trusted from the push output: nineteen annotated tags, each on the commit in the
table below.

`bin/tag-pre-revamp.sh` is what created them. It takes the directory holding the
plugin repos, is safe to re-run — a tag that exists is left alone — and refuses
to guess: a shallow clone missing the commit is reported rather than tagged.
Deriving the boundary needed full history, and the clones arrive shallow holding
only the campaign's own commits, so `git fetch --unshallow origin` is what made
the pre-revamp past visible at all.

**It had to run from Lester's machine.** The sandbox's git proxy answers a tag
push with HTTP 403 while allowing branch pushes, so the tags could not leave a
session; they were created and verified in one and the container took them with
it. That is why this sat waiting rather than being finished when it was written.

**Two repositories already carried tags, and an earlier draft of this file said
none did.** wp-pagenavi has six and wp-useronline four, bare version numbers
from scribu's tenure (2010–2014), already on their remotes. They do not collide
with the new tags and their naming is the same bare-version shape. The claim was
never checked against `git tag` — it was prose about a number nothing measured,
which is the same failure §7.2.2's note records.

| Plugin | Tag | Commit | Date |
|---|---|---|---|
| freemyinternet | 0.01 | `8a7a7a59` | 2020-05-20 |
| wp-ban | 1.69.2 | `8f5452ac` | 2025-03-09 |
| wp-commentnavi | 1.12.2 | `45b51b7d` | 2023-08-09 |
| wp-dbmanager | 2.80.10 | `b7ad9070` | 2024-11-24 |
| wp-downloadmanager | 1.69.1 | `416b9f54` | 2026-02-13 |
| wp-draftsforfriends | 1.0.2 | `952592aa` | 2023-08-09 |
| wp-email | 2.69.3 | `066014a9` | 2024-12-18 |
| wp-pagenavi | 2.94.5 | `3a010444` | 2024-12-19 |
| wp-pluginsused | 1.50.2 | `7cff1208` | 2023-08-09 |
| wp-polls | 2.77.4 | `50adb772` | 2025-12-26 |
| wp-postratings | 1.91.2 | `75e54f4f` | 2024-07-16 |
| wp-postviews | 1.78 | `9b1c2c84` | 2026-01-16 |
| wp-print | 2.58.2 | `dde8f97c` | 2023-09-08 |
| wp-relativedate | 1.51 | `b7fa2f8d` | 2023-08-09 |
| wp-serverinfo | 1.66 | `a7dc3cfe` | 2026-06-16 |
| wp-showhide | 1.06 | `a1a0ee21` | 2025-11-28 |
| wp-stats | 2.56.1 | `22839ce3` | 2026-06-22 |
| wp-sweep | 1.2.0 | `cff61a76` | 2026-06-19 |
| wp-useronline | 2.88.9 | `14d4edc2` | 2025-07-15 |

Two things the boundary turned up, both about released state rather than tags,
and both re-checked against the commits themselves before the tags were cut:

* **wp-email shipped with its header behind its `Stable tag`.** At `066014a9`
  the header reads `2.69.2` and the `Stable tag` reads `2.69.3`, so wordpress.org
  served that tree as 2.69.3 while every site running it reported 2.69.2 — a
  standing update prompt that never clears. It had happened once before, at
  2.69.0/2.69.1. The tag is named for what shipped, and says so.
* **Five plugins carried `Stable tag: trunk`**, not four: freemyinternet,
  wp-commentnavi, wp-draftsforfriends, wp-pluginsused and wp-relativedate. §14
  says four. This is the git side of that claim rather than the SVN side, so it
  is evidence and not proof, but the number to check is five.

## READ FIRST — CI and your machine are not the same environment

Two divergences have each cost a day. Both have the same shape: something is
true on a fresh CI install and false on a long-lived local container, so a suite
passes in one place and fails in the other, and neither says which is right.
**Assume CI is right — it installs fresh, which is what a real site looks like.**

### The permalink structure decides what the suites test

**WordPress turns pretty permalinks on during installation**, whenever the
server can rewrite — `wp_install_maybe_enable_pretty_permalinks()` in
`wp-admin/includes/upgrade.php`. The wp-env container can, so **every fresh
install is `/%year%/%monthnum%/%day%/%postname%/`.** A long-lived local wp-env
drifts to plain and stays there.

That is not a nuisance. It means the suites cover *different code paths in each
environment*: wp-print's `/print/` endpoint was exercised only in CI, and its
`?print=1` fallback only locally. Five suites were red on CI for weeks while a
full local sweep reported 867/867. Before believing a green local E2E run, check
`wp option get permalink_structure` in the tests container.

**The rule, settled 2026-08-03:** a suite that depends on the structure **sets
it to a literal**. It never reads the site's and puts that back — that is not
restoring state, it is laundering drift, and it is what kept the original
defect alive through the fix of the bug inside it. A test that wants the other
structure sets it *after* the last REST call, because `requestUtils` stops
resolving the moment `/wp-json/` moves (the HTML 404 arrives as "Unexpected
token '<'", which sends you looking in the wrong place entirely).

Three plugins depend on rewrite endpoints — wp-print `/print/`, wp-email
`/email/` and `/emailpopup/`, wp-downloadmanager `/download/` — and all three
pin an absolute structure in `beforeAll`. The other sixteen are
structure-independent: they navigate through `post.link`, which core builds
correctly either way, or through admin URLs.

One of these was **a real bug in the field, not a test defect**:
`redirect_canonical()` rewrites `?p=<id>` to the pretty permalink, and the query
that lands there looks a post up by slug among the *public* statuses — so
wp-draftsforfriends' share links to private and scheduled posts 404'd on
essentially every real site while 42 local tests passed over it. Fixed in
`WP_DraftsForFriends_Preview::keep_the_share_url()`.

Two shapes to grep for, both mechanical, both clean as of 2026-08-03:

* `` `${ something.link }&` `` — concatenation onto a permalink. Build the URL
  with `URL` and `searchParams`, or branch on `includes( '?' )` as
  `wp-print/tests/e2e/helpers.js` does.
* an assertion naming `?p=`, `?page_id=`, `?author=` or `?cpage=` — the plain
  form of something core has a function for. Ask WordPress for it.

### `vendor/` exists under CI and not on your machine

`composer install` runs in CI and usually has not run in a working tree here, so
**any test that walks the plugin root sees a different set of files in each
place.** Composer declares `ComposerAutoloaderInit<hash>` in
`vendor/composer/autoload_real.php` — a class inside the plugin directory that
is not the plugin's.

This broke all six PHPUnit jobs in wp-showhide and wp-pluginsused on 2026-08-03.
The test matched every class whose file sat under the plugin root and subtracted
`tests/`; locally that found the two real classes, and under CI it also found
Composer's.

**Prefer an allow list to a deny list** when scanning the plugin's own files —
`includes/` plus the root entry points. A deny list acquires a new member every
time somebody installs something.

## E2E lessons that will recur — read before writing the next suite

* **`bin/test-e2e.sh` is the only entry point.** wp-env installs a plugin into
  the tests environment but activates neither it nor any theme; PHPUnit needs
  neither, because its bootstrap loads the plugin itself and never renders a
  page. A browser gets no plugin, no menu, and a front page returning 200 with
  an empty body. The script fixes both on every run.
* **A plugin that renders only under some condition needs that condition
  created *and* a test asserting the fixture itself**, or the suite is vacuous.
  Both pagination plugins have a "the fixture really is more than one page"
  test for exactly this.
* **Template-tag plugins need a theme shim** — a mu-plugin under
  `tests/e2e/mu-plugins`, mapped by `env.tests.mappings` in `.wp-env.json`, and
  **guarded on `PHP_SAPI === 'cli'`** because PHPUnit shares that environment. A
  fixture forcing comment paging on made a unit test fail while the plugin was
  behaving perfectly.
* **Fixtures created in parallel tie on timestamp** and sort unpredictably.
  Create sequentially with explicit dates where order matters.
* **Navigate by clicking the link the plugin rendered**, not by typing a URL.
  The shape of a page URL is not the plugin's to know — `/page/2/` is pagination
  on a site with a permalink structure and a 404 on one without — and the link
  is the thing under test anyway.
* **`page_comments`, `comments_per_page`, `default_comments_page` are not in
  core's REST settings allowlist.** `requestUtils.updateSiteSettings()` accepts
  them and silently changes nothing. Set them from the fixture. `posts_per_page`
  *is* in the allowlist.
* **Assert on the plugin's own accessible labels, not the text beside them.**
  That text is a template a site can replace; a test reading it is really
  asserting nobody opened the Templates tab.
* **Five per page**, not the WordPress default of ten, in both the suites and
  the demo seeder — more pages for the same fixture, and pages are the only
  thing a pagination plugin is about.
* **A time-relative fixture asserting a calendar concept is a bug waiting for
  the clock.** wp-relativedate's "yesterday" fixture was `Date.now() - 26
  hours`, which lands two calendar days back when the suite runs between
  midnight and 02:00. CI ran at 01:44 UTC and the plugin was right. Pin to
  midday.
* **Run E2E one plugin at a time.** Four concurrent Playwright runs tore each
  other down on a 7.6 GiB Docker.
* **A `wp eval` call is a full WordPress request, so for five plugins it *is*
  the upgrade.** wp-dbmanager, wp-stats, wp-useronline, wp-postviews and
  wp-postratings run their migration on `plugins_loaded` or `init`, which WP-CLI
  reaches like any other request — so seeding the legacy rows in one call and
  reading them back in a second finds them already migrated. The browser request
  that follows then has nothing left to do, and a suite that looks like it is
  testing the admin path is testing WP-CLI. **Seed and read back inside one
  call**, and put everything the fixture needs — the legacy rows, an
  already-current row, the legacy cron events — into that same call. Two of the
  three assertions in wp-dbmanager's first run failed on this and the reason took
  a mutation-shaped detour to find. The plugins that migrate on `admin_init` are
  unaffected: WP-CLI never fires it.
* **A scalar legacy row reads back as a string.** WordPress stores an option
  value as text, so `update_option( 'download_method', 2 )` is `"2"` on the way
  out and `"2"` is what the fold-in writes into the consolidated array. Arrays
  are serialised and keep their types. Every reader casts, so it has never
  mattered — but a test asserting `2` is asserting something untrue of every
  install in the world.

**Four defects in the *tests* accounted for 20 of the 39 fixes** in the
2026-08-02 sweep, and each will recur in any suite written the same way:

1. **A Settings API checkbox is two inputs** — a hidden `value="0"` beside the
   box, so `[name="…"]` matches both and dies of Playwright strict mode. Hit
   wp-useronline ×3, wp-ban, wp-email ×4 in one loop, wp-downloadmanager. Give
   every suite a `checkbox()` helper beside its `field()`.
2. **`get_current_user_id()` inside `wpEval()` is 0.** `wp eval` has no logged-in
   user, so `get_user_meta( get_current_user_id(), … )` reads the empty string
   and the assertion reports a working feature as broken. Hit wp-downloadmanager,
   wp-email, wp-draftsforfriends.
3. **A page-global XSS sentinel is contaminated by core**, which prints
   unescaped values on the same page: the admin bar's `Howdy, <display name>`,
   `comment_form()`'s `Logged in as …`, and `the_title()`. Scope the assertion to
   the plugin's own container. Hit wp-postviews, wp-useronline, wp-stats ×2,
   wp-downloadmanager ×2.
4. **Strict mode on selectors that legitimately match twice.** `WP_List_Table`
   draws its tablenav above *and* below (`.total-pages`, `tfoot, tbody`), and the
   Dashboard carries core's own `.notice-error`.

Two suites are thin rather than wrong, and are where to spend the next E2E hour:
**wp-email** (45) leans on the interceptor recording one message, never covers
`[email_link]` placement within content, and renders each standalone template
once; **wp-postviews** (98) is padded — a six-way parametrised loop at
`display.spec.js:114` and a four-way at `settings.spec.js:87` make ~15 of its 98
one assertion with a different argument.

## Tests that cannot fail

Three have been found, all passing for years. The shape is worth recognising on
sight.

* **A hardcoded list compared against itself.** wp-showhide and wp-pluginsused
  looped over an array of their own class names asserting each starts with the
  plugin prefix — true of any list anybody would type. Fixed 2026-08-03 by
  reading `get_declared_classes()` instead. **Any assertion whose two operands
  both come from literals written into the test is this bug.**
* **A filter that matches nothing.** The replacement for the above is only
  honest because it asserts the set it found is non-empty first. A scan that
  finds no files passes silently.
* **A fixture the plugin never renders.** wp-sweep's vitest suite passed while
  `messageContainer()` was broken in every browser, because
  `tests/js/helpers.js` built a DOM the plugin does not produce. A unit test
  that constructs its own fixture tests the fixture.
* **A fixture that differs from the defaults.** wp-print had a migration test
  that passed throughout the bug, because its fixture was customised and so its
  result differed from the defaults — the write landed. It could not see a
  defect that only shows when the two are equal. Both new tests were confirmed
  to fail with the fix reverted.

**Confirm a new test fails before believing it passes.** Every fix above was
verified by reverting the code and watching the test go red.

## Run the same checks CI runs

**`php -l` and `verify.py` passing means very little on its own.** They are a
strict subset of what gates the repositories, and treating the subset as the
whole put four broken commits on master on 2026-08-03 — two phpcs errors, a
class scan that matched `vendor/`, and a hook-surface guard that had to be
updated deliberately. Every one was invisible to the checks being run here and
obvious to the ones that were not.

**A SessionStart hook installs the toolchain**, in all nineteen plugins and in
this repository: `.claude/hooks/session-start.sh`, registered by
`.claude/settings.json`. It installs Node 24 (what `ci.yml` pins), phpcs and
WPCS, the repo's npm dependencies where there is a lockfile, and starts the
Docker daemon, which is present but not running by default. Idempotent and
remote-only.

**One file, byte-identical in all twenty.** It names no plugin and branches on
what it finds, and `bin/verify.py` holds the copies to
`_standards/templates/.claude/` — so edit the template and copy it out, never a
copy. `.claude/` was already in the metadata fixture's `SKIPPED_DIRECTORIES` and
is already named in §1 as development tooling excluded from the SVN deploy, so
it ships to nobody.

That makes **two of the nine CI jobs reproducible here** — "PHP coding standards"
and "JS coding standards and tests". Both were validated: phpcs catches a planted
double-quoted string, `npm ci` is clean under npm 11, `eslint` passes, and
wp-sweep's 34 vitest tests run.

**The six PHPUnit jobs and the Playwright job still cannot run**, and not for
want of Docker — Docker starts fine. wp-env downloads WordPress from
`*.wordpress.org`, and this session's egress policy blocks that host (403 at the
agent proxy; `npmjs.org` and `github.com` are allowed). That is an organisation
policy, not something to route around, so those suites belong to CI. It is the
gap that let a hook-surface test failure through on 2026-08-03.

To install the PHP side by hand instead:

```sh
export COMPOSER_ALLOW_SUPERUSER=1
composer global config --no-plugins allow-plugins.dealerdirect/phpcodesniffer-composer-installer true
composer global require squizlabs/php_codesniffer wp-coding-standards/wpcs
```

Then, **from inside the plugin directory**, which is what CI does and what makes
it pick up that plugin's own `phpcs.xml`:

```sh
cd <plugin> && "$(composer global config bin-dir --absolute)"/phpcs -q --report=full .
```

Run from anywhere else it falls back to a default standard, misses the ruleset,
and reports tens of thousands of issues from `vendor/` — which is a broken
invocation, not a finding.

Two sniffs the collection's own style trips repeatedly, both worth knowing
before writing a docblock: a long description must **start with a capital
letter** (a backtick or a lowercase identifier fails, though a `§` slips through
as multibyte), and a string with nothing to interpolate must use **single
quotes**.

For the JS job, `npm ci && npm run lint:js && npm run test:js` inside a plugin,
under Node 24. Under Node 22's npm 10 the lockfiles read as out of sync, which
is the false alarm in Traps below.

**PHPUnit remains CI-only.** That gap is real: `tests/test-metadata.php` pins
each plugin's hook surface as an exact set, so any new hook fails it by design,
and nothing short of running the suite will tell you.

## Traps

* **A red job whose failing step is `Start wp-env` is an environment failure,
  not a finding.** wp-env's own Dockerfile fetches
  `https://composer.github.io/installer.sig` while building `tests-cli`; a
  runner network blip makes the hash check declare the installer corrupt and
  delete it, and the next step has no file to run. Re-run it once before
  reading anything into it. Seen three times on wp-showhide's WP 6.8 / PHP 8.2
  single-site job, most recently 2026-08-03, and a re-run has fixed it every
  time. If it keeps recurring, a retry on that step is the real fix.

* **`npm ci` failing with `Missing: yaml@2.9.0 from lock file` is your npm, not
  the lockfile.** `ci.yml` pins Node 24, whose npm is 11.x, and the lockfiles
  are correct under it — checked 2026-08-03 across four plugins. npm 10
  resolves vite's optional peer `yaml` differently and declares the lock out of
  sync. **Do not regenerate the lockfile to make the message go away:** npm 10
  also strips the `libc` arrays npm 11 writes on optional platform packages, so
  the "fix" is a 69-line diff that removes metadata CI depends on and silently
  reverses the drift it claims to correct. Match the npm major first.

* **Test discovery is `<directory prefix="test-">`.** A test file not named
  `test-*.php` is **silently not run** rather than erroring. After any rename,
  compare the test count against what the plugin reported before — a suite that
  suddenly got smaller is the symptom.

* The shared `phpunit.xml.dist` turns on `beStrictAboutTestsThatDoNotTestAnything`,
  `failOnWarning` and `failOnRisky`. A test without an assertion is risky, and
  risky is fatal. That is deliberate.

* The local `~/svn/wordpress_plugins` checkouts are **stale** (2022-era). Query
  `plugins.svn.wordpress.org` directly for the released baseline — §14 has the
  table.

* `plugin_deploy.sh` (in `outside this repository`) globs its
  exclusions, so `phpunit*.xml*` and `vitest.config.*` are already excluded.

* `wp-serverinfo` and `wp-sweep` have extra `claude.yml` /
  `claude-code-review.yml` workflows. Those are **not** part of this standard;
  leave them alone.

* **wp-draftsforfriends' bootstrap logs real `Table 'wp_draftsforfriends'
  doesn't exist` errors** during `_delete_all_posts`, because
  `WP_DraftsForFriends_Shares::delete_for_post()` is hooked to `deleted_post`
  and fires before the table exists. Noise, not a failure.

* `bin/test-all.sh` triggers a wp-env deprecation about
  `testsEnvironment`/`env`/`testsPort`. §10 pins that `.wp-env.json` shape in
  all 19, so it will need changing together when wp-env drops them.

## Is the collection compliant? What checks what

Worth keeping because the answer is not "run `verify.py` again".

**The mechanical half is continuously checked and green.** `bin/verify.py` is
**127 checks**, and the shared metadata fixture covers §13 including the
shared-row contract two plugins violated. Both run on every push. Re-auditing
nineteen plugins against the spec by hand buys nothing.

**41 of the spec's 48 sections have something mechanical behind them.** These
six do not, and each stays that way for a reason:

| Section | Why not |
|---|---|
| §4.4 Markup | judgement |
| §7.2.1 Process-wide state | needs the suite running |
| §7.2.3 A suite that dies is not one that passed | enforced by `bin/test-all.sh`; §7.2.3 says so, so the next audit does not write a second check |
| §7.3 Coverage | a number, and gaming it is worse than missing it |
| §13.3 WP-CLI and REST naming | nothing to check until item 1 ships |
| §15 Order of work | process, not state |

Two more were attempted and deliberately abandoned, which is worth as much as
the rules that landed. **§4.2.2's "do not repeat a word the context supplies"** —
the section itself says the obvious mechanical reading is wrong, and a check for
it fires on `Users Online` while missing `E-Mail Templates`. And **§2.7's "every
check of the plugin's own capability goes through one filter"**, which cannot be
separated mechanically from the core meta-caps, `unfiltered_html` and editor
gates the section explicitly exempts. Both were written, seen to be useless, and
deleted rather than left in looking like coverage.

**The audit worth doing is the spec against the checks, not the plugins against
the spec.** Every defect of the last week came out of it: `@package` split along
file age, the metadata fixture free to drift, §11's raster ban satisfied by all
nineteen and enforced by nothing, §12's script list stale in all nineteen
identically, §7.6.1, and the capability grants below. **A rule the spec implies
and nothing enforces is a rule nineteen copies will drift from, and the drift is
invisible precisely because every tool is green.**

## Rules earned the hard way

* **Comment density is not a defect signal in this collection, and two
  successive attempts to make it one were both wrong.** Recorded because the
  error is easy to repeat, and because it is the clearest case of a measurement
  that looked objective and was not:

  * *Raw comment share* rates wp-polls worst (35.6 % against wp-postratings'
    46.6 % at nearly the same size). wp-polls is in fact among the best
    explained plugins here. Its share is low because it carries a lot of code
    per docblock.
  * *Counting only `//`* rates wp-relativedate worst in the collection, at 0.4
    per 100 lines. It is second **best** at 15.4. The plugin explains itself in
    `/* … */` blocks, which a `//`-only counter files as docblocks.
    wp-pluginsused moved from second-worst to fifth-best for the same reason.

  Measured properly — inline `//` plus non-docblock `/* */`, against code lines
  — the collection spans 6.8 to 16.0 per 100, and **the low end is correct**.
  wp-email's least-commented file is a `WP_Widget` subclass with 80 lines of
  code and no inline explanation at all, because nothing in it is surprising.
  **Counting cannot tell "under-explained" from "nothing to explain"; only
  reading can.** The mechanical half is clean and checked: every function in
  shipped code has a docblock, every file has a file-level one, and `@package`
  is the display name everywhere.

* **`register_setting()` attaches two things to the settings row, and
  activation and WP-CLI run neither** — a `sanitize_option_*` filter, and, where
  a `default` is passed, a `default_option_*` filter that answers `get_option()`
  with the shipped defaults for a row that does not exist. Written up as
  **§7.6.1**. **Any migration test that only runs under WP-CLI is testing the
  easy path.** Four variants were found across five plugins.

  **The read half and the write half are not equally dangerous, and this file
  said they were until 2026-08-04.** Read `wp-includes/option.php` before
  writing another word about either.

  * **Reading is the real defect.** A bare `get_option()` behind an
    `is_array()`/`false ===` guard cannot tell an absent row from a defaulted
    one, so the fold-in is skipped while the legacy row is deleted regardless.
    Nothing in core saves you. This is what wp-print, wp-pluginsused and
    wp-dbmanager each had, and it is what `verify.py` now fails.
  * **Writing is mostly core's problem, and core handles it.**
    `update_option()` asks the `default_option_*` filter what it would answer
    and calls `add_option()` when that is what `$old_value` was. The one gap is
    the comparison *above* that fallback, which returns early when the value
    being written is identical to the one just read — and `update_option()`
    **sanitises before it compares**, so a sanitiser that alters its input at
    all closes even that. wp-polls was measured against this and was never
    losing data.

  The practical consequence, and what the eleven E2E suites were built on:
  **assert the raw row, but do not expect the bare `update_option()` to be what
  fails.** A migration test that goes red only when the read is bare is testing
  the thing that actually breaks.

* **One list must not drive both the migration and uninstall.** Both §13.2
  shared-row violations (wp-polls, wp-downloadmanager) were that design: the
  single list is what stops a row the plugin owns drifting off the uninstall
  list, and both had a row they never owned on it. Each fix is pinned by two
  tests — the contract (absent from the uninstall list) and the behaviour (a
  seeded row survives) — because a test that walks the single list cannot see
  the defect. **Do not fold the lists back together.**

* **The capability a plugin grants must be the capability it checks.** Four
  plugins invent one — wp-downloadmanager, wp-email, wp-polls, wp-postratings —
  and **three of the four granted something other than what they gate on**:
  `add_cap()` took the constant or its literal string while every screen checked
  `capability()`, the same value passed through the plugin's filter. A site
  using that filter gets an administrator holding a capability nothing looks at
  and screens gated on one nobody holds — locked out of its own plugin, silently.
  Two of the three never removed the capability on uninstall either. Fixed
  2026-08-04 and now a `verify.py` rule.

  **The count is the lesson.** Seven plugins declare a `CAPABILITY` constant;
  only four *create* one. `install_plugins`, `activate_plugins` and
  `publish_posts` are core's and are nobody's to grant — an audit that counted
  declarations rather than `add_cap()` calls would have looked at the wrong
  seven and missed all three defects. **Ask which plugins create a thing, not
  which mention it.**

* **Capabilities do not mean the same thing on a network** (§7.2.2 has the
  table). Five plugins failed the first multisite run for this; in every case
  core was right and the test was wrong. Weakening a gate to make a test pass
  would have handed network-level power to every site administrator on every
  network — wp-dbmanager's Run SQL Query console being the worst case.

* **A one-sided capability test asserts nothing.** "A user without
  `manage_options` cannot reach the screen" passes with the plugin deactivated,
  because the page does not exist. STANDARDS 7.5 forbids the form; both
  navigation suites now assert an administrator *can* reach the same screen.

* **The harness can lie.** A test reaching the real `wp_send_json_error()` took
  the PHP process down mid-run **with status 0**, and `bin/test-all.sh` reported
  the plugin as passing when 46 tests had already errored. The script now
  requires PHPUnit to have printed a verdict and treats its absence as a
  failure — see §7.2.3. **Do not remove that check.**

* **Prefer a mechanical check to a spot-check.** A `verify.py` rule for §4.2
  immediately caught two plugins putting `add_settings_field()` on the wrong
  class — drift no human review would have seen. The `phpcs.xml` and `ci.yml`
  identity checks caught 13 plugins between them, and the
  `helper-metadata-testcase.php` check added 2026-08-03 closes the last
  templated file that had none. **Anything copied into nineteen repositories
  diverges unless something compares it.**

* **Watch for rules that cannot be satisfied.** §9's ban on inline suppressions
  was reversed twice before landing on: fix the code, put collection-wide sniffs
  in the shared ruleset, and require a reason on the residue.

* **Commit after every step.** Two sessions died mid-flight. The first, with no
  checkpoints, lost 18 plugins' work.

## Binding decisions from Lester's four asks

All four are implemented. The specifications are kept because they record
decisions that still bind anything built on top of them.

1. **#17 Settings naming.** `<Name> Settings` on all 14 settings screens.
2. **#18 wp-print + wp-email link settings.** The four-way style select and both
   `post_text`/`page_text` fields are gone; only the custom HTML template
   remains, with `%POST_TYPE%` resolving to the post type's singular label. The
   migration synthesises the template from the old style *and* text, collapsing
   to `%POST_TYPE%` only when the two texts are the stock pair — otherwise it
   keeps post_text verbatim and the Upgrade Notice says the page wording is
   lost. **One template cannot express two arbitrary strings.**
3. **#19 wp-postviews Display Options.** The six-context matrix is gone, but
   `WP_PostViews_Display::should_be_displayed()` still answers a
   `wp_postviews_should_display` filter. The 2.0.0 Upgrade Notice names that
   method as the documented replacement for the old global, so removing it
   outright would break a promise in the release about to ship.
4. **#20 Proxy header.** Five plugins have one, all now on wp-polls' canonical
   label "Header That Contains The IP:" and three-part description.

## History

Kept short on purpose; the detail is in git.

* **2026-07-28** — spec written, 19 agents run one per plugin. All but
  freemyinternet were stopped before committing and **reset clean on 2026-07-29**
  rather than salvaged: those trees were built against two rules that had since
  changed, and a half-applied rename looks clean to every tool we have.
* **2026-07-30** — fan-out complete. All 19 pass `verify.py` (961 failures → 0).
  PHPUnit run for the first time, single site then multisite. Five real
  behavioural bugs found and fixed, the most user-visible being
  wp-downloadmanager's Add File ignoring its own source radio.
* **2026-08-01** — root folder became a git repository. Playwright suites
  written for all 19.
* **2026-08-02** — full E2E sweep, 826/867. Fifteen plugin bugs found, all since
  fixed; two release blockers (wp-print, wp-pluginsused migrations discarding
  the settings of the commonest released install); both §13.2 shared-row
  violations. The full 1,078-line report was deleted on 2026-08-03 once every
  bug in it was fixed — its four recurring *test* defects are folded into the
  E2E lessons above, and the per-plugin run log is in git.
* **2026-08-03** — CI reconciled with local for the first time (the permalink
  divergence above); assertion messages taken to 7,860 of 7,860; the metadata
  fixture held to its template; two tests that could not fail replaced. Then the
  nineteen pre-revamp tags were cut and pushed, and `_standards/` was cut from
  eight files to four: `BRIEFS.md`, `SNAPSHOT.md`, `E2E-SWEEP-2026-08-02.md` and
  `E2E-RERUN-2026-08-02.txt` all described work that had finished, and three of
  the four had drifted into saying things that were no longer true. **A document
  that records a migration becomes wrong the moment the migration lands** —
  BRIEFS still instructed an agent to create wp-relativedate's options row, which
  has existed since 2026-07-30. What was worth keeping was extracted first.

* **2026-08-04** — the §7.6.1 release blocker closed: wp-dbmanager fixed, a
  `verify.py` rule behind it, wp-polls hardened, both misleading comments
  corrected. Items 1(a), 1(b), 1(e), 1(f). Two claims in this file were found
  wrong while acting on them, which is the day's real output: §7.6.1's write
  half is handled by core, so wp-polls was never losing data; and the
  wp-pluginsused comment about a failing assertion was three fixes out of date.
  **Both were found by running the thing rather than reading it** — a mutation
  test on `save()`, and the E2E suite the comment was attached to. A third test
  was written, discovered to pass with the fix reverted, and deleted rather than
  committed. Item 8 added at Lester's request and deferred by his call.

* **2026-08-05** — item 1 closed. All eleven remaining migration suites written,
  run to green and committed, 78 tests in all, so every one of the fifteen
  migrating plugins now has a browser test of its migration. Three findings came
  out of running them, all now in the E2E lessons and none of them producible by
  reading: **a `wp eval` call is a full WordPress request**, so for the five
  plugins that migrate on `plugins_loaded` or `init` the fixture cannot be seeded
  in one call and read in another — the second call has already done the upgrade;
  **a scalar legacy row reads back as a string**, so an assertion on an integer
  is an assertion about no install that exists; and **wp-downloadmanager's legacy
  row wins over an existing current row**, which is the opposite of what the test
  assumed and what the code means.

  Four suites failed on their first run and were fixed. wp-commentnavi's and
  wp-pagenavi's were additionally confirmed by mutation, run separately rather
  than one assumed from the other, and three of seven tests went red in each.

  **Wall clock was the whole cost**: the same six-test suite takes two minutes on
  an idle machine and over an hour with an editor and a dozen wp-env stacks up,
  because almost all of it is `npx --yes @wordpress/env run` startup rather than
  browser time. Two runs were abandoned as hangs before that was understood.

* **2026-08-04** — the §7.6.1 release blocker closed, the spec-against-checks
  audit finished, and a capability audit found by it. `verify.py` 93 checks to
  127; 31 of 48 sections enforced to 41. Six spec sections corrected, four live
  defects fixed, three plugins' capability grants repaired. §13.3's naming
  reversed by Lester, deleting a breaking change the campaign had invented.
  wp-sweep's screen grouped under headings.

  **Three claims in this file were found wrong while acting on them, and that
  is the day's real output.** §7.6.1's write half is handled by core, so
  wp-polls was never losing data. The wp-pluginsused comment about a failing
  assertion was three fixes out of date. And two plugins with byte-identical
  migrations behave differently under the same mutation, because one sanitiser
  is idempotent on the defaults and the other is not. **All three were found by
  running the thing rather than reading it** — a mutation test, an E2E suite,
  and the same mutation run twice. A fourth test was written, discovered to pass
  with the fix reverted, and deleted rather than committed.

  This file was cut from 1,052 lines to its current length the same day: the
  finished items became a findings list, and "read the diffs for voice" was
  dropped as a task nobody could pick up while its measurements were kept.

The programme found roughly **twenty-five spec bugs and eleven `verify.py`
bugs**, every one because an agent pushed back rather than complied. The pattern
that made it work: one plugin finds it, fix it centrally, the other eighteen
never see it.
