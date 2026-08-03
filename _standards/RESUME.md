# Resume here

State of the consistency programme as of **2026-08-03**. Read this, then
`_standards/STANDARDS.md`, which is the contract everything else follows.

**In one line:** all nineteen plugins are green on CI, the bug backlog is empty,
and the only substantial work left is a phase that has not started (WP-CLI, REST
and blocks).

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

* `_standards/STANDARDS.md` — the spec. 15 sections.
* `_standards/BRIEFS.md` — the agent launch kit: a reusable preamble, the
  identity table, and a per-plugin section recording what the survey found in
  that repo. Survey knowledge that exists nowhere else and is expensive to
  re-derive.
* `_standards/templates/` — the files each plugin copies verbatim, placeholders
  `{{SLUG}}` `{{NAME}}` `{{CLASS}}` `{{UNDER}}` `{{UPPER}}` `{{L10N}}`
  `{{DESCRIPTION}}`.
* `_standards/E2E-SWEEP-2026-08-02.md` — the full per-plugin E2E sweep report,
  1,078 lines. Every bug in it is fixed; it is kept for the detail.
* `.wp-env.json` — all 19 plugins in one WordPress on 8888/8889.
* `bin/verify.py` — mechanical checker, ~40 rules per plugin.
  `python3 bin/verify.py [slug…] [--quiet]`. Exit status is the failure count.
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

## Current state — verified 2026-08-03

* **CI green on all 19**, checked run by run rather than assumed.
* `verify.py` 0 across all 19.
* PHPUnit green single site and multisite; Playwright green.
* **7,860 of 7,860 assertions carry a failure message** (was 3,360, 42.7 %).
* The permalink audit of the E2E suites is complete — see below.
* No known plugin bug is outstanding.

## Remaining work, in order

Nothing here blocks a release.

1. **WP-CLI, REST API and Gutenberg blocks across the collection.** The only
   substantial item, and a phase of its own rather than a cleanup. `wp-sweep`
   already has `WP_Sweep_Command` and `WP_Sweep_API` and is the reference; §13.3
   pins the naming (`wp wp-sweep`, `wp-sweep/v1`) and the reason — the bare
   nouns it replaced were names any plugin could have claimed, and neither
   WordPress nor WP-CLI detects the collision.

2. **Read the diffs for voice.** The mechanical half is done and closed. What
   is left is a human read, and the measurements below say where *not* to spend
   it.

   **Comment density is not a defect signal in this collection, and two
   successive attempts to make it one were both wrong.** Recorded because the
   error is easy to repeat:

   * *Raw comment share* rates wp-polls worst (35.6 % against wp-postratings'
     46.6 % at nearly the same size). wp-polls is in fact among the best
     explained plugins here. Its share is low because it carries a lot of code
     per docblock.
   * *Counting only `//`* rates wp-relativedate worst in the collection, at 0.4
     per 100 lines. It is second **best** at 15.4. The plugin explains itself in
     `/* … */` blocks, which a `//`-only counter files as docblocks. wp-pluginsused
     moved from second-worst to fifth-best for the same reason.

   Measured properly — inline `//` plus non-docblock `/* */`, against code lines
   — the collection spans 6.8 to 16.0 per 100, and **the low end is correct**.
   wp-email's least-commented file is a `WP_Widget` subclass with 80 lines of
   code and no inline explanation at all, because nothing in it is surprising.
   Counting cannot tell "under-explained" from "nothing to explain"; only
   reading can.

   The mechanical half, all clean: **1,871 functions across all nineteen have a
   docblock**, every file has a file-level docblock, and `@package` is the
   display name everywhere. That last one was a real find — four plugins
   (wp-useronline, wp-postratings, wp-draftsforfriends, wp-sweep) carried the
   lowercase slug in their older files and the display name in their newer ones,
   splitting each plugin along age rather than meaning, and canonicalisation
   walked past it because nothing compared the halves. `verify.py` checks it now.

3. **One open API question**, left deliberately for a collection-wide decision:
   whether wp-draftsforfriends gains `wp_draftsforfriends_share_created` /
   `_extended` / `_revoked` actions and a `_share_url` filter. New public API on
   a plugin that has never had any cannot be withdrawn once shipped.

4. ~~**Sweep for assertions whose two operands are both literals.**~~ **Done
   2026-08-03. One finding across all nineteen**, in wp-downloadmanager:
   `assertTrue( true )` standing in for "serve() returned rather than ending the
   request". Reaching the line was the real assertion, but that form would also
   have passed if `serve()` printed an error on the way out — so it now captures
   the output and asserts it is empty.

   **A constant is not a literal.** The first pass counted `WP_SHOWHIDE_VERSION`
   and `self::PER_PAGE` as literals and reported 73 findings, nearly all of them
   `assertSame( '3.0.0', WP_SHOWHIDE_VERSION )` — which is a real test, because
   the constant comes from the code under test. Only values written *in the
   test file* count. Scope `foreach` sources per method too, or a literal array
   in one test makes the next test's variable look literal.

**Off this list on purpose:** screenshots into `~/svn/wordpress_plugins/…/assets/`
and the SVN release itself. Lester does both by hand. Nothing here pushes, tags
or touches SVN.

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

## Rules earned the hard way

* **`register_setting()` attaches two things to the settings row, and
  activation and WP-CLI run neither** — a `sanitize_option_*` filter, and, where
  a `default` is passed, a `default_option_*` filter that answers `get_option()`
  with the shipped defaults for a row that does not exist. Every migration that
  reads or writes through the bare `get_option()`/`update_option()` pair is
  therefore correct under WP-CLI and wrong on the one path a real update takes.
  Written up as **§7.6.1**. **Any migration test that only runs under WP-CLI is
  testing the easy path.** Four variants were found across five plugins.

* **One list must not drive both the migration and uninstall.** Both §13.2
  shared-row violations (wp-polls, wp-downloadmanager) were that design: the
  single list is what stops a row the plugin owns drifting off the uninstall
  list, and both had a row they never owned on it. Each fix is pinned by two
  tests — the contract (absent from the uninstall list) and the behaviour (a
  seeded row survives) — because a test that walks the single list cannot see
  the defect. **Do not fold the lists back together.**

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
  violations. Report at `_standards/E2E-SWEEP-2026-08-02.md`.
* **2026-08-03** — CI reconciled with local for the first time (the permalink
  divergence above); assertion messages taken to 7,860 of 7,860; the metadata
  fixture held to its template; two tests that could not fail replaced.

The programme found roughly **twenty-five spec bugs and eleven `verify.py`
bugs**, every one because an agent pushed back rather than complied. The pattern
that made it work: one plugin finds it, fix it centrally, the other eighteen
never see it.
