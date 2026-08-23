# Resume here

State of the consistency programme as of **2026-08-10**. Read this, then
`_standards/STANDARDS.md`, which is the contract everything else follows.

**In one line: the campaign is finished.** All nineteen plugins were released
to wordpress.org on 2026-08-09/10, every one tagged at its README's version,
serving roughly 880,000 active installs between them, and **no campaign item
is open**.
What the release itself found is under "Closed 2026-08-10", and it is the
campaign's thesis proving itself one last time.

**Nine releases are staged and deliberately not shipped**, every one the
`released — released+0.0.1 staged` shape, and `bin/verify.py`'s SHIPS_AS plus
§14's table are the machine-readable copy of this list. wp-downloadmanager
2.0.1 — the category-zero renumbering fix, changelog and Upgrade Notice
written. wp-draftsforfriends 2.0.1 — both requests from the one post-release
support topic: the copy button became a clipboard dashicon beside the link,
and the post editor gained a Drafts for Friends meta box (posts only; the
`?p=<id>` link shape is why). wp-postratings 2.0.1, staged 2026-08-13 — a
regression the 2.0.0 security fix caused, written up below. wp-useronline
4.0.1, staged 2026-08-17 — the IPv6 address lookup from a post-release
support topic, written up below. wp-pagenavi 3.0.1 and wp-pluginsused 2.0.1,
staged 2026-08-21 — network activation upgraded only the current site,
written up below. wp-postviews 2.0.1, staged 2026-08-22 — GitHub issue #61:
the "Count Views From" setting was enforced only on the wp_head path, so the
AJAX/REST path that cached sites actually use counted guests under
"Registered Users Only" and skipped the bot exclusion; both endpoints now ask
the setting with the visitor's real login state. wp-sweep 2.0.1, staged
2026-08-22 — the 2.0.0 support-forum reports of the Tools -> Sweep screen
timing out: 2.0.0 computed every count before printing a byte, asked each
table's `COUNT(*)` once per row rather than once, and counted the duplicated
meta sweeps through the `GROUP_CONCAT` query that hauls every duplicate row's
ids into PHP. The screen now renders immediately and the script fetches the
counts afterwards, sequentially (`counts=now` via a `<noscript>` link is the
no-JavaScript path, a Count-column sort still computes synchronously, and the
new `wp_sweep_defer_counts` filter restores the old render); the duplicated
counts read per-key totals only. wp-polls 3.0.1, staged 2026-08-22 — the
front-end assets load only on pages that show a poll, by the head-time scan
plus a render flag the footer enqueue reads. Lester is accumulating fixes
rather than releasing again immediately; when he says ship, the
`release-wp-plugin` skill is the path. Nothing else waits on any of them.

**All nineteen read `Tested up to: 7.1` in git, and none of them says so on
wordpress.org.** WordPress 7.1 became the current release and the readme header
was bumped across the set on 2026-08-20, together with the value `bin/verify.py`
checks for and the §3.2 template, so a plugin still reading 7.0 now fails
verification. Lester's call is that it rides along with each plugin's next
release rather than justifying nineteen releases for a metadata line — so
wordpress.org goes on showing 7.0 until then, and there the compatibility line
is the stale one, not the git one.

**7.1 moved more than the version number: it moved the list table primary
column, and that turned wp-dbmanager red on 2026-08-20.** A sorting test read
`td.column-name` and core had moved that cell into a `th scope="row"`. Fixed,
green, and the whole collection swept — nothing any plugin *ships* was
affected. It leaves two open questions, both about CI rather than about any
plugin: whether the end-to-end job should pin a WordPress version instead of
following `latest`, and whether `Start wp-env` should retry. Written up under
"Closed 2026-08-20".

**Before writing another migration test, read the §7.6.1 entry under "Rules
earned the hard way"** — advice the release sharpened rather than dated: the
write half turned out to be missing its guard in six plugins after all, held
off by hook order and an imperfect sanitiser rather than by anything anyone
wrote. The read half is still the real defect, and the eleven suites written
on 2026-08-05 are all built on it.

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

## Current state — verified 2026-08-10

**All nineteen are released, green on CI at their current `HEAD`, and level
with their remotes.** The release state was checked on 2026-08-10 by comparing
each repo's `Stable tag` against what `api.wordpress.org` serves — all nineteen
match, with the staged 2.0.1s (wp-downloadmanager then, wp-draftsforfriends
since) the intentional divergences.
The CI state was checked per repository with `gh run list` against
`git rev-parse HEAD` rather than inferred from the last push. The twentieth
repository, this one, is level too.

**Every number below moves with the next commit — re-run rather than quote.**
This file has been wrong about exactly that before: wp-sweep was one commit
behind `origin/master` on 2026-08-07 while a line here claimed all twenty
level, because a cloud session had pushed and nothing local had fetched —
**`git status` says nothing about a remote being ahead without a `git fetch`
first**, which is why the start-of-session check at the top now has one. CI is
the authority; `gh run list` per repo takes a minute.

* **The whole collection was run, not sampled.** `bin/test-all.sh` and
  `bin/test-all.sh --multisite` both report all 19 plugin suites passed, and
  `verify.py` is 0. That sweep mattered more than it looks: it was the first
  time CI's metadata fixture had seen the nineteen README rewrites.
* **The blocks phase is finished and pushed** — twelve blocks in eight plugins,
  all eight run locally one at a time, wp-postratings and wp-showhide on
  multisite too, wp-ban and wp-print as non-block controls.
* phpcs, eslint and the assertion-message ratio are clean. **Every assertion in
  the collection carries a failure message**;
  `python3 bin/measure_assertions.py /path/to/plugins/*` re-derives the ratio.
* Playwright is green on every `upgrade.spec.js`, but only wp-dbmanager's was
  recently run as a whole file — the stalest claim here, so re-check it first.
  PHPUnit's six-row matrix runs in CI on every push and is green everywhere.
* **A cancelled run is not a failed one.** Pushing twice in quick succession
  cancels the first run by design; see Traps.
* The permalink audit of the E2E suites is complete — see below.
* **A green CI sweep does not survive the next push.** Six repositories were
  pushed to on 2026-08-10 after the release — wp-downloadmanager (`f2cdb7b` plus
  two documentation commits), wp-relativedate, wp-serverinfo, wp-showhide and
  wp-sweep. Three of those were red before the fixes below, from one stale string
  each. Re-run `gh run list` per repo; the paragraph above is a method, not a
  result. The method was re-run late on 2026-08-10, after those pushes settled:
  all nineteen level with their remotes after a fetch, CI green at every HEAD,
  `verify.py` 0, and wordpress.org matching every `Stable tag` —
  wp-downloadmanager's staged 2.0.1 then the one intentional divergence;
  wp-draftsforfriends' staged 2.0.1 joined it later that day.
* **No known plugin bug is outstanding that is not already fixed in git.**
  wp-downloadmanager's category-zero defect is fixed as the staged 2.0.1, which
  now carries a second fix — the N/A-versus-blank split between its two admin
  screens — and is still deliberately unreleased so fixes can accumulate.
  wp-polls' widget was found on 2026-08-07 and fixed on 2026-08-08; the
  write-up is kept below because how it was found is the useful part.

## Closed 2026-08-23 — the final verification pass, and the campaign's close

A closing audit is verifying the canon landed everywhere: a grep-matrix of
every pass-eight item, a zero-tolerance sweep for every retired name across
code/tests/docs, frozen surfaces diffed against the released wordpress.org
zips, the ten staged releases reconciled three ways, and a last drift sweep.
Its one named-but-unverified candidate so far: **a wp-sweep count/sweep
whitelist disagreement**, possibly fallout from the sweep_count →
wp_sweep_count admin action rename — check whether any allow-list, nonce
action or JS data-action still references the old names or disagrees with
the PHP hooks. If this session ended before the report landed, re-run that
check first, then finish the audit's checklist (it is spelled out in this
entry) and close this section with the verdicts.

The report came back: everything held except four findings, all fixed and
pushed the same day. The sweep whitelist candidate was a false alarm — the
action rename is complete and self-consistent. The real ones: **wp-ban's
migration ran only from admin_init and the WP-CLI subcommands**, so a
cron-driven background update served the front end unmigrated until somebody
opened wp-admin — the canon had miscounted it among the direct-call plugins;
it runs on `init` priority 5 now, with a hook test, and that also settles the
registered-default trap on every path. wp-useronline was the lone holdout on
the `register()` rename; wp-sweep, wp-postviews and wp-useronline still named
their admin enqueue callback after the hook (postviews' fix collided with an
existing `enqueue()` gate, renamed `screen_loaded()`). And the two loop
sentences — the cap and the restore — now read identically in all seventeen
files that carry them; the activation-update elaborations were judged
per-plugin rationale and kept. Frozen surfaces were diffed against all
nineteen released zips: identical. Ten staged releases reconciled three ways
with every bullet mapping to a real change. verify.py 0, twenty clean level
trees, twenty green CI runs.

That is the campaign: eight audit passes, one canon, one fix pass, one
closing verification — and the ninth pass's findings were a hook, three
names and two sentences, which is what convergence looks like when it is
nearly done.

## Closed 2026-08-23 — pass eight: the implementation-parity fix pass ran

An eighth audit built feature-by-feature matrices (asset gating, capability(),
Options/Install/REST/CLI/Blocks/AJAX/Widget method names, recurring comment
idioms, bootstrap shapes) and found 42 convergence items — the same feature
under different names across plugins, the exact drift class the campaign
exists for. **`_standards/pass-eight-canon.md` holds the chosen shape for
every item**, including the three judgement calls already made: the upgrade
hook converges on `init` priority 5 (wp-postratings' comment correctly
indicts admin_init — background updates run on cron); the theme-override
stylesheet lookup converges on the navi pair's child→parent algorithm; the
legacy `polls`/`email` front-end AJAX action names stay (renaming breaks
pages cached with the old script — deliberate, record as such), with only
wp-sweep's admin-only actions gaining the prefix. Frozen surfaces the fix
pass must not touch are listed in the canon's process rules.

The fix pass ran 2026-08-23: four agents over disjoint repo sets, ~45
themed commits across all nineteen, every repo's suites and phpcs green
before its push, e2e for the seven AJAX/widget/wiring plugins (polls 51,
downloadmanager 85, postratings 77, postviews 116, email 54, sweep 72 with
three contention flakes that passed 22/22 in isolation, useronline 97),
verify.py 0 across 19 throughout. The predicted fallout mode appeared three
times and was fixed the same way each time: moving the upgrade to `init`
means a WP-CLI boot migrates the site, so e2e fixtures now seed and read
back in one `wp eval` call (polls, downloadmanager, email). freemyinternet's
missing network-activation loop became its staged 1.0.1 — the tenth staged
release. Two agent judgement calls stood: wp-downloadmanager keeps
`test-security.php` (from the earlier pass) and serverinfo's plugins-screen
link says "Server Information", not "Settings", because that is what it
opens. dff's flagged leftovers (defaults()/markers()/enqueue()) were
finished by hand. §2.7.1 of the standard carries the load-bearing
differences the pass kept.

## Closed 2026-08-22 — the performance wave: all three findings fixed

Pass seven's three performance findings are closed, failing-test-first,
suites and Playwright green on each:

* **wp-postratings** no longer queries every vote row on every loop of every
  page for a display that defaults off — the filter gate moved in front of
  the query — and its assets load only where a rating renders, on
  wp-useronline's render-flag mechanism (theme template tags defeat content
  scanning, which decided the choice). 77 e2e specs prove the vote path with
  the footer-delivered script. Both ride the staged 2.0.1.
* **wp-useronline**'s table gained `KEY user_ip` and `KEY user_id`, so the
  per-request DELETE and per-IP COUNT stop scanning. DB_VERSION 1 → 2; an
  existing site gains the keys through maybe_upgrade() → dbDelta on its first
  request after update, proven against the table shape transcribed from the
  4.0.0 SVN tag, with a guard against dbDelta's user_ip_2 re-add mode. Rides
  the staged 4.0.1.
* **wp-polls** enqueues only on pages that show a poll, by both sibling
  mechanisms at once: wp-stats' head-time scan (shortcode/block/widget, so
  the stylesheet still reaches the head with no unstyled flash) plus
  wp-useronline's render flag read on wp_footer for what the head cannot see
  (template tags, archives) — print_late_styles() runs at wp_footer 20, the
  enqueue sits at 10, and the inline bar-colour block is guarded against
  double emission. Staged as 3.0.1, the ninth staged release.

A counting note: pass four's audit reported seven staged releases and this
file was "corrected" to say seven — but wp-sweep's 2.0.1 was already staged,
so the true count was eight. The audit counted divergence against
wordpress.org and still missed one; the headline paragraph above now defers
to SHIPS_AS and §14 precisely because prose counts keep rotting.

## Closed 2026-08-22 — pass seven: the outward faces

A seventh audit swept what only the outside world sees. The load-bearing
surfaces all passed: every public entry point added or changed since the
2026-08-09 security review was read as code and none has a gap (the
postviews REST/AJAX paths, the vote paths, the eight block render callbacks,
the useronline refresh, the sweep count endpoints, the draftsforfriends
metabox); shipped dependencies carry zero advisories (`npm audit --omit=dev`
and `composer audit --locked` clean across all nineteen — the dev-only
lighthouse/@wordpress/scripts chains are upstream watch-items); wordpress.org
assets, screenshots, banners and stable-tag state agree with the READMEs
everywhere; GitHub metadata is uniform. Fixed the same day: the
wp-relativedate header's misplaced apostrophe ('2 'Seconds Ago') and
wp-dbmanager's space-before-comma — both on every install's Plugins screen —
plus three GitHub blemishes (showhide's stale description, three
trailing-whitespace homepages). Deferred: jsdom three majors behind (dev
only, rides the next vitest), freemyinternet's PNG icons against the
collection's SVGs.

The performance spot-check is the pass's real yield, held for Lester's call:
wp-postratings queries every vote row for the post on every loop of every
page before checking a filter that defaults off (the gate belongs before the
query); wp-useronline's per-request DELETE and per-IP COUNT scan for want of
`user_ip`/`user_id` keys (a schema bump); wp-postratings (~16 KB) and
wp-polls (~13 KB) enqueue site-wide unconditionally. wp-postviews and
wp-pagenavi verified near-zero.

## Closed 2026-08-22 — pass six: what the words claim

A sixth audit swept the claims layer: plugin CLAUDE.md standalone rules,
documented-vs-actual API, README content accuracy, e2e spec quality,
verify.py's own text, git hygiene, and a code-level read of every
post-release shipped diff. The code side came back clean — no unsanctioned
shipped change anywhere, no assertion-free or skipped e2e spec, no
cannot-fail check in verify.py, no signed commit. The words needed work:

* **README staleness cluster**: the §4.2.2 tab renames stopped short of the
  prose in four READMEs — wp-postratings ("Ratings Options" ×4), wp-email
  (menu paths still naming "E-Mail" and "Manage E-Mail" for what the menu
  calls WP-EMail and Logs), wp-polls (two tab mentions and one screen
  docblock) and wp-downloadmanager ("Download Templates"). wp-polls' shipped
  3.0.0 changelog also named a `wp_polls_uninstall_site()` that never
  existed — corrected to the Install method that does. All fixed.
* **wp_postviews_capability** was the only capability filter of fifteen with
  no README mention; it has a FAQ entry now.
* Four CLAUDE.md lines violated the standalone rules (one true cross-repo
  reference in wp-print, two collection-reference claims, one unverifiable
  state-of-work claim in wp-postviews). Fixed.
* verify.py cited §7.6.1 for the rule §7.6.2 states, and a comment still
  described §2.5's pre-rewrite text. Fixed.
* **Recorded, not repaired**: 27 pushed commits authored by Claude carry no
  session trailer (the SessionStart-hook rollout predates the convention),
  and 17 subjects run past 72 characters. History is public; rewriting it
  for trailers is worse than the miss. The convention holds for new commits.

## Closed 2026-08-22 — pass five: names, and the shapes inside files

A fifth audit swept what no pass had: file naming conventions and in-file
structure. Two findings were against the standard itself — §1's layout tree
predated the e2e, blocks and Claude-workflow phases (redrawn; the closing
bullet now says the tree is what the repo *tracks*, not what ships), and §2.8
is being outrun by the newest files' long docblocks (89 of 173 class files,
worst are the newest — left to the touch-it-trim-it rule, no sweep). The rest
was majority-vs-outlier and was fixed across all nineteen in one pass, three
agents on disjoint repo sets, one commit per fix-class per repo:

* **Guards**: `defined( 'ABSPATH' ) || exit;` and
  `defined( 'WP_UNINSTALL_PLUGIN' ) || exit;` everywhere — three whole plugins
  and three main files came off the if-block form, and fourteen uninstall.php
  guards converged. Four suites pinned a guard spelling by regex or literal;
  every pin was found before its suite ran and moved with the guard.
* **Names**: `test-upgrade.php` wins over `test-migration.php` (the e2e side
  was already unanimously `upgrade.spec.js`); `tests/js/helpers.js` wins over
  `helper-dom.js`/`helper-load.js`; `test-escaping.php` over `test-kses.php`
  and commentnavi's `test-security.php` — but wp-downloadmanager keeps its
  `test-security.php`, which a fix agent correctly judged to be a genuine
  broad security suite the audit had misfiled as an escaping suite. Settings
  suites live in `test-settings.php`; pagenavi's screen tests took their own
  `test-settings-screen.php` after the first fold-in put two classes in one
  file and verify.py's §7.1 check said no. Assorted one-offs: ban's
  trust-proxy file, print's lifecycle→uninstall, relativedate's singular
  template-tag, sweep's and showhide's tests/js names, postratings'
  extensionless e2e requires.
* **In-file**: 'use strict' in the five shipped JS files missing it; GROUP
  before PAGE in the two Settings classes that flipped §2.2's order; wp-polls'
  admin CSS header no longer names a file dead since the restructure.

Shipped-code edits are guard spelling, five JS strict pragmas and a CSS
comment — behaviour-preserving, riding each plugin's next release; the staged
versions were not touched. Suites, phpcs, lint and verify.py green across all
nineteen before each push.

## Closed 2026-08-21 — the drift audit, and the five defects it survived

Two agent audits — one normalising every shared file across the nineteen and
diffing the copies, one walking the test suites for coverage gaps — found the
shared surface in better shape than feared: CI, composer.json, README
structure, the §1.1 floors and the metadata contract are uniform or correctly
derived, and most "missing test file" cells are the plugin genuinely lacking
the feature. Five defects were real, and all five are fixed, one commit per
plugin per defect:

* **`run_uninstall()` degraded on its second call** in seven plugins (the
  `function_exists` shape), plus wp-stats' delegate and wp-email's single-site
  patch-up: the first call in a process ran uninstall.php's real network loop,
  every later call silently uninstalled the current site only, so two
  uninstall tests in one multisite run exercised two different behaviours.
  All nine now carry the fan-out in the helper — the same loop the file runs,
  every call — which four plugins already had. The five suites that
  *reimplement* the deletions instead (their uninstallers drop tables, and
  DDL commits through the suite's transaction) keep that sanctioned shape.
* **wp-useronline's uninstall path was executed by nothing** — its helper's
  docblock promised the compensating source assertions lived in
  test-install.php, and they did not; emptying uninstall.php left the suite
  green. The two tests every other reimplementing plugin carries exist now.
* **One declared range, two resolved lint rule sets** — `@wordpress/eslint-plugin
  ^25.7.0` was locked at 25.7.0 in six plugins and 25.8.0 in thirteen. All
  nineteen lockfiles now resolve one registry state (25.9.0). The residual
  cross-plugin differences are nested pins under the block-build dependencies
  only the eight `src/` plugins carry — derived, not drift.
* **Eight spellings of the test-loader function**, three of them breaking
  §2.5's prefix rule, and two bootstraps (wp-dbmanager, wp-draftsforfriends)
  missing the test-library guard. All nineteen now declare
  `_{{under}}_manually_load_plugin` behind the guard.
* **Two verbs for the per-site uninstall work** — wp-email, wp-sweep and
  wp-draftsforfriends said `_delete_options` where sixteen said
  `_uninstall_site`. The loop-called verb is `_uninstall_site` everywhere now
  — wp-sweep's renamed outright, wp-email's and wp-draftsforfriends' kept as
  prefixed sub-helpers the new verb calls; §2.5 also names the second
  sanctioned shape,
  the Install-delegating file wp-polls, wp-postratings and wp-useronline carry.

One self-inflicted lesson worth keeping: two of the uninstall.php edits were
made with sequenced string replaces, and the second replace rewrote the body
of the wrapper the first had just inserted, into a self-call. wp-email's
suite then died on memory at the same test every run — an infinite recursion
under a runner reads as SIGKILL at 49%, not as a stack trace. The stash test
(`git stash` → green → `git stash pop`) is what localised it in one run.

The follow-up closed the same day, all of it agent-built and mutation-checked
where a mutation could prove anything: all eight network-activation
test-multisite.php files exist and pass (the table owners assert the table per
site, wp-stats asserts the per-site url — the one seed nothing self-heals);
wp-commentnavi's stylesheet cascade and both twin filter gaps are tested;
wp-postratings has its e2e security spec, driving the AJAX vote reply that
PHPUnit cannot see. The cosmetic tail went too: the option setter is
set_options( array ) in all eight suites that have one (wp-postratings keeps
its merge-into-stored semantics — 58 call sites layer overrides, and a
defaults merge would drop them), the four suites that kept migration tests
inside test-options.php moved them to test-upgrade.php, and the bin/build
comment, wp-ban's script order and wp-downloadmanager's eslint comment match
their majorities. Two deliberate non-changes: no helper-source.php was
introduced where suites inline file_get_contents, and wp-showhide keeps "The
block registers" — it has one block, and uniformity would make the sentence
wrong. One judgement worth keeping: MariaDB 12 lists temporary tables in SHOW
TABLES, which is the only reason the table assertions work under the
harness's CREATE TEMPORARY rewrite; a MySQL-backed harness would need the
filter-removal form wp-email's metadata test already uses.

A fresh adversarial re-audit then verified every claim above mechanically and
came back five findings, all fixed the same day: the activation-side
get_sites() cap was unpinned in wp-draftsforfriends, wp-postviews and
wp-postratings while their uninstall side's was (the exact bug class the
campaign closed could have re-entered green); wp-postratings and wp-showhide
were the only two eslint configs without the declared tests/e2e CommonJS
override, linting clean on parser-default luck; three set_options() copies
lacked the array type hint; the bootstrap run-hint existed in three phrasings;
and this file overstated the _delete_options rename. Twenty repos ended the
day with clean level trees and a green latest CI run each.

A third pass the next day verified the second pass's fixes sha-for-sha and
swept fresh angles (e2e infrastructure, the uninstall source-assertion
contracts, docblock truth, staged-release consistency — six staged, not five:
wp-postratings 2.0.1 was already among them). Five residual findings, fixed
the same day: the fourteen new test-multisite.php files had already forked
(two stack-test forms, three fixture spellings, two isolation-test names —
converged on the majority frame); wp-draftsforfriends alone lacked the
multisite isolation test; a ninth set_options() in wp-email's AJAX base was
untyped; wp-relativedate and wp-showhide were the only two with no pin on
uninstall.php's site-query cap; and §2.5 repeated the _delete_options
overstatement RESUME had already corrected.

## Closed 2026-08-21 — two bootstraps upgraded only one site of a network

A survey of the eighteen `includes/class-{{slug}}.php` bootstraps, prompted by
wp-pagenavi looking unlike the rest, found the reverse of what it looked like:
wp-pagenavi and wp-commentnavi are near-clones — the only pair where the
bootstrap class does its own `require_once`s rather than the main plugin file —
and the clone had drifted in the one place it mattered.

`WP_PageNavi::activate()` and `WP_PluginsUsed::activate()` took no
`$network_wide` and ran the upgrade against whichever site was current.
`WP_CommentNavi::activate()`, the same file in the same shape, loops
`get_sites( number => 0 )`. Settings and version markers are per-site rows, so
a network activation left every other site's legacy row unread — wp-pagenavi
serving the shipped defaults on its front end, wp-pluginsused publishing
plugins its hidden list would have hidden.

**Low severity for a reason worth writing down: the same routine is also on
`admin_init`**, and `migrate()` deletes the legacy row only after folding it
in. So nothing was lost and every site healed the moment somebody opened its
dashboard. Only a network whose subsites are front-end-only stayed wrong, which
is why it survived — and it is the shape to look for, because a bug that
repairs itself under every hand-check is invisible to hand-checking.

**Nothing tested the loop on any of the three**, including the one that had it.
`tests/test-multisite.php` is now on all three: the loop, the per-site
activation that must not touch its neighbours, the uncapped `get_sites()` read
off `pre_get_sites` rather than by building a 101-site fixture, and the unwound
blog stack. Mutation-checked on each — deleting the branch again fails two of
the four. Suites, multisite suites, phpcs and `verify.py` are green on all
three.

All three are pushed, and the two fixes are staged as wp-pagenavi 3.0.1 and
wp-pluginsused 2.0.1 — header, constant, Stable tag, changelog section and the
metadata suite's expected_version() moved together, deliberately unreleased so
fixes can accumulate. wp-commentnavi's commit is tests only and stays at its
released 2.0.0.
## Closed 2026-08-20 — WordPress 7.1 moved the list table primary column

Two plugins were red the morning after the `Tested up to: 7.1` sweep, and only
one of them for a reason that lives in this collection.

wp-dbmanager's `tables.spec.js` failed on "the tables list sorts by the column
headed" — first try and Playwright's own retry — while the other 55 tests
passed. The read was `.wp-list-table tbody tr td.column-name` and it came back
empty. That looks exactly like a navigation race: `allInnerTexts()` is the one
read in that suite that does not auto-wait, and it sits directly after a click
that starts a full page load. **That was the first diagnosis and it was wrong.**
An added `toBeAttached()` waited its full ten seconds, twice, and reported
"element(s) not found". The cells were not late. They were absent.

What settled it was the diff rather than the log: the last green run and the
first red one are **one README line apart**, and no browser test can see
`Tested up to`. **WordPress 7.1 moved the primary column of every admin list
table out of a `td` and into a `th scope="row"`**, giving it an `aria-label`
naming the row, so that a screen reader announces a row by its title instead of
by "Select All" — core ticket #32892, open eleven years. The checkbox column
went the other way, `th` to `td`. wp-dbmanager's `name` column is the primary
column in both of its modes, being the first column that is not the checkbox,
so the single cell that test reads is precisely the one core moved.

The fix is core's own migration advice: **match the class, not the element.**
`.column-name` reads the column on both sides of 7.1; `td.column-name` reads it
on neither side from 7.1 onwards.

**The collection was swept and wp-dbmanager was the only one.** No shipped CSS,
JS or PHP in any of the nineteen scopes a list table selector to a `td`, so
nothing a user sees was affected — the part that mattered, with 880,000
installs between them. Every other `column-` selector in the E2E suites was
already class-only: wp-ban's `.column-ip`, wp-draftsforfriends' `.column-link`,
wp-polls' `.column-pollq_id`, wp-sweep's `.column-group` and `.column-name`.
wp-sweep has its own sorting test over the same markup and stayed green purely
because it never wrote the element name.

**The end-to-end job follows WordPress `latest` and nothing pins it.**
`.wp-env.json` carries `"core": null`, and the E2E job sets no `WP_ENV_CORE`
where the PHPUnit matrix sets one per row. That is why a WordPress release
turned a repository red with no commit behind it. Left open deliberately:
pinning makes the job reproducible, not pinning is what caught a real
compatibility break on the day it shipped, and a pinned row plus a `latest` row
buys both for the price of one more job — across nineteen workflows, or none.

wp-commentnavi was the other red one and was never any of this. Its
`Start wp-env` step died inside wp-env's own image build on `Could not open
input file: /tmp/composer-setup.php` — the composer installer download failing
upstream, one matrix row out of six, green on the re-run with no commit.
wp-dbmanager hit the same class of failure twice more within the hour, once on
an HTTP 504 from api.github.com fetching PHP-Parser. **Three upstream download
failures in eighty minutes across two plugins.** A retry around the step would
pay for itself if it keeps costing re-runs, and like the pinning question it is
all nineteen workflows or none.

## Closed 2026-08-17 — wp-useronline linked every IPv6 visitor to a whois that cannot read one

A wordpress.org topic against wp-useronline: the detailed listing links each
address to `whois.domaintools.com/<ip>`, which answers "Malformed Domain or IP"
for an IPv6 address. On a host with IPv6 switched on that is most of the
listing, and the reporter named three services that read both — ipinfo.io,
ip-api.com and who.is.

Only ipinfo.io survives being checked. who.is redirects
`whois-ip/ip-address/<ipv6>` to its own bare search form, and does it for the
percent-encoded form too; ip-api.com's page takes the address in a fragment, so
it is a JavaScript app rather than a URL. **The reporter's shortlist was three
names, and two of them do not do the thing the topic is about** — worth the ten
minutes of curl before committing to a default, because every one of them
returns HTTP 200 while dropping the address on the floor.

Staged as 4.0.1: the default becomes `https://ipinfo.io/<ip>`, and
`wp_useronline_ip_lookup_url` filters it, receiving the raw address as its
second argument. Two things the shape is deliberate about:

* **The encoding stays.** `get_ip()` validates with `FILTER_VALIDATE_IP`, but
  the column also holds whatever releases before 4.0.0 wrote into it, so the
  default keeps `rawurlencode()` — verified against ipinfo.io, which resolves
  `2001%3Adb8%3A%3A1` and the bare colons alike. `esc_url()` passes both
  through; the unit test asserts the emitted `href`, so that is pinned rather
  than assumed.
* **An empty return drops the link rather than emitting `href=""`.** Blank means
  "do not hand a visitor's address to a third party", and the obvious
  filter-then-print shape turns that into a link to the screen you are already
  on, which looks like it worked. Guard and test both, mutation-checked.

**Adding a filter is a patch; renaming one is not.** The 4.0.0 metadata test
pinned `expected_version()` to the literal `4.0.0` to stop the filter renames
folding into a 3.0.x — a bump that could only ever be tripped by the next
legitimate patch. It now pins the major, which is what the rule was about.

**Staging this one exposed §14's table as a fourth unchecked copy.** Lester
noticed the table said `2.0.0` for wp-postratings while the paragraph above and
`SHIPS_AS` both said 2.0.1. Only wp-downloadmanager's row was ever marked,
because it was staged on release day and the two staged after it moved
`SHIPS_AS`, moved the plugin's three markers and left the table alone — and
nothing read the table, so nothing said. §14's own prose calls `SHIPS_AS` its
machine-readable half; `verify.py` now checks that claim, reading the last
version each row names and comparing it. wp-draftsforfriends and wp-postratings
are marked, and the check was run against the unmarked rows to see it fail. The
number now lives in four places with three of them checked against the fourth,
which is the most this shape allows.

## Closed 2026-08-13 — the 2.0.0 security fix refused the site's own drafts

A wordpress.org topic against wp-postratings: every vote answered
`Invalid Post ID (#50408)`, and the reporter had checked the id against the
edit URL, so the message was pointing at the one thing that was right. Their
note "it's not being used on any publicly available pages" was the whole
answer — an editorial queue rating unpublished posts.

The cause was ours, and recent. The 2026-08-09 security review added
`is_post_publicly_viewable()` to both vote paths, closing a real hole: a
stranger could seed `ratings_users` and `ratings_score` on a draft, and a text
template holding `%POST_TITLE%` or `%POST_CONTENT%` returned unpublished
content in the reply. But **the guard asked what the post was and never who was
asking**, so it refused the author of the draft exactly as it refused a
stranger. Fixed by adding `current_user_can( 'read_post', … )` beside the
public test — `read_post` maps to `edit_post` on every unpublished status, so
nobody is handed a post they could not already open, and the hole stays shut.

Three things worth carrying:

* **A "can the public see it" test is not an authorisation check.** It answers a
  question about the row, and the two coincide only for anonymous visitors. Any
  new guard of that shape needs the second clause written at the same time, or
  it breaks every logged-in workflow the plugin has.
* **The refusal named the wrong thing.** "Invalid Post ID" sent the reporter to
  check the id, which was fine, and cost the round trip that would have found
  it. The message is now "This Post Cannot Be Rated (#…)", one string for both
  "no such post" and "not yours to rate" — telling them apart tells a stranger
  which drafts exist, which is why the REST route answers 404 rather than 403
  for both. `wp_postratings_is_ratable` filters the decision for anyone whose
  answer is neither.
* **It is contained.** `is_post_publicly_viewable` appears in no other plugin in
  the collection — checked across all nineteen — so nothing else needs the same
  fix. The security review's other findings are unaffected.

The unit cases live in `tests/test-vote.php`; the browser case is
`voting.spec.js`, "a post the public cannot see is still ratable by somebody who
can", and it earns its place because the unit tests call `process_vote()`
directly and so never exercise the rendered nonce or the AJAX action on a
non-public post. Both were run against the unfixed source and both fail there.

## Closed 2026-08-10 — a readme sweep turned three suites red

The sweep that dropped "upgraded from" floors and version-row claims out of the
READMEs was right about the substance and left three repositories failing every
PHPUnit leg — eighteen jobs — on one stale string each.

`upgrade_notice_subjects()` in wp-relativedate, wp-serverinfo and wp-showhide
still listed `wp_<slug>_version` as something the Upgrade Notice must mention,
while the same class declared `has_version_row()` false. The two were asserting
opposite things about one plugin. **Removing the entry removed no coverage**: the
shared `test_version_row_holds_exactly_plugin_and_db()` fires `plugins_loaded`
and `init` and requires `get_option()` to come back false for these four, so the
absence of the row is pinned by behaviour, not by a string in a readme. Checked
before deleting anything, because a list entry that looks obsolete is exactly
what a real assertion looks like from the outside.

The same sweep missed two places it existed to fix, and a third turned up next to
them — all three claims about behaviour, all in comments, none reachable by any
check that exists:

* `wp-showhide.php` said the last-run value "is kept in the `wp_showhide_version`
  row". The constant is displayed and never stored.
* `class-wp-serverinfo.php` said the one row the plugin keeps is
  `wp_serverinfo_version`, "see `WP_ServerInfo_Options`" — a row nothing writes
  and **a class that does not exist in the repository**.
* `wp-sweep/uninstall.php` said its two `delete_option()` calls clear what the
  plugin wrote and what "the upgrade" deletes. There is no upgrade; both rows are
  2.0.0 **beta** leftovers, which is what its own `CLAUDE.md` had said all along.
  Its function comment justified spelling the names out by reference to
  `WP_Sweep_Options`, which `test-options.php` requires not to exist.

Established before rewording rather than assumed: **no released version of any of
the four ever wrote its row.** `0d31075` ("Store nothing at all", 30 July) took
the markers, the options classes and the schema counters out before all four
shipped, so naming the row in an Upgrade Notice would send owners hunting through
`wp_options` for something that was never there. Only a pre-release build wrote
one, which is the single case `uninstall.php` still cleans up.

`b8d50de`, `bbe00c3`, `813cbea`, `d73ffe1`. All four green single site and
multisite, phpcs clean, `verify.py` 0.

**The gap this leaves.** `verify.py` already knows which plugins these are —
`STORES_NOTHING` names the four, and asserts they define no `DB_VERSION`. It has
never checked that they do not *claim* a row, which is why three false statements
survived a sweep aimed at them. Nothing was removed from `verify.py`; the check
was never written. Two would close it, both mechanical rather than prose
matching: for a slug in `STORES_NOTHING`, `wp_<under>_version` may appear only in
`uninstall.php` and `tests/`; and a plugin may not name a `WP_<Prefix>_*` class
no file declares. The second catches all three dead-class pointers above.

## Closed 2026-08-10 — wp-downloadmanager's two admin screens disagreed

Manage Downloads printed "N/A" for a file in no category; the Delete File
confirmation for that same file printed nothing — one click apart, on the row the
owner had just clicked. The list table was the only caller that had a label, so
every other caller printed the empty string by accident rather than by choice.

The label is now a parameter on `category_name()`, which puts the choice at each
call site. The two admin screens pass "N/A"; three callers deliberately do not,
and the docblock says why — the listing heading (category 0 there means *every*
category, so it would read "Downloads: N/A"), the feed's `<category>` element,
and WP-CLI's csv/json/yaml, where an empty value cannot be mistaken for a
category somebody named N/A.

The part that would have been got wrong: the lookup had to stop distinguishing
*absent* from *blank*, because category 0 is present and blank by design.
Returning the fallback only for a missing key would have printed nothing for
exactly the file the fix is about. The blank test is `'' !== $name` rather than
`empty()`, so a category named `0` keeps its name.

`f2cdb7b`. Six mutations each applied alone, all killed; 472 tests green single
site and multisite; 85 Playwright locally and green on CI. Staged in 2.0.1, which
now carries two fixes and is still deliberately unreleased.

## Closed 2026-08-10 — the release of all nineteen

Released through the `release-wp-plugin` skill: pre-flight, staged trunk read
by hand, the staged tree exercised on lesterchan.net before anything was
published, trunk committed, svn-copied to `tags/<version>`, screenshots
committed from `assets/`. The five plugins that had sat on `Stable tag: trunk`
for years now have real tags, and the local SVN checkouts are at HEAD for the
first time since 2022 — which changes nothing about the rule: ask the
repository URL, not the checkout.

**The final pre-release audit found §7.6.2's write guard missing from six of
nineteen plugins** — wp-postviews, wp-postratings, wp-downloadmanager,
wp-draftsforfriends, wp-email and wp-useronline. The guard (`add_option()` when
the row is absent, because `update_option()` writes nothing when the migrated
value equals the registered default) was stated with wp-print as the reference;
nothing enforced it, so it had drifted, exactly as the campaign's thesis
predicts. All six are fixed: two shipped with the fix, four were re-tagged.
`verify.py` enforces it now and STANDARDS gained §7.6.2 (`21d9d17`).

**Why no data was ever lost, and why that is not comfort.** In wp-postviews
and wp-postratings the migration runs on `init` and `register_setting()` on
`admin_init`, so the defaults filter did not exist yet when the migration
wrote; wp-useronline's runs on `plugins_loaded`, earlier still; in the rest,
both sit on `admin_init` at the same priority, and the ordering of two
`add_action()` calls was the entire protection. Worse, the migration tests that existed were
green for a reason unrelated to the code: `update_option()` sanitises before
it compares, so a sanitiser that happened to alter the shipped defaults — kses
collapsing a doubled space in one template default — was what made the
migrated value differ and the row get written. Lester flagged the doubled
space as a cosmetic blemish; removing it turned two plugins' migration tests
red. **A test that passes only because a sanitiser is imperfect cannot fail
for the right reason.** Each of the six now also asserts the shipped defaults
are a fixed point of its own sanitiser, so the day that stops being true is
reported rather than silently absorbed; `fa15fb1` is the template-side check.

**wp-downloadmanager had a second live defect hiding the first.**
`sanitize_categories()` handled only the textarea's string form, but it is
`register_setting()`'s callback, so core also runs it from `add_option()` /
`update_option()` with the stored **array** — which a string sanitiser answers
with `''`. Every whole-row write collapsed the category list to one blank
entry and left every file reading "N/A", including the upgrade routine's own
write. Being wrong is also what altered the defaults and gave `update_option()`
a difference to find — so the write guard alone would have written the blanked
list. Fixed in `e91c1eb` and re-tagged.

**Found the same day, after the release: seventeen changelog lines said "up
from 6.0 and 7.4".** §14.1 forbids naming the floors a reader upgraded from —
the numbers describe the pre-revamp *repositories*, not anything a real site
declared — and the rule was applied to every Upgrade Notice but never to the
`BREAKING:` changelog lines, and nothing checked it. Sixteen plugins shipped
the line (wp-dbmanager and wp-serverinfo each asserting different, equally
wrong predecessors). All stripped, and `verify.py` now fails any README
containing ", up from ". The three store-nothing plugins' claims of a
`{{UNDER}}_version` row they never write — README, one header docblock and one
uninstall docblock — were corrected in the same pass, closing the "Known
discrepancy" sections their CLAUDE.md files carried. The corrections are in
git; wordpress.org serves them with each plugin's next release.

**What is staged as 2.0.1 and not released.** A fresh install shipped its only
category at index 0 — the slot that means "no category" — so the Add File
dropdown offered it and the first settings save renumbered the list, orphaning
every file filed before it. Changing the default alone is unsafe because
`all()` merges the stored value over it, so the fix is the default change plus
a migration that shifts the categories and renumbers `file_category`, run once
off a marker bump. Committed (`1ef3089`), changelog and Upgrade Notice
written, `Stable tag` already 2.0.1, and `verify.py`'s `SHIPS_AS` moved with
it. Releasing is Lester's call.

## Closed 2026-08-09 — the security review

One reviewer per plugin plus a pass across the whole tree, for injection, XSS
and account takeover, widened on the ask to command injection, path traversal,
arbitrary file access, SSRF, CSRF, object injection and information disclosure.
**Twenty-seven findings, all fixed, all with tests.** The write-up pairing each
finding with the plugin it was in and the commit that closed it is deliberately
**not in this repository** — ask Lester for it. This repository is public; that
document is the collated version, and see the note below the tiers for why the
two are kept apart.

**The three things asked about specifically were in good shape.** No SQL
injection: all 160 `$wpdb` call sites resolve to bound parameters, table-name
properties, integer casts or real allow-lists. No account takeover: nothing
calls `wp_set_auth_cookie`, `wp_signon` or `wp_update_user` anywhere. Output
escaping was consistently right.

**What the sweep actually found was trust boundaries drawn one level too
generously** — a plugin-specific capability reaching a file-read primitive, a
captcha that does not survive contact with a script, a diagnostic dump printed
without redaction, an editor-preview route publishing an inventory core keeps
behind `activate_plugins`.

Six were fix-first, eleven more were real with a precondition, ten were
hardening, and eight further items turned up while closing the hardening tier —
including three term sweeps that were **deleting data that was in use**, which is
a data-loss bug rather than a security one.

**Which plugin each finding belonged to is deliberately not written down here.**
Every one is fixed and released, and each plugin's own changelog describes its
own fixes, so nothing is being hidden. What is withheld is the *collation*: an
index pairing a plugin with the flaw its previous release carried does the
sorting work for somebody targeting the installs that have not updated yet, and
install counts mean that is most of them for weeks after a release. Keep it that
way when adding to this section.

**Every new guard was mutation-tested** — the guard reverted, the suite re-run.
That caught four tests of mine that could not fail: a traversal fixture pointing
at a path that 404s either way, two flood tests whose `REPLACE` collapsed every
row into one, a cache probe reading a fixture an earlier run had left on disk,
and an e2e fixture that went through the sanitiser it claimed to bypass. **Write
the mutation step into any security fix from the start**; it is the only thing
that distinguishes a passing test from a test.

**The cross-cutting finding is worth remembering.** All nineteen carried a
Playwright storage state holding a `wordpress_logged_in_*` cookie, and twenty
workflows uploaded `artifacts/` wholesale on failure. The release rsync excluded
it, but that exclusion lives outside the repositories. The files are gone,
`bin/test-e2e.sh` cleans up on exit, and the workflows upload
`artifacts/test-results/` only.

## Closed 2026-08-09 — the i18n sweep

**Every user-facing string in the collection is translatable, and
`wp i18n make-pot` extracts 2,104 of them across the nineteen with zero
warnings.** That extractor run is the check worth repeating; it is ground truth
for malformed placeholders, wrong domains and conflicting translator comments in
a way no grep is.

What was wrong, in the order it matters:

* **Two strings were never translated at all** — wp-sweep's two
  `WP_CLI::success()` literals.
* **Seven were padded into uselessness.** A translator sees a msgid in a list,
  where a leading or trailing space is invisible. wp-email's Mail It button was
  widened with five spaces either side of its label; two of its validation
  messages ended in a colon and a space so a value could be glued on — while the
  server-side copies of those same two already used `sprintf`. wp-downloadmanager
  glued the site name to a feed title beginning with a space. wp-polls ended an
  alert in a space the script then doubled.
* **Four sentences were assembled from fragments** a translator cannot reorder:
  wp-pluginsused' summary joined by a bare "and" with the full stop in PHP,
  wp-stats' "Posted By … On …", and two in wp-print including a heading that
  wrapped the title in ASCII double quotes — which is not the quotation mark
  every language uses.
* **Thirty-seven translator comments said nothing**, all in wp-polls: they read
  `translators: %s: value.`, which satisfies the sniff — it only checks a
  comment exists — while telling a translator exactly what it does not need to
  know.
* **Nine bare words had no context.** `To`, `From`, `and`, `to`, `on`, `url`,
  `referral` across four plugins, now `_x()` with a context.
* **One number was locale-blind.** wp-serverinfo read the load average four ways
  and formatted it in only one of them, so the displayed shape depended on which
  branch the host took. All four now yield a float and it is formatted once,
  through `number_format_i18n()`.

**`test_no_translatable_string_carries_edge_whitespace()` is in the shared
metadata fixture**, so the padding class cannot come back. The other classes
were found by reading and a new one would need the same.

**Two things are left alone on purpose.** `wp-downloadmanager-quicktag.js` has
`l10n.label || 'Download'` — PHP localises that label translated and the literal
only shows if the whole localised object is missing, a state in which nothing
else on the screen works either. And `Domain Path: /languages` points at a
directory `test_no_abandoned_build_or_translation_artefacts_ship()` requires not
to exist: nothing calls `load_plugin_textdomain()`, translations come from
translate.wordpress.org into `WP_LANG_DIR/plugins/`, so the header is inert. It
stays because §3.2 mandates it and `test_text_domain_is_the_plugin_slug()`
asserts it, and because `Text Domain` is redundant by the same argument.

**Where translatable text can live is a closed set** — PHP, JavaScript, block
metadata and CSS `content:`. All four were swept. Block titles, descriptions
**and keywords** all reach the POT with their own contexts, because every
`block.json` carries `textdomain`; core wires `wp_set_script_translations()`
itself for the six blocks whose editor scripts import `@wordpress/i18n`, since
`wp-i18n` is in their asset dependencies. Nothing needs to call it by hand.

## Known and unresolved, 2026-08-09

**One wp-stats browser test failed once and the reason is not known.**
`page.spec.js` — *the General Stats block counts every kind of thing on the
site* — failed in a full local run and passed on re-run and in CI. It was not
reproduced: **both attempts to reproduce it were contaminated by running two
Playwright suites against one wp-env instance at the same time**, which is the
next entry.

What was fixed is the reason it could not be diagnosed. Every line in that block
is pluralised with `_n_noop()` and the two arms share no substring — "1 tag was
created." against "2 tags were created.", and the nickname line gains the word
"different" only in the plural. Four of the six locators were written against
one arm, so a count that was not the expected one matched **nothing**, and
Playwright reported a timeout waiting for an element. The patterns span both
arms now, so the next occurrence prints the number.

**Two E2E suites against one wp-env instance will destroy each other, and the
wreckage looks exactly like a data bug.** Thirteen tests failing across five
unrelated spec files, `2 pages were created.` where the fixture makes one.
`bin/test-e2e.sh` does not guard against it and `wp-env` does not either: the
ports are per plugin, so two runs *of the same plugin* share one database. Cost
about an hour and one wrong conclusion. Run one at a time, or reach for CI.

## Closed 2026-08-08 — the README audit, read as somebody installing the plugin

Nineteen READMEs, audited for whether the instructions are *true* and then for
whether they are *clear* — two halves that need completely different methods,
and both found something.

**Correctness is now mechanical.** Every backticked and bolded admin path,
split on its arrows, each segment checked against the strings the plugin
actually renders — that check is §3.3 in `verify.py`, and it reads JS as well
as PHP (a block's inspector labels live in `src/` and appear nowhere in the
PHP) and `_x()` too, or wp-sweep's own menu title reads as a fiction. It found
wp-polls sending readers through three wrong labels in one sentence, and
wp-postratings answering an FAQ with a **Ratings Colour** setting that has
never existed — both survived a whole major revamp. Shortcodes, functions in
examples, stable tags and the requirement headers were all clean already.

**Clarity, and nothing mechanical can do this.** Read cold, four descriptions
never said what the plugin is in the first sentence and were rewritten —
wp-polls (the flagship), wp-dbmanager, wp-showhide and wp-relativedate, the
last two also carrying typos nobody had noticed. **The check and the read find
different things and neither substitutes for the other**: the mechanical pass
cannot tell that a description says nothing; the read would never have caught
"Ratings Colour", a confident sentence about a plausible setting.

**`## Installation` is now required of all nineteen** — Lester's call,
overruling a proposal to require it only where there is a real first-run step,
because wordpress.org renders it as a tab and a tab missing on some plugins
reads as an omission. The move was worth more than the section: setup steps
were hiding in `## Usage` in five plugins and in `## Description` in wp-print,
and wp-dbmanager's "secure the backup folder" — the one step with a security
consequence — was the fourth bullet of a usage list.

**One thing checked rather than assumed:** these READMEs use markdown headings
where the wordpress.org format documents `== Section ==`, and the deploy does
not convert them. The live wp-print readme has used `##` for years, so the
parser handles it and nothing is missing.

## Closed 2026-08-08 — the blocks phase broke the metadata fixture two ways

Eight plugins gained blocks; five went red on PHPUnit while three stayed green.
**The green ones were the finding, not the red ones.** Both fixes are in the
shared fixture, copied to all nineteen, and §6 and §7.2.1 carry the full
reasoning; what stays here is the shape of the two causes.

**Cause (a) — §6's dependency rule predates blocks.** A block's editor script
dependencies are written by the build, and that is not a §6 violation, it is
what a block is — §7.2.1's *a metadata rule written before X will fire on X's
scaffolding*, answered the same way: widen the rule, do not move the file. For
block scripts only, every dependency must be a handle WordPress itself
registers **and none may be jQuery** — core ships `jquery`, so "core provides
it" alone would reopen the one door §6 exists to close.

**Why three plugins passed anyway, which is the worse half.** The fixture read
`wp_scripts()->registered`, a process-wide global those three plugins' own
`set_up()` methods null or replace — so the loop ran against nothing and
passed, and **wp-polls shipped a block through six green PHPUnit rows on the
identical dependency array that failed wp-postratings**. The fixtures had not
drifted; the plugins' `set_up()` methods had. The block half is now read off
disk, from the `build/*/*.asset.php` manifest the build wrote and the release
ships — same answer in every plugin and every run order, verified by breaking
it deliberately in wp-showhide, the plugin where the old assertion saw nothing.

**Cause (b) — firing `init` twice re-registers the blocks**, which is a
`_doing_it_wrong()` notice, which this suite turns into a failure. **The guard
was deliberately not put in the plugin** — a second registration in production
would be a real bug and a guard would swallow it; the test's one-process
simulation is what is imperfect, so `fire_init()` empties the block registry of
the plugin's own blocks first, the state a real second request starts from.
Anything that re-fires `init` goes through it.

## Closed 2026-08-08 — wp-polls' widget warned on the front end

`WP_Polls_Widget::widget()` read three `$instance` keys with no defaults and no
guard, so a partial instance printed `Warning: Undefined array key` into the
middle of the rendered page. **The count is what made it a defect rather than a
style note**: seven plugins ship a `WP_Widget` subclass, five parse `$instance`
against defaults, wp-useronline guards every read — wp-polls was the only one
of the seven doing neither. One copy of a pattern drifting while every tool
stays green, **found by looking at a screenshot of the widget**, not by any
suite: the same shape as §7.6.1 and worth the same conclusion — a rule nothing
checks is a rule some copy has already drifted from.

**Fixed 2026-08-08** the way the five siblings do it — a `defaults()` method
read by *both* `widget()` and `form()`, so the two cannot disagree about what
an unset key means — and pinned by two tests, one rendering an instance with no
keys at all and asserting on the *warning* rather than the markup.

**Two things were deliberately not done.** `update()`'s return-false-without-
submit guard is a three-plugin pattern rather than wp-polls drift, and changing
it is a behaviour change nobody asked for. And **no `verify.py` rule was
added**, though "every `widget()` parses its instance against defaults" is
mechanical and there are seven copies of it. That rule is worth writing; it is
not written.

## Remaining work

**The list is empty.** Item 1 — WP-CLI, REST and blocks — closed 2026-08-08;
item 2 — the screenshots — closed the same day, and its SVN half shipped with
the 2026-08-10 releases. What follows is the findings the two items produced,
kept because they bind anything built on these surfaces; the instructions are
spent and gone.

### Item 1 findings — WP-CLI, REST and blocks, closed 2026-08-08

**Every plugin in §13.4.4's scope has its surface.** Commands and namespaces
across the scope — wp-sweep already had both — with wp-email excluded from REST
by Lester's call (§13.4.5 says why, and says not to finish the job later).
**Twelve blocks in eight plugins**: wp-polls (`poll`, `page-polls`),
wp-downloadmanager (`download`, `page-download`), wp-pluginsused (three), and
one each in wp-postratings, wp-postviews, wp-useronline, wp-stats and
wp-showhide. The scope reasoning, the naming (slug without the `wp-` prefix)
and the three deliberately unclaimed names all live in §13.3–§13.4; this file
no longer restates them.

**wp-polls was the reference and §13.4.10 is what the other seven inherited** —
the toolchain cost the time, not the blocks. **Read §13.4.10's last paragraph
before the next phase of anything**: every one of the seven deviated from the
reference somewhere, and every deviation was right — wp-showhide needed
`InnerBlocks` because `[showhide]` encloses; four plugins correctly did not
copy `block_editor_styles()` because they ship no CSS; wp-useronline correctly
refused wp-polls' "block and shortcode on one page" test, which would have
**passed** while asserting a duplicate DOM id. Uniformity would have bought a
green test standing guard over a bug.

Findings that bind anything built on these surfaces:

* **A refusal answers 403, not 400** — Lester, 2026-08-08, written up as
  §13.4.6a. A client cannot tell from a 400 whether retrying differently would
  help.
* **How an AJAX handler reports its outcome decides how hard REST is.** Answer
  JSON or throw on refusal and it ports cleanly; return-or-echo a string either
  way and it does not port at all. wp-postratings' `process_vote()` and
  wp-email's `process()` were the third kind and were fixed first — refusals
  that deliberately say nothing to a visitor throw with an **empty message** so
  the browser path is unchanged. And wp-email needed three outcomes where two
  looked obvious: a delivery the mailer refused is not a failed validation, and
  folding them together handed the form back to somebody whose message had
  simply bounced. `invalid`, `failed` and `sent` are distinct.
* **wp-useronline is the one to read before writing the next command**, because
  consistency pressure would have produced both of its mistakes. It takes no
  nonce and must not — anonymous nonces come from one session every logged-out
  caller shares, so a nonce cannot authenticate a visitor; two tests pin the
  *absence*. And its command reads and never writes, because the admin offers
  no destructive action; a test asserts no such subcommand exists.
* **A second entry point surfaces old bugs.** wp-downloadmanager's
  `download_shortcode()` compared `0 !== $id` strictly against what
  `shortcode_atts()` returns — a string — and wp-stats gated its stylesheet on
  `has_shortcode()` alone, so a block-only page loaded no CSS. Both found by
  the identical-markup assertion earning its place.
* **Three `verify.py` checks came out of the batch**, each found by an agent
  rather than the checker: every include guards against direct access (wp-polls'
  own blocks class was the only one of eighteen without it); §13.4.7's blocks
  row is enforced like the CLI and REST rows; a block plugin's runners must
  invoke `bin/build`. All mutation-tested both directions.
* **`--format=ids` printed `Array` per row in six plugins**, with a documented
  pipe built on it — under "Tests that cannot fail", because the reason every
  suite stayed green is structural.
* **`WP_Polls_Poll` exists because the admin handler interleaved `$wpdb` calls
  with the notice markup announcing them**, so a second caller could only copy
  the queries. The extraction removed three assignments never read — one a
  query for `poll_latestpoll`, a row the 3.0.0 migration deletes, so the branch
  had been reading nothing for a whole major version.
* **The `admin-ajax.php` actions stayed registered**, per §13.4.2 — a theme or
  cached script calling one is in the same position as a post containing a
  shortcode, so each route was added beside its action, not in place of it.

### Item 2 findings — the screenshots, closed 2026-08-08

71 images across all nineteen, taken against the rebuilt admin, every
`## Screenshots` list rewritten to match, reviewed and accepted by Lester —
including the ten plugins thinner than the old set, whose old counts described
a UI that no longer exists. The files went out with the 2026-08-10 releases,
committed from `assets/` through the skill's screenshots step, which also
`svn rm`s every image the new readme no longer captions.

**Every caption was later checked against its image, and seven were wrong** —
miscounts, the wrong tab, the right number of the wrong thing, and worst,
**controls that exist nowhere** (wp-draftsforfriends' "shareable statuses",
wp-pluginsused' "where it links"): the class that costs a user real time,
because they install expecting a setting no screen offers. The method that
worked: read the sentence, then check any claim it makes against the code —
`grep -c add_settings_field` settled three in seconds. A claim with a number in
it is worth checking; a claim naming a screen is worth checking harder. The
seeded post bodies also named sibling plugins, so two screenshots advertised
the wrong plugin; `seed.php` is neutral now and both were retaken.

**Two findings outlast the images.** *Count-matches-README is not coverage*:
the check that passed on all nineteen throughout only proves captions line up
with files, and passes on any number including one too small — a person looking
is what found the gap. And *a subagent's account of its own work is not
evidence*: this one reported a git fix as blocked when the reflog showed it had
succeeded, and following its instructions would have duplicated a commit.
Check the repository, not the report.

**Off this list on purpose:** the SVN release itself. Lester does it by hand;
nothing here pushes, tags or touches SVN. **Reading the diffs for voice is off
it too** — a decision, not an oversight: the mechanical half is checked on
every push, what was left was a human read nobody could pick up, and what it
*measured* is kept under "Rules earned the hard way".

## Closed on 2026-08-05 — the eleven migration suites

**Every migrating plugin now has a browser test of its migration.** Fifteen
migrate; all fifteen have a green `tests/e2e/upgrade.spec.js`, the last eleven
written on 2026-08-05 — 78 tests, each run to green before it was committed.
The findings none of which reading the code would have produced — a `wp eval`
call is a full WordPress request, a scalar legacy row reads back as a string,
and **wp-downloadmanager's legacy row wins over an existing current row**,
pinned in both directions because the wrong reading is the plausible one — are
folded into the E2E lessons below. One more belongs here: **a blocking
`execFileSync` inside a test cannot be interrupted by Playwright's timeout**,
so a slow helper reads as a hang rather than a failure — two runs were
abandoned on that before machine load turned out to be the cause, and the same
suite that took an hour under load took two minutes without it.

wp-commentnavi's and wp-pagenavi's were confirmed by mutation, run separately
rather than one assumed from the other: three of seven tests went red in each.
The other nine rest on the collection's usual guard — every one failed at least
once on its first run and was fixed, the same evidence in a less deliberate
form.

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

**All nineteen are tagged and pushed**, so every plugin has a ref for "as it
shipped before this work". `git -C <plugin> tag` is the authority; the table
that used to sit here restated nineteen commit hashes git already holds.
A one-off script created them, and it is gone now that they exist. The one
thing worth carrying forward if it is ever rewritten: it refused to guess rather
than tagging a shallow clone that was missing the commit.

**It had to run from Lester's machine.** The sandbox's git proxy answers a tag
push with HTTP 403 while allowing branch pushes, which is why this sat waiting
rather than being finished when it was written.

Three findings outlived the tagging itself:

* **wp-email shipped with its header behind its `Stable tag`.** At `066014a9`
  the header read 2.69.2 and the `Stable tag` read 2.69.3, so wordpress.org
  served that tree as 2.69.3 while every site running it reported 2.69.2 — a
  standing update prompt that never clears. It had happened once before, at
  2.69.0/2.69.1.
* **Five plugins carried `Stable tag: trunk`**, not four: freemyinternet,
  wp-commentnavi, wp-draftsforfriends, wp-pluginsused and wp-relativedate. §14
  said four until this was found. Settled by the 2026-08-10 releases: all five
  now have a real version tag and a numeric stable tag.
* **Two repositories already carried tags and an earlier draft said none did.**
  wp-pagenavi has six and wp-useronline four, bare version numbers from scribu's
  tenure. The claim was never checked against `git tag` — prose about a number
  nothing measured.

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
  committed; see "Closed on 2026-08-05". **Wall clock was the whole cost**: the
  same six-test suite takes two minutes on an idle machine and over an hour
  with a dozen wp-env stacks up, because almost all of it is
  `npx --yes @wordpress/env run` startup rather than browser time.

* **2026-08-09/10** — **all nineteen released to wordpress.org** through the
  `release-wp-plugin` skill: pre-flight, staged trunk, live-site verification on
  lesterchan.net, trunk commit and tag, screenshots committed from `assets/`.
  The final audit found §7.6.2's guard missing from six plugins and a
  category-sanitiser defect in wp-downloadmanager; see "Closed 2026-08-10". The
  releases were preceded by the two incidents now recorded in the skill and
  under Traps — the emptied wp-ban trunk (2026-08-08) and the live-site
  `git reset --hard` that reverted seven migrated plugins (2026-08-09).

The programme found roughly **twenty-five spec bugs and eleven `verify.py`
bugs**, every one because an agent pushed back rather than complied. The pattern
that made it work: one plugin finds it, fix it centrally, the other eighteen
never see it.

