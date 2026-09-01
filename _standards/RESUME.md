# Resume here

State of the consistency programme as of **2026-09-02**. Read this, then
`_standards/STANDARDS.md`, which is the contract everything else follows.

**In one line: the campaign is finished.** All nineteen plugins were released
to wordpress.org on 2026-08-09/10, every one tagged at its README's version,
serving roughly 880,000 active installs between them, and **no campaign item
is open**.
What the release itself found is under "Closed before 2026-08-24", and it is
the campaign's thesis proving itself one last time.

**Fifteen patch releases have been staged after the campaign, and all fifteen
are now released.** Nothing is staged. **The list lives in `bin/verify.py`'s
SHIPS_AS and §14's table; count from those, never from prose here** (this
paragraph has been wrong four times). Released 2026-08-24: freemyinternet 1.0.1,
wp-pluginsused, wp-downloadmanager, wp-draftsforfriends, wp-postviews and
wp-sweep 2.0.1, wp-useronline 4.0.1. Released 2026-08-28: wp-polls and
wp-pagenavi 3.0.1. Released 2026-08-29: wp-postratings 2.0.1. Released
2026-09-02: wp-useronline 4.0.2, wp-polls 3.0.2, wp-postratings 2.0.2,
wp-stats 3.0.1, wp-draftsforfriends 2.0.2 — write-ups under the dated entries
below and in each README's changelog. When Lester says ship, the
`release-wp-plugin` skill is the path. Nothing else waits on any of them.

**SHIPS_AS does not move on a release.** It records the version a repo intends
to ship, so it was already right for all seven before they went out and is
still right after. What goes stale on a release is prose like this paragraph
and §14's table — which is the whole reason the sentence above says to count
from the machine-readable half.

**All nineteen read `Tested up to: 7.1` in git, and the eleven released across
2026-08-24 to 2026-09-02 now say so on wordpress.org; the other eight still
show 7.0** — wp-ban, wp-commentnavi, wp-dbmanager, wp-email, wp-print,
wp-relativedate, wp-serverinfo and wp-showhide. That count is derived from
`svn cat .../trunk/readme.txt` per slug, not from adding up releases: four of
the five shipped on 2026-09-02 were already in the earlier ten, so the number
moved by one, not by five.
WordPress 7.1 became the current release and the readme header
was bumped across the set on 2026-08-20, together with the value `bin/verify.py`
checks for and the §3.2 template, so a plugin still reading 7.0 now fails
verification. Lester's call is that it rides along with each plugin's next
release rather than justifying nineteen releases for a metadata line — so the
remaining eight go on showing 7.0 until then, and there the compatibility line
is the stale one, not the git one.

**7.1 moved more than the version number: it moved the list table primary
column, and that turned wp-dbmanager red on 2026-08-20.** A sorting test read
`td.column-name` and core had moved that cell into a `th scope="row"`. Fixed,
green, and the whole collection swept — nothing any plugin *ships* was
affected. It leaves two open questions, both about CI rather than about any
plugin: whether the end-to-end job should pin a WordPress version instead of
following `latest`, and whether `Start wp-env` should retry. Both are listed as
open at the head of "Closed before 2026-08-24".

**Before writing another migration test, read the §7.6.1 entry under "Rules
earned the hard way"** — advice the release sharpened rather than dated: the
write half turned out to be missing its guard in six plugins after all, held
off by hook order and an imperfect sanitiser rather than by anything anyone
wrote. The read half is still the real defect, and the eleven migration
suites are all built on it.

**The campaign's core lesson: a rule nothing checks is a rule that is probably
also wrong**, not merely unenforced. It held to the last day: §7.6.2's write
guard was stated with wp-print as the reference, nothing enforced it, and six
of nineteen plugins did not carry it — found on release day by asking what
enforces the rule, never by re-reading the plugins.

**Trust the tools over this file.** At the start of a session run
`python3 bin/verify.py --quiet`, then in each repo `git fetch` followed by
`git status -sb` and `git log --oneline -3`. Between them they tell you the
true state without believing a word written here. **The `git fetch` is not
optional** — a cloud session pushes to the remote, and until you fetch,
`git status` reports a stale checkout as clean and level. And for anything
about what is *released*, ask wordpress.org rather than any local checkout:
`https://api.wordpress.org/plugins/info/1.2/` per slug, or the comparison loop
at the end of the `release-wp-plugin` skill for the whole set in one pass.

## What this is

Bringing all 19 plugins in this folder to a single written standard, so they
read as though one person wrote them on the same afternoon. The only permitted
differences between two plugins are name, features and capability.

## Decisions already made — do not re-litigate

| Question | Decision |
|---|---|
| Public identifier renames | Full canonicalisation **with** migration — shipped in the 2026-08 majors. The migrations stay live for sites upgrading from pre-revamp versions. |
| Class naming | Prefix everything: `WP_Email_Admin`, `WP_Print_Admin`. `freemyinternet` keeps `FreeMyInternet_*`. |
| CI matrix | **6 PHPUnit rows — every supported stack in both modes:** WP 6.8/PHP 8.2, WP latest/PHP 8.2, WP latest/PHP 8.5, each single **and** multisite. Plus phpcs and JS jobs, so 8 checks on a JS plugin and 7 without. Multisite runs on the floor too: that is where it breaks. |
| Admin UI | Full Settings API rewrite everywhere, one menu rule (§4.1), `WP_List_Table` for all tabular screens. |
| Renamed hooks that were public in the last SVN release | **Dropped outright.** No `apply_filters_deprecated()` shims. Every one documented under `## Upgrade Notice`. |
| Versioning | The campaign was folded into one major per plugin, released 2026-08-09/10 — wp-dbmanager and wp-useronline skipped a number, see §14. Post-release work gets its own version, staged first in `verify.py`'s `SHIPS_AS`. |
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

* `_standards/STANDARDS.md` — the spec. **15 numbered sections, 58 including
  subsections** (this line said 17 until 2026-08-03 and 48 until 2026-08-07, and
  nothing had counted either time). Recount rather than trust it:
  `grep -oE '^#{2,4} [0-9]+(\.[0-9]+)*' _standards/STANDARDS.md | wc -l` — and
  note the `#{2,4}`, because §7.6.1 is the one heading four levels deep and a
  `#{2,3}` pattern silently drops it. The jump from 48 to 58 is §13.4 and its
  nine subsections; see "Is the collection compliant?".
* `_standards/templates/` — the files each plugin copies verbatim, placeholders
  `{{SLUG}}` `{{NAME}}` `{{CLASS}}` `{{UNDER}}` `{{UPPER}}` `{{L10N}}`
  `{{DESCRIPTION}}`.
* `.wp-env.json` — all 19 plugins in one WordPress on 8888/8889.
* `bin/verify.py` — mechanical checker, not every check applying to every
  plugin. `python3 bin/verify.py [slug…] [--quiet]`; exit status is the failure
  count. Count the checks with `grep -c '\.check(' bin/verify.py` rather than
  trusting a number written here — three numbers this file has carried for it
  were each stale within days.
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

## Current state — last verified end to end 2026-09-02

**All nineteen are released, green on CI at their current `HEAD`, and level
with their remotes; nothing is staged.** The twentieth repository, this one, is
level too.

**Every claim in this section moves with the next commit — re-run rather than
quote.** This file has been wrong about exactly that before: wp-sweep was one
commit behind `origin/master` while a line here claimed all twenty level,
because a cloud session had pushed and nothing local had fetched —
**`git status` says nothing about a remote being ahead without a `git fetch`
first**, which is why the start-of-session check at the top has one. CI is the
authority; `gh run list` per repo takes a minute, and the release state comes
from `api.wordpress.org`, never from a local SVN checkout.

**A green CI sweep does not survive the next push**, and a sweep is not a
sample. Check the runs against `git rev-parse HEAD` per repository rather than
inferring from the last push, and remember that **a cancelled run is not a
failed one** — pushing twice in quick succession cancels the first by design
(see Traps).

What holds as of the last full check:

* `bin/test-all.sh` and `bin/test-all.sh --multisite` report all 19 plugin
  suites passing; `verify.py` is 0; phpcs and eslint are clean.
* **Every assertion in the collection carries a failure message.**
  `python3 bin/measure_assertions.py /path/to/plugins/*` re-derives the ratio.
* **Twelve blocks in eight plugins**, all built and shipped from `src/` through
  `build/`. PHPUnit's six-row matrix runs in CI on every push and is green
  everywhere.
* Playwright is green on every `upgrade.spec.js`, but the whole-file runs are
  the stalest claim here — re-check those first. The permalink audit of the E2E
  suites is complete.
* **No known plugin bug is outstanding that is not already fixed in git.**

## Closed 2026-09-02 — five staged patches released, and the live-site step waived

wp-useronline 4.0.2, wp-polls 3.0.2, wp-postratings 2.0.2, wp-stats 3.0.1 and
wp-draftsforfriends 2.0.2 went out, least-changed first, in that order. Four of
the five carry one change: §2.7.1's rule that an asset gate which *guesses*
must expose a filter to be overruled. wp-polls had grown
`wp_polls_needs_assets` for a poll rendered where the head scan cannot see it;
wp-postratings, wp-stats and wp-useronline guessed the same way with no escape
hatch, and for the latter two a miss was permanent because neither has a second
pass. wp-useronline also renamed its gate and two public template methods from
singular to plural, following §2.7.2. wp-draftsforfriends is unrelated — a meta
box that creates a share link with a button rather than a checkbox, and twenty
times the diff of any of the others.

**Lester waived the deploy to lesterchan.net for all five**, on the grounds
that they are bug fixes and the live site takes the released version from the
directory anyway. That is the second time the step has been skipped for a
batch — seven went the same way on 2026-08-24 — and it is worth being precise
about what the two waivers have in common, because the step's own write-up
argues for it in absolute terms. Both were batches of small, same-shaped
changes to plugins already running on the site. The step earns its place on a
rewrite, where what it catches is a screen that renders wrong rather than code
that is wrong; the failures it has actually caught were all of that kind. The
standing instruction is unchanged, and so is the reason wp-showhide sat two
weeks behind: skipping the deploy is safe **because** the site updates itself
from wordpress.org, which is exactly the fact that made the gap invisible when
it was skipped and the release then failed.

Nothing else was notable, which is itself the point: pre-flight green on all
five, CI green on the exact commit shipped, every tag free, `assets/` needing
no change in any of them — caption counts already matched file counts, so for
the first time in these releases there were no orphaned screenshots to remove.
The staged `svn stat` for each was modifications only: no adds, no deletes, no
unversioned entries. Trunk r3676711–r3676724.

**`build/` did not move in any of the four block plugins**, and that is
correct rather than a failed build. The filters are PHP-side; the compiled
editor bundles are built from `src/` and were unchanged. It is worth writing
down because a `svn stat` with no `build/` line in a block plugin looks exactly
like a build that never ran, and the check that tells them apart is
`svn ls <trunk URL>/build` after the commit, not the stat before it.

## Closed 2026-08-29 — wp-postratings 2.0.1 released, and the last of the ten

**wp-postratings 2.0.1** (trunk r3670662, tag r3670663) closes the set: all ten
patches staged after the campaign are live, and nothing is staged. The live-site
step was skipped again, so lesterchan.net is behind on all ten. It shipped eight
commits; what the three interesting ones taught is written up under the
2026-08-28 entry below, and the durable halves are in "Rules earned the hard
way" and "Tests that cannot fail".

## Closed 2026-08-28 — wp-polls and wp-pagenavi released; three defects found on the way

Two of the three remaining staged patches went out: **wp-polls 3.0.1** (trunk
r3670406, tag r3670407) and **wp-pagenavi 3.0.1** (trunk r3670430, tag
r3670431). The live-site step was skipped again, at Lester's instruction.

**The pre-flight is not the only gate worth running.** wp-polls passed all 31
checks, `verify.py` and CI, and the release still stopped: 3.0.1 moves the
upgrade to `init`, which is the change that had just produced a real defect in
wp-downloadmanager, so the same shape was worth reading before publishing rather
than after. Trunk was staged, then reverted, and the release went out an hour
later with a lock in it. Nothing had been published, which is the whole point of
4e existing as a stop.

**Which plugins actually need the lock.** A sweep of all nineteen for
non-idempotent work in a migration path found three: wp-downloadmanager (the
`file_category + 1` shift and the permission rotation in `upgrade_pre_150()`),
wp-postratings (`maybe_add_indexes()` reads `SHOW INDEX` then `ALTER`s, on every
front-end request until the markers move — two requests both issue it, and the
second sits on the metadata lock for the length of the first), and wp-polls,
whose schema work is reached only from activation so its lock is defensive. The
other sixteen have no table writes in migration code. All three implementations
are byte-identical, and their tests were brought to parity. wp-polls' own lock
was **justified wrongly at first** — see "Quantify before describing a
consequence" under "Rules earned the hard way"; what it buys is that the work is
not done twice, not protection from a lost update.

**wp-postratings picked up three defects while it sat staged**, all found by
looking rather than by a suite:

* the numbers shape drew its box two ways — sides as a border on the container,
  top and bottom as inset shadows on the bar inside it. Same colour, but the
  sides fell on the page background and the top and bottom on the bar's own
  tint, so they rendered at roughly four times each other's contrast. One
  outline now draws all four.
* one refusal template served three reasons, so a site on **Guests Only**
  refused a logged-in member and then told them to become a registered member.
  `%RATINGS_PERMISSION%` gives each reason its own sentence — **and the fix
  reached nobody**, which is the durable half and is under "Rules earned the
  hard way".
* a ten-point numeric scale's cells were not equal width, and the test that
  claimed they were could only pass on CI's fonts — under "Tests that cannot
  fail", with the e2e test that never read the message it was named for.

**Two stale assertions, and the more useful one passed.** Replacing the refusal
sentence turned `tests/e2e/voting.spec.js` red — a string pinned in the e2e tree
after I had swept `tests/*.php`, exactly the miss CLAUDE.md warns about. The
instructive one is the test that stayed green, and it is under "Tests that
cannot fail".

**Mutation testing earned its place twice here.** It killed two guards in
`adopt_permission_token()` that no assertion could distinguish — `str_replace`
is a no-op when its needle is absent, so the outcome is identical with or
without them. What the surviving guard buys is one avoided write of the settings
row, so the test counts writes instead of asserting on a value that does not
change.

## Closed 2026-08-24 — seven of the ten staged patches released, one re-tagged

Released in this order, chosen by size of diff rather than by importance so the
smallest change was the first thing to go through the procedure that day:
freemyinternet 1.0.1, wp-pluginsused 2.0.1, wp-downloadmanager 2.0.1,
wp-draftsforfriends 2.0.1, wp-useronline 4.0.1, wp-sweep 2.0.1,
wp-postviews 2.0.1. Still staged: wp-pagenavi 3.0.1, wp-postratings 2.0.1,
wp-polls 3.0.1.

**The live-site step was skipped, at Lester's instruction.** Every one of the
seven went straight from staged trunk to `svn ci` without the deploy to
lesterchan.net, so the site is behind on all seven and none of them was
exercised against real data before publication. That is a deliberate departure
from the release skill's standing "live site always", not an oversight — but it
is also why the defect below was found by reading the migration rather than by
running it.

### wp-downloadmanager 2.0.1 was re-tagged the same day

The category migration it shipped renumbers every category up by one and adds
one to every row's `file_category` to match. Two ways that could go wrong, both
found by asking what happens when the request dies, after it was already
public:

* **The two writes were ordered option-first, table-second, and the guard is
  the option.** A request dying between them left a list one ahead of its rows,
  and the next request saw an empty slot 0 — indistinguishable from an install
  that never needed shifting — and returned early. Every file would read its
  neighbour's category for good, with nothing able to detect it. The docblock
  argued that order was the safe one; it is safe against a double shift and
  unsafe against a half one, and nothing said so.
* **Nothing held a lock, and 2.0.1 moved the upgrade to `init`.** On
  `admin_init` two concurrent runs took two open admin tabs; on `init` any two
  visitors will do, and both would add their own 1 to every row.

Fixed by putting `wp_downloadmanager_category_shift_pending` between the two
writes so an interrupted run is resumed rather than lost, and by taking a lock
before the upgrade does anything. **The lock is an `add_option()` row, not
`wp_cache_add()`** — with no persistent object cache `wp_cache_add()` succeeds
in every request, which is precisely the site that needs protecting, whereas
the unique key on `option_name` makes the INSERT fail for the second caller.
An abandoned lock times out rather than stranding the site on the old schema.

**Lester's call was to re-tag 2.0.1 rather than ship 2.0.2**, on the grounds
that the directory takes about a day to propagate so almost nobody could have
the first cut, and for anyone who did the migration had already run. Recorded
in §14 as the exception it is: a re-tag leaves whoever downloaded the first cut
holding different bytes under the same version for ever, and is not the
default.

Both new guards were mutation-tested rather than assumed: removing the lock
fails one new test and restoring the old early-return fails the other, so
neither is a test that cannot fail.

### What the release procedure itself got right

Nothing else needed touching. Every one of the seven had a clean pre-flight,
`verify.py` 0, CI green on the exact shipped SHA, and `assets/` already correct
— no screenshot to add, none orphaned, every caption matching. The two plugins
with a new shipped file (wp-draftsforfriends' meta box, wp-postviews' bootstrap
class) needed the `svn add` the procedure's "read the `?` list before adding
it" step exists for, and nothing else appeared in either list.

## Closed before 2026-08-24 — the findings, not the log

Everything from the spec being written on 2026-07-28 to the last patch staged
before the first post-campaign release. **The instructions are spent; the
blow-by-blow is in git and in each plugin's changelog.** What is kept here is
what still binds work not yet done — and the durable lessons have already been
promoted into "Rules earned the hard way", "Tests that cannot fail", "E2E
lessons" and "Traps" below, which is where to read them rather than here.

**Three things on this list are still open.** They are the only reason to read
past this paragraph:

* **`verify.py` does not check that a store-nothing plugin refrains from
  *claiming* a row.** `STORES_NOTHING` names the four and asserts they define
  no `DB_VERSION`; three false statements about a `{{UNDER}}_version` row still
  survived a sweep aimed at them, in a plugin header, a comment and an
  uninstall docblock. Two mechanical rules would close it: for a slug in
  `STORES_NOTHING`, `wp_<under>_version` may appear only in `uninstall.php` and
  `tests/`; and a plugin may not name a `WP_<Prefix>_*` class no file declares
  — which also catches the two dead class pointers found beside them
  (`WP_ServerInfo_Options`, `WP_Sweep_Options`, both required by tests *not* to
  exist).
* **No `verify.py` rule for "every `widget()` parses its instance against
  defaults"**, though it is mechanical and there are seven copies. wp-polls'
  widget read three `$instance` keys with no defaults and no guard, printing
  `Warning: Undefined array key` into the rendered page; five of the seven
  parse against defaults and wp-useronline guards every read, so wp-polls was
  the only one of seven doing neither. Found by looking at a screenshot of the
  widget, not by any suite. The fix is a `defaults()` method read by **both**
  `widget()` and `form()`, so the two cannot disagree about an unset key.
* **The end-to-end job follows WordPress `latest` and nothing pins it**, and
  `Start wp-env` has no retry. `.wp-env.json` carries `"core": null` where the
  PHPUnit matrix sets `WP_ENV_CORE` per row, which is why WordPress 7.1 turned
  wp-dbmanager red with no commit behind it. Left open deliberately: pinning
  makes the job reproducible, not pinning is what caught a real compatibility
  break on the day it shipped, and a pinned row plus a `latest` row buys both
  for one more job. The retry question came from **three upstream download
  failures in eighty minutes** across two plugins — the composer installer and
  an HTTP 504 from api.github.com. Either change is all nineteen workflows or
  none.

### What the passes found, in one line each

* **The consistency campaign, 2026-08-21 → 23** — eight alternating audit and
  fix passes took the collection from "released and green" to "converged and
  proven". **The rules it produced are §2.7.1 (differences that must not be
  flattened) and §2.7.2 (the method-name canon) — read those, not this.** The
  yield: a `run_uninstall()` helper degrading to single-site on its second call
  in seven suites; wp-useronline's uninstall path executed by nothing; eight
  spellings of the test loader; a ninth untyped `set_options()`; READMEs
  describing pre-rename screens; four CLAUDE.md standalone-rule breaks; three
  performance findings (postratings' unbounded `loop_start` query, useronline's
  unindexed per-request scans, unconditional site-wide assets in
  polls/postratings); then eleven feature matrices, 42 convergence items and
  ~46 themed commits. The closing pass diffed every frozen surface byte-for-byte
  against all nineteen released wordpress.org zips: identical.
* **Two bootstraps upgraded only one site of a network** (wp-pagenavi,
  wp-pluginsused): `activate()` took no `$network_wide` and ran against
  whichever site was current, where wp-commentnavi — the same file in the same
  shape — loops `get_sites( number => 0 )`. Low severity only because the same
  routine is also on `admin_init`, so every site healed the moment somebody
  opened its dashboard, and **a bug that repairs itself under every hand-check
  is invisible to hand-checking** — that is the shape to look for. Nothing
  tested the loop on any of the three, including the one that had it;
  `tests/test-multisite.php` now does, reading the uncapped `get_sites()` off
  `pre_get_sites` rather than building a 101-site fixture.
* **wp-useronline linked every IPv6 visitor to a whois that cannot read one.**
  The reporter named three replacement services and **only one survives being
  checked** — who.is redirects to its own search form, ip-api.com takes the
  address in a fragment — while all three answer HTTP 200 while dropping the
  address on the floor. Ten minutes of `curl` before committing to a default.
  Shape worth copying: an **empty** filter return drops the link rather than
  emitting `href=""`, because the obvious filter-then-print shape turns "do not
  hand a visitor's address to a third party" into a link to the current page.
  And **adding a filter is a patch; renaming one is not** — the metadata test
  now pins the major rather than the literal version.
* **§14's table was a fourth unchecked copy of the version.** It said `2.0.0`
  for wp-postratings while the prose and `SHIPS_AS` both said 2.0.1, because
  nothing read the table. `verify.py` now compares the two. The number lives in
  four places with three checked against the fourth, which is the most this
  shape allows.
* **A readme sweep turned three suites red** — eighteen jobs, on one stale
  string each: `upgrade_notice_subjects()` still listed `wp_<slug>_version`
  while the same class declared `has_version_row()` false. Removing the entry
  removed no coverage, because the shared version-row test pins the absence by
  behaviour — checked before deleting, since a list entry that looks obsolete is
  exactly what a real assertion looks like from the outside.
* **wp-downloadmanager's two admin screens disagreed** about a file in no
  category — "N/A" on one, nothing on the other, one click apart. The label is
  now a parameter on `category_name()`, so the choice sits at each call site,
  and three callers deliberately pass nothing. The part that would have been got
  wrong: the lookup had to stop distinguishing *absent* from *blank*, because
  category 0 is present and blank by design.
* **`register_setting()`'s callback is also called with the stored array.**
  wp-downloadmanager's `sanitize_categories()` handled only the textarea's
  string form, so every whole-row write collapsed the category list to one
  blank entry — including the upgrade routine's own write. Being wrong is also
  what altered the defaults and gave `update_option()` a difference to find, so
  §7.6.2's write guard alone would have written the blanked list.
* **Seventeen changelog lines said "up from 6.0 and 7.4".** §14.1 forbids
  naming the floors a reader upgraded from — the numbers describe the
  pre-revamp *repositories*, not anything a real site declared, and fifteen of
  nineteen released readmes declare no `Requires PHP` at all. The rule had been
  applied to every Upgrade Notice and never to the `BREAKING:` lines, and
  nothing checked it. `verify.py` now fails any README containing `, up from `.
* **The blocks phase broke the metadata fixture two ways, and the green
  plugins were the finding.** The fixture read `wp_scripts()->registered`, a
  process-wide global three plugins' own `set_up()` methods null or replace, so
  the loop ran against nothing and passed — **wp-polls shipped a block through
  six green PHPUnit rows on the identical dependency array that failed
  wp-postratings**. The block half is read off the `build/*/*.asset.php`
  manifest now. Separately, firing `init` twice re-registers the blocks, which
  is a `_doing_it_wrong()` and so a failure; the guard is deliberately in
  `fire_init()` and **not** in the plugin, because a second registration in
  production would be a real bug and a guard would swallow it. §6 and §7.2.1
  carry the reasoning.
* **The README audit, read as somebody installing the plugin.** Correctness is
  mechanical now — §3.3 in `verify.py` splits every backticked admin path on
  its arrows and checks each segment against the strings the plugin renders,
  reading JS and `_x()` as well as PHP. It found wp-polls sending readers
  through three wrong labels in one sentence and wp-postratings answering an
  FAQ with a **Ratings Colour** setting that has never existed, both survivors
  of a whole major revamp. **The check and the read find different things and
  neither substitutes for the other**: the mechanical pass cannot tell that a
  description says nothing; the read would never have caught a confident
  sentence about a plausible setting. `## Installation` is required of all
  nineteen — Lester's call, because wordpress.org renders it as a tab and a
  missing tab reads as an omission; the move exposed setup steps hiding in
  `## Usage` in five plugins, wp-dbmanager's "secure the backup folder" among
  them. Checked rather than assumed: wordpress.org's parser handles `##`
  headings, so the deploy does not need to convert them.
* **The screenshots: 71 images, and seven captions were wrong** — miscounts,
  the wrong tab, and worst, **controls that exist nowhere**, the class that
  costs a user real time because they install expecting a setting no screen
  offers. The method that worked: read the sentence, then check any claim it
  makes against the code (`grep -c add_settings_field` settled three in
  seconds). Two findings outlast the images — **count-matches-README is not
  coverage** (it passes on any number, including one too small), and **a
  subagent's account of its own work is not evidence**: one reported a git fix
  as blocked when the reflog showed it had succeeded, and following its
  instructions would have duplicated a commit. Check the repository, not the
  report.
* **The WP-CLI, REST and blocks phase.** Twelve blocks in eight plugins; scope,
  naming and the three deliberately unclaimed names live in §13.3–§13.4.
  **Read §13.4.10's last paragraph before the next phase of anything**: every
  one of the seven followers deviated from wp-polls somewhere and every
  deviation was right — wp-useronline correctly refused wp-polls' "block and
  shortcode on one page" test, which would have **passed** while asserting a
  duplicate DOM id. What binds new work on these surfaces: a refusal answers
  **403, not 400** (§13.4.6a); **how an AJAX handler reports its outcome decides
  how hard REST is** — answer JSON or throw and it ports, return-or-echo a
  string and it does not, and a refusal that deliberately says nothing to a
  visitor throws with an **empty** message so the browser path is unchanged;
  **wp-useronline is the one to read before writing the next command**, because
  consistency pressure would have produced both of its mistakes (it takes no
  nonce and must not, since anonymous nonces come from one session every
  logged-out caller shares, and it reads and never writes — two tests pin each
  *absence*); and **the `admin-ajax.php` actions stayed registered** per
  §13.4.2, each route added beside its action rather than in place of it.
  **A second entry point surfaces old bugs** — wp-downloadmanager's shortcode
  compared `0 !== $id` strictly against what `shortcode_atts()` returns, and
  wp-stats gated its stylesheet on `has_shortcode()` alone, so a block-only page
  loaded no CSS.
* **The security review — twenty-seven findings, all fixed, all with tests.**
  The three things asked about specifically were in good shape: all 160 `$wpdb`
  call sites resolve to bound parameters, table-name properties, integer casts
  or real allow-lists; nothing calls `wp_set_auth_cookie`, `wp_signon` or
  `wp_update_user`; escaping was consistently right. What it found was **trust
  boundaries drawn one level too generously**. Eight further items turned up
  while closing the hardening tier, including three term sweeps **deleting data
  that was in use** — a data-loss bug rather than a security one. Every new
  guard was mutation-tested, which caught four tests of mine that could not
  fail; **write the mutation step into any security fix from the start.**

  **Which plugin each finding belonged to is deliberately not written down
  here, and the collated write-up is not in this repository — ask Lester.**
  Every one is fixed and released and each changelog describes its own fixes,
  so nothing is hidden; what is withheld is the *collation*, because an index
  pairing a plugin with the flaw its previous release carried does the sorting
  work for somebody targeting the installs that have not updated yet, and
  install counts mean that is most of them for weeks after a release. **Keep it
  that way when adding to this section.**
* **The i18n sweep — 2,104 strings, zero `wp i18n make-pot` warnings.** That
  extractor run is the check worth repeating; it is ground truth for malformed
  placeholders, wrong domains and conflicting translator comments in a way no
  grep is. The classes found: two strings never translated at all; **seven
  padded into uselessness**, because a translator sees a msgid in a list where
  a leading or trailing space is invisible; four sentences assembled from
  fragments a translator cannot reorder; thirty-seven translator comments that
  said nothing (`translators: %s: value.` satisfies the sniff, which only checks
  a comment exists); nine bare words with no context; and one locale-blind
  number. **Only the padding class is pinned by a test**
  (`test_no_translatable_string_carries_edge_whitespace()` in the shared
  metadata fixture) — the rest were found by reading and a new one would need
  the same. Two things are left alone on purpose: the quicktag's
  `l10n.label || 'Download'` fallback shows only in a state where nothing else
  on the screen works, and `Domain Path: /languages` is inert — nothing calls
  `load_plugin_textdomain()` and translations arrive from
  translate.wordpress.org — but §3.2 mandates it and a test asserts it.
* **The eleven migration suites.** All fifteen migrating plugins have a green
  `tests/e2e/upgrade.spec.js`. Their findings are in "E2E lessons" below; one
  more belongs here: **a blocking `execFileSync` inside a test cannot be
  interrupted by Playwright's timeout**, so a slow helper reads as a hang
  rather than a failure. Two runs were abandoned on that before machine load
  turned out to be the cause — the same suite took an hour under load and two
  minutes without it.
* **The spec-against-checks audit** took `verify.py` from 93 `check()` sites to
  127 and found **six spec sections simply wrong**. The capability audit fell
  out of it, and the §7.6.1 release blocker closed with it; both are under
  "Rules earned the hard way". **The audit worth doing is the spec against the
  checks, not the plugins against the spec** — that conclusion, and its current
  arithmetic, are under "Is the collection compliant?".
* **The pre-revamp tags.** All nineteen are tagged and pushed, so every plugin
  has a ref for "as it shipped before this work"; `git -C <plugin> tag` is the
  authority. Three findings outlived the tagging: **wp-email shipped with its
  header behind its `Stable tag`** at `066014a9` — 2.69.2 in the header against
  2.69.3 stable, so wordpress.org served that tree as 2.69.3 while every site
  running it reported 2.69.2, a standing update prompt that never clears, and it
  had happened once before at 2.69.0/2.69.1. **Five plugins carried
  `Stable tag: trunk`, not four**, which §14 had said for years. And **two
  repositories already carried tags while a draft here said none did** —
  wp-pagenavi six, wp-useronline four, from scribu's tenure — prose about a
  number nothing had measured.
* **One wp-stats browser test failed once and the reason is not known.**
  `page.spec.js`, *the General Stats block counts every kind of thing on the
  site*, failed in a full local run and passed on re-run and in CI; both
  reproduction attempts were contaminated by the two-suites-one-wp-env hazard
  under Traps. What was fixed is the reason it could not be diagnosed: every
  line in that block is pluralised with `_n_noop()` and the two arms share no
  substring, so four of six locators written against one arm matched **nothing**
  and Playwright reported a timeout waiting for an element. The patterns span
  both arms now, so the next occurrence prints the number.

### Three habits that came out of the passes and are not written elsewhere

* **A WP-CLI boot fires `init`**, so a migration fixture must seed and read back
  in **one** `wp eval` — the long form is in "E2E lessons".
* **An infinite recursion under the test runner reads as SIGKILL at a fixed
  percentage**, which looks like anything but recursion. `git stash` → green →
  `git stash pop` localises it in one run.
* **Sequenced string replaces can rewrite the text an earlier replace just
  inserted.** The wrapper-self-call bug shipped twice in one afternoon that way.
  Order the replaces so no output is an input, or do them in one pass.

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

* **Match a list table cell by its class, never by its element.** WordPress
  7.1 moved the primary column into a `th scope="row"`, so `td.column-name`
  finds nothing from 7.1 and `th.column-name` finds nothing before it, while
  `.column-name` reads both. The primary column is the first one that is not
  the checkbox — that is, whichever column names the row, which is the column
  a sorting test is most likely to read.
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
* **Playwright's `request` fixture is logged in as the administrator, and a
  "logged out" test that forgets it is testing the wrong person.**
  `playwright.config.js` sets `use.storageState` for the whole suite, and every
  fixture inherits it — `request` as much as `page`. A REST call made through it
  therefore carries the admin session cookie, which is invisible until something
  depends on *who* is asking.

  It cost a wrong diagnosis on 2026-08-08. wp-polls' anonymous-vote test minted
  the poll nonce through `wp eval`, which runs with nobody logged in, and posted
  it through `request`, which was user 1 — so `wp_verify_nonce()` refused it and
  the endpoint looked broken when the fixture was. **A nonce is tied to the user
  it was made for**, so both sides have to be the same person.

  The fix is a nested describe with
  `test.use( { storageState: { cookies: [], origins: [] } } )`, and — this is the
  part worth copying — **a test asserting the fixture really is logged out**,
  because `/wp/v2/users/me` answers 401 to a visitor and 200 to an
  administrator. Without it the anonymous test passes as the admin the day
  somebody changes the storage state, and a vote is not the thing that would
  tell you. Same family as "Tests that cannot fail" below.

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

* **You cannot mutation-test anything under `build/`, because the runner
  rebuilds it first.** `bin/test.sh` and `bin/test-e2e.sh` both run `bin/build`
  before they run anything — added so a suite cannot silently test a stale
  build. The cost is the mirror image: edit `build/showhide/index.asset.php` to
  prove an assertion bites, run `bin/test.sh --filter Metadata`, and the build
  regenerates the file before PHPUnit starts. **The suite passes, and it passes
  for a reason that has nothing to do with the code.**

  Seen on 2026-08-08 verifying that the new block dependency rule catches
  `jquery`. The first attempt came back green and the claim under test was
  nearly recorded as unproven. Injecting the same value and calling phpunit
  directly —

      npx @wordpress/env run tests-cli --env-cwd=wp-content/plugins/<slug> \
        vendor/bin/phpunit -c phpunit.xml.dist --filter Metadata

  — failed exactly as it should. **Mutate the source and rebuild, or bypass the
  runner; never mutate a build artefact and use the runner.** The same applies
  to anything else generated during a run.

* **A stand-in that records instead of doing cannot see what the real thing
  does with the recording.** The WP-CLI `format_items()` stand-in stores the
  rows it is handed so a test can assert on them without parsing
  column-aligned text — which is the right design, and it means **the formatter
  is the one thing the suite structurally cannot test**.

  Six commands advertised `--format=ids`, and all six passed rows of
  associative arrays to `format_items()`. Real WP-CLI hands `ids` straight to
  `implode()`, so every one of them printed the word `Array` once per row, with
  a PHP warning — and wp-polls' README documented
  `wp polls list --format=ids | xargs -n1 wp polls close`, a pipe built on it.
  Thirty-odd CLI tests were green the whole time, on data real WP-CLI would
  have mangled.

  Two agents inferred it from WP-CLI's source and both flagged it as something
  they could not check. **One `wp polls list --format=ids` in the wp-env
  container settled it in seconds**, which is the lesson: a stand-in is a model
  of the real thing, and the parts of the real thing it models away are exactly
  where the bugs live. `verify.py` has a rule now, but the rule was written
  *after* running it, not instead.

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

* **A test named for a behaviour that checks something weaker than the
  behaviour.** wp-postratings' `Guests Only shows a logged-in user the
  permission template` asserted only that the vote form was absent and never
  read the message, so it passed for the whole life of the bug, on precisely
  the case that was broken. **Worse than no test, because it is counted** — a
  name is what a later reader trusts instead of the body.

* **A test that passes only because a sanitiser is imperfect.** The §7.6.2
  migration tests that existed were green because `update_option()` sanitises
  before it compares, and kses collapsing a doubled space in one template
  default was what made the migrated value differ and the row get written.
  Removing the doubled space — a cosmetic fix — turned two plugins' migration
  tests red. Each of the six now asserts the shipped defaults are a fixed point
  of its own sanitiser, so the day that stops being true is reported.

* **An assertion CI's one platform structurally cannot break.**
  wp-postratings' `a ten point numeric scale keeps every cell the same width`
  asserted an invariant the stylesheet did not provide — the cell reserved its
  size as a *minimum* and grew for two-digit glyphs — so it passed on CI's
  fonts and failed on macOS. **CI runs one platform's fonts.** Make the
  invariant true by construction (equal grid columns) rather than measuring.

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

* **`svn log` on a working copy cannot see commits newer than that copy, so it is
  not evidence about wordpress.org.** It defaults to `BASE:0`. After an accidental
  deploy on 2026-08-08 a local `svn log -l 2 trunk` reported the newest revision as
  2022 and the conclusion drawn was "nothing was published". The URL told the truth
  immediately:

      svn log -l 2 http://plugins.svn.wordpress.org/<slug>/trunk
      svn ls        http://plugins.svn.wordpress.org/<slug>/trunk

  r3638607 had emptied wp-ban's trunk seven minutes earlier. **Ask the repository,
  not the checkout** — the same shape as the `git fetch` entry in Current state: a
  local view is a claim about your disk and nothing else.

* **The deploy script is retired, and the reason is the incident that retired
  it.** It did everything in one pass ending in `svn ci` — no
  dry run, no diff to read, no place to stop. It was invoked on 2026-08-08 to
  test an unrelated guard, piped through `head -4` in the belief that would stop
  it. It did not: SIGPIPE only kills the writer on its next write and the script
  had already finished. It emptied wp-ban's trunk on wordpress.org.

  Nothing was lost — `tags/1.69.2` was untouched, so downloads and updates kept
  working, and `svn merge -c -<rev>` restored trunk. What it cost was trust in a
  release path that could not be rehearsed. The work now lives in the
  `release-wp-plugin` skill as Step 4, inspectable commands with a hard stop at
  `svn stat` before the commit, and every one of the 2026-08-10 releases went
  through it. **A copy of that script still exists outside this repository —
  never run it, and do not reintroduce a one-pass deploy to the release path.**


* **The deploy rsyncs the working tree, not a clean export** — true of the old
  script and of the skill's Step 4c alike — so anything present on disk ships
  whether or not git tracks it. Three things were going to wordpress.org that
  should not have been, all fixed in the exclusion list on 2026-08-05:

  * `CLAUDE.md` and `AGENTS.md` — not dotfiles, so the `$SRC_DIR/*` glob did not
    skip them the way it skips `.claude/` and `.github/`;
  * **`artifacts/`** — Playwright's traces, failure screenshots and
    `storage-states/admin.json`, which is a logged-in WordPress session cookie
    for the local test container. It is in every plugin's `.gitignore`, which is
    exactly why nobody saw it: `git status` is silent about it and the deploy
    copies it anyway. All nineteen had one on disk. Running the browser suite
    once and deploying afterwards was enough to publish it.

  The plugin briefings were made standalone the same day for the same reason —
  no `_standards/` paths, no `§` citations, no dates, no claims about the
  collection — and that rule stands even now they are excluded, because anyone
  cloning a plugin from GitHub is in the same position. The four failure modes
  are in the root `CLAUDE.md`; **do not write a plugin file that assumes this
  checkout.**

  A fourth was added the same day from reasoning rather than from finding one on
  disk: **`.DS_Store`**. The `$SRC_DIR/*` glob skips dotfiles, but only at the
  top level — `--recursive` then copies everything *inside* the directories it
  matched, dotfiles included. So `./.DS_Store` never shipped and
  `includes/.DS_Store` always would have, and Finder writes those into any
  folder somebody opens.

  **The lesson is bigger than the four entries.** An exclusion list is a deny
  list, and a deny list acquires a new member every time the toolchain grows —
  which is the same trap §7.2.1 records for metadata tests scanning the plugin
  root. After changing anything about what lives in a plugin directory, dry-run
  the deploy's rsync into a scratch directory and read what comes out. Doing
  exactly that is what turned up all four.

  As of 2026-08-05 the audit is clean: across all nineteen, what ships is the
  main plugin file, `includes/`, `js/`, `css/`, `tinymce/`, `index.php`,
  `LICENSE`, `uninstall.php`, `README.md` (renamed to `readme.txt` by the
  script) and wp-dbmanager's two `.txt` payloads. Nothing else.

* **`--no-gpg-sign` does not cover a rebase.** These repositories are unsigned
  by decision and the global `commit.gpgsign` is true, so every commit here
  passes `--no-gpg-sign` — but a rebase makes its own commits and reads the
  config directly. `git rebase master` stops on the first pick with *"error: you
  have staged changes in your working tree"* and advises `git commit --amend
  '-S'`, which is the real message wearing a disguise: the `-S` is the tell, and
  the rebase has already decided to sign. It is not a conflict, and `git status`
  says as much — *all conflicts fixed*.

  Use `git -c commit.gpgsign=false rebase <base>`. The same applies to anything
  else that commits on your behalf: `cherry-pick`, `revert`, `merge --no-ff`,
  `commit --amend` inside a rebase. Seen 2026-08-08 rebasing wp-polls'
  `wp-cli-rest-blocks` onto master.

* **Never pipe a test run through `tail`, and this cost a diagnosis on
  2026-08-08.** Two things go wrong at once. The exit status you see is
  `tail`'s, so a suite that failed reports success — `bin/test-e2e.sh | tail -25`
  came back "exit code 0" on a run with **13 failures**. And the failure detail
  is thrown away: Playwright prints each failure's expected/received above the
  summary, so a 25-line tail keeps the list of test names and none of the
  reasons. Redirect to a file and read that.

  What was left of that run was: 13 failed, 17 never ran, 8 passed in 1.8
  minutes. **An immediate re-run with nothing changed passed 38 of 38 in 5.9
  minutes.** Two hypotheses were tested against it and both died — the tests
  database was not left as a network by the multisite suite, and PHPUnit had
  already reinstalled it single-site before the failing run — and by then
  Playwright's second run had cleared `artifacts/test-results/`, taking the
  traces with it. **The cause is unknown and now unknowable**, which is the
  whole point of the entry: the log was the only thing that could have said,
  and a pipe through `tail` destroyed it.

  **Three hypotheses have now been tested and all three are dead.** The tests
  database was not left as a network by the multisite suite; PHPUnit had already
  reinstalled it single-site before the failing run; and the one that sounded
  best — a stale `artifacts/storage-states/admin.json`, since PHPUnit rebuilds
  the database that saved session belongs to and all 13 failures were in specs
  needing the admin — **was tried deliberately on 2026-08-08 and did not
  reproduce**: the browser suite was run immediately after a PHPUnit run with
  that same stale file in place, and passed 38 of 38.

  So the honest state is **one unexplained red run against four green ones**,
  and the entry stays here as a flake to watch rather than a diagnosis. If it
  recurs: keep the log, and look at `17 did not run` first — Playwright abandoned
  that run in 1.8 minutes against 5.9 to 7.2 for a full pass, so whatever it was
  hit early and hit the harness rather than any one test.

* **A browser suite that fails from some point onward and never recovers was
  stomped, not broken — and the tell is in the tests environment afterwards.**
  wp-postviews on 2026-08-08: **57 passed, then 56 consecutive failures**, every
  one of them the same `Class "WP_PostViews_Options" not found` out of
  `wp eval` on `tests-cli`. Not a single pass after the cliff.

  The plugin's own classes being absent means the plugin was not active, and the
  post-mortem check settled which way: in the tests environment afterwards
  **wp-postviews was inactive and `twentytwentyone` was inactive too**. Those are
  precisely the two things `bin/test-e2e.sh` activates before it runs, and its
  own comment names the hazard — *"Running PHPUnit reinstalls this same
  database, which takes the plugin, the theme and the logged-in session with
  it."* A plugin alone could be a deactivation; **plugin and theme together is
  the database being reinstalled underneath a running suite.**

  What was *not* established is what ran PHPUnit — nothing of this session's was
  in flight. So this is a confirmed mechanism with an unproven trigger, and it
  is written down for the signature rather than the culprit. Note it is the same
  shape as the unexplained red run above, which sits three dead hypotheses deep;
  one of those was "PHPUnit reinstalls the database", tested as *before* the
  failing run and correctly rejected. **During** was never tested.

  Read the cliff before reading the failures. 56 failures is one event; a
  contiguous block with no pass after it is an environment that changed, and the
  useful evidence is in the container, not the log. Two checks settle it in
  seconds: `wp plugin list` and `wp theme list` against `tests-cli`.

* **The browser suites belong in CI, and this is why.** Every `ci.yml` already
  runs Playwright, PHPUnit across the WP/PHP matrix single and multisite, ESLint
  and the JS tests. CI gives each plugin its own runner and its own containers,
  so nothing can reinstall a database underneath anything else — which is the
  one failure mode local runs keep producing, twice now with a full diagnosis
  costing more than the run. Locally the suites must be run one plugin at a time
  and are still not safe; in CI nineteen run at once and are. Push and read the
  runs. Lester's call, 2026-08-08, and it retired a queue of four suites that
  were being run serially for no gain.

* **A cancelled CI run is not a failed one.** Every `ci.yml` sets
  `concurrency: cancel-in-progress: true`, so pushing a second commit while the
  first run is going kills the first. Five plugins showed a grey cancelled run
  on 2026-08-05 for exactly that reason. The code is still covered — the
  successor run contains the same tree — but if you want the history clean, let
  a run finish before pushing again.

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

* The local `~/svn/wordpress_plugins` checkouts were brought to HEAD by the
  2026-08-10 releases and go stale again from here. Query
  `plugins.svn.wordpress.org` or the plugins API for the released baseline
  rather than trusting them — §14 has the release-day table.

* The deploy's exclusions are globbed (`phpcs*.xml*`, `vitest.config.*`, …) so
  config variants are covered; the list lives in the `release-wp-plugin`
  skill's Step 4c.

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
**160 checks** as of 2026-08-10 — re-derive with `grep -c '\.check(' bin/verify.py`
rather than quoting; this file has been wrong about its own arithmetic three
times — and the shared metadata fixture covers §13 including the shared-row
contract two plugins violated. Both run on every push. Re-auditing nineteen
plugins against the spec by hand buys nothing.

**But a green `verify.py` is not evidence the suites pass, and this bit on
2026-08-08.** The two enforce overlapping rules from *separate sources*, and
nothing links them. The canonical README section list lives in `verify.py` AND
in `helper-metadata-testcase.php`; adding `## Installation` to the first and not
the second gave 0 failing checks across 19 while seven plugins' CI went red on
an array diff whose entire content was `+ 1 => 'Installation'`.

So: **when you change a rule, grep for it in both files before believing
either.** The overlap is not documented anywhere and there is no test that the
two agree — which is itself worth fixing if this recurs a third time.

**41 of the spec's 58 sections have something mechanical behind them**, and the
denominator moved on 2026-08-07 when §13.4 added seven. These do not, and each
stays that way for a reason:

| Section | Why not |
|---|---|
| §4.4 Markup | judgement |
| §7.2.1 Process-wide state | needs the suite running |
| §7.2.3 A suite that dies is not one that passed | enforced by `bin/test-all.sh`; §7.2.3 says so, so the next audit does not write a second check |
| §7.3 Coverage | a number, and gaming it is worse than missing it |
| §13.4 and its subsections | scope and process. **Two of the three exceptions listed here are now closed**: §13.4.7's file and class names are checked, and §13.4.9's `--exclude='src'` is in the release skill's rsync and dry-run verified. **§13.4.2 is still open** — "a plugin registering a block still registers the shortcode it wraps" is mechanical and drift-prone, and every block plugin's own suite asserts it, but nothing checks it across the collection |
| §15 Order of work | process, not state |

**The arithmetic, measured on 2026-08-08 — and the measurement's limits matter
as much as its answer.**

Mechanically: the spec has **58** numbered sections; **40** are cited by a `§`
label in `bin/verify.py` or in the shared metadata fixture, and **18** are not.
That closes — 40 + 18 = 58 — where the old "41 of 48 with six unenforced"
accounted for 47 and never did. Re-derive it with:

```sh
grep -oE '^#{2,4} [0-9]+(\.[0-9]+)*' _standards/STANDARDS.md | awk '{print $2}' | sort -u > /tmp/s
grep -ohE '§[0-9]+(\.[0-9]+)*' bin/verify.py _standards/templates/helper-metadata-testcase.php \
  | tr -d '§' | sort -u > /tmp/c
comm -12 /tmp/s /tmp/c | wc -l    # cited
comm -23 /tmp/s /tmp/c | wc -l    # not cited
```

**Both files must be sorted the same way or `comm` returns nonsense** — the
first attempt sorted one numerically and one lexically and produced a list of
sections that "did not exist".

**But 40 is an upper bound on enforcement, not a count of it, and the difference
is the point.** A `§` citation is evidence that somebody had the section in mind,
not proof that a check tests it. §7.2.1's only two citations are *comments about
a different rule* — "test-\*.php would be the §7.2.1 mistake" — and this file has
always, correctly, listed §7.2.1 as unenforced because it needs the suite
running. So at least one of the 40 is a false positive, and there may be more.

Four of the 18 are also not real gaps: **§2, §3, §4 and §5 are parent headings**
whose subsections are enforced. The genuine unchecked leaves are §4.4, §7.2.3,
§7.3, §7.6, §15 and most of §13.4 — and §13.4's subsections are scope and
process prose, which is unenforceable by nature rather than by neglect.

**The honest summary: roughly three quarters of the spec has something
mechanical behind it, the remainder is judgement or process, and no more precise
number should be written here without walking the sections one at a time.**
Counting citations is a five-minute proxy; the audit that produced every finding
of 2026-08-04 was the slow version, and it is the slow version that finds bugs.

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

* **A wrong default is not fixed by editing the default.** The defaults are
  written into the option row at install and by the migration, not read back
  lazily, so changing a shipped default reaches new installs and nobody else.
  wp-postratings' `%RATINGS_PERMISSION%` fix — one refusal template had served
  three reasons, so a site on Guests Only refused a logged-in member and then
  told them to become a registered member — was **inert for every existing
  site**, and the suite was green throughout because nothing had changed.
  `adopt_permission_token()` corrects the stored copy; anything that changes a
  default needs that second half written at the same time. It surfaced because
  Lester asked how the new token got translated, not from any test.

* **A "can the public see it" test is not an authorisation check.** It answers
  a question about the row, and the two coincide only for anonymous visitors.
  wp-postratings' 2.0.0 security fix added `is_post_publicly_viewable()` to
  both vote paths — closing a real hole, and refusing the author of a draft
  exactly as it refused a stranger, so every editorial workflow broke. The
  second clause (`current_user_can( 'read_post', … )`) has to be written at the
  same time or the guard breaks every logged-in path the plugin has. Its
  refusal also **named the wrong thing**: "Invalid Post ID" sent the reporter
  to check the id, which was fine. One message now covers "no such post" and
  "not yours to rate", because telling them apart tells a stranger which drafts
  exist — the same reason the REST route answers 404 rather than 403 for both.

* **Quantify before describing a consequence.** Two findings in one week were
  reported with more confidence than they had. The wp-polls lock was justified
  as fixing a lost update that is not reachable — `get_option()` serves
  autoloaded rows from one `alloptions` snapshot per request, so any two
  requests compute the same values; what the lock actually buys is that the
  work is not done twice. And wp-postratings' numeric border was described as a
  fill landing "in the wrong place", inherited from the test's own comment;
  measured, the error is 0.75px at 5/10 and 1.34px at 9/10, which nobody would
  ever see. Both fixes were still right, for the invariant rather than the
  symptom. Check the mechanism, or measure it, before writing down what it costs.


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
   would break a promise that release — now shipped — made in writing.
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

* **2026-08-04** — the §7.6.1 release blocker closed, the spec-against-checks
  audit finished, a capability audit found by it; six spec sections corrected,
  four live defects fixed, §13.3's naming reversed by Lester. See "Closed on
  2026-08-04". **Three claims in this file were found wrong while acting on
  them, all three by running the thing rather than reading it** — a mutation
  test, an E2E suite, and the same mutation run twice; a fourth test was
  written, discovered to pass with the fix reverted, and deleted rather than
  committed. This file was cut from 1,052 lines the same day: finished items
  became a findings list. (It was cut again on 2026-08-10, the same way.)

* **2026-08-05** — the eleven migration suites written, run to green and
  committed. **Wall clock was the whole cost**: the
  same six-test suite takes two minutes on an idle machine and over an hour
  with a dozen wp-env stacks up, because almost all of it is
  `npx --yes @wordpress/env run` startup rather than browser time.

* **2026-08-09/10** — **all nineteen released to wordpress.org** through the
  `release-wp-plugin` skill: pre-flight, staged trunk, live-site verification on
  lesterchan.net, trunk commit and tag, screenshots committed from `assets/`.
  The final audit found §7.6.2's guard missing from six plugins and a
  category-sanitiser defect in wp-downloadmanager. The
  releases were preceded by the two incidents now recorded in the skill and
  under Traps — the emptied wp-ban trunk (2026-08-08) and the live-site
  `git reset --hard` that reverted seven migrated plugins (2026-08-09).

* **2026-09-02** — this file compacted a third time, by the method the two
  earlier cuts used: every dated entry before 2026-08-24 became one findings
  list, and the lessons that were still parked inside those entries were
  promoted into "Rules earned the hard way" and "Tests that cannot fail" first.
  Three of them had existed **only** inside a changelog entry — among them "a
  wrong default is not fixed by editing the default", which is the collection's
  own thesis. **A lesson recorded only in a dated entry is a lesson that will
  be deleted by the next compaction.** Write it into the durable section the
  same day, and let the dated entry point at it.

The programme found roughly **twenty-five spec bugs and eleven `verify.py`
bugs**, every one because an agent pushed back rather than complied. The pattern
that made it work: one plugin finds it, fix it centrally, the other eighteen
never see it.

