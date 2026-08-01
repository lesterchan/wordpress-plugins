# Resume here

State of the consistency programme as of 2026-07-28. Read this, then
`_standards/STANDARDS.md`, which is the contract everything else follows.

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
| Root of this folder | **Tracked since 2026-08-01**: `github.com/lesterchan/wordpress-plugins`, branch `main`, holding `_standards/`, `bin/`, `.wp-env.json` only. The 19 plugin directories are gitignored by name — each is its own repo on `master`. |
| Commit signing | **None.** Use `git commit --no-gpg-sign`, despite the global `commit.gpgsign = true`. Existing history is unsigned and stays that way. |
| Supported floors | **WordPress 6.8, PHP 8.2** — raised from 6.0 / 7.4 on 2026-07-28, *after* the agents ran. See §1.1. |
| Version markers | Own row `{{UNDER}}_version` = `array( 'plugin' => …, 'db' => … )`, **never** inside the settings array. See §2.1 for why. |
| RTL | No `*-rtl.css` anywhere; CSS logical properties instead (§5.1). |
| README Contributors | Exactly `GamerZ`, every plugin. wp-pagenavi loses `scribu`. |

> **The floor change landed after the fan-out**, so the ten finished plugins
> carry WP 6.8 / PHP 8.2 in all six places and the untouched ones do not.
> `verify.py` flags the latter until they catch up — expected, not a
> regression. Per §1.1, also delete any now-dead back-compat shim for PHP < 8.2
> or WP < 6.8 rather than leaving it unreachable.

> **The 2026-07-28 fan-out below is history.** All 19 were reset clean and the
> work restarted; jump to "Session of 2026-07-29" for the live state.

## What exists

* `_standards/STANDARDS.md` — the spec. 15 sections.
* `_standards/BRIEFS.md` — **the agent launch kit.** A reusable preamble, the
  identity table (name / class prefix / port / JS / version), and a per-plugin
  section recording what the survey found in that specific repo: which files are
  loose, where jQuery hides, which hooks rename, which constants are deliberate.
  Launch an agent with the preamble plus that plugin's section. This is survey
  knowledge that exists nowhere else and is expensive to re-derive — do not
  write fresh prompts from scratch.
* `_standards/templates/` — 15 files each plugin copies verbatim, placeholders
  `{{SLUG}}` `{{NAME}}` `{{CLASS}}` `{{UNDER}}` `{{UPPER}}` `{{L10N}}`
  `{{DESCRIPTION}}`.
* `.wp-env.json` — all 19 plugins in one WordPress on 8888/8889.
* `bin/test-all.sh` — every plugin's PHPUnit suite in that one container.
  `--multisite` for the network run. Keeps going past failures.
* `bin/verify.py` — mechanical checker, ~40 rules per plugin. `python3
  bin/verify.py [slug…] [--quiet]`. Exit status is the failure count.

## Where the work got to

19 agents were run, one per plugin, each applying STANDARDS.md §15 to its own
repo. They were told **not** to start Docker (19 concurrent wp-env stacks is not
survivable), so they ran `phpcs`, `php -l`, `eslint` and `vitest` but **not**
PHPUnit.

All 19 agents were stopped before committing, except **freemyinternet**, which
finished and committed at `2a2eaf7`. The other 18 repos hold uncommitted,
**possibly half-applied** work — an interrupted rename leaves a plugin broken in
a way `phpcs` will not catch, because phpcs checks style, not references.

### Decision: discard it and restart fresh

Lester chose to **restart the fan-out from scratch** rather than resume the
stopped agents or salvage the dirty trees. So step 1 is to reset the 18:

```sh
cd ~/git/wordpress_plugins
for p in wp-ban wp-commentnavi wp-dbmanager wp-downloadmanager \
         wp-draftsforfriends wp-email wp-pagenavi wp-pluginsused wp-polls \
         wp-postratings wp-postviews wp-print wp-relativedate wp-serverinfo \
         wp-showhide wp-stats wp-sweep wp-useronline; do
  git -C "$p" reset --hard HEAD && git -C "$p" clean -fd
done
```

`reset --hard`, **not** `checkout .` — the agents used staged renames, and
`checkout .` restores the working tree from the index, leaving every `git mv`
in place. It looks like it worked and does not.

Confirm every one reports `dirty=0` afterwards, then relaunch one agent per
plugin against the **current** spec.

**Done 2026-07-29.** All 19 were reset clean.

## FAN-OUT COMPLETE — 2026-07-30

**All 19 plugins pass `bin/verify.py`: 0 failing checks, every tree clean.**
Collection-wide the count went 961 → 0. No two plugins claim the same option row.

Every plugin now has: the shared `phpcs.xml`, `ci.yml`, `.editorconfig`,
`.gitignore` and both PHPUnit configs byte-identical to `_standards/templates/`;
`WP_`-prefixed classes in `class-wp-*.php`; one `{{UNDER}}_options` row (or none,
for the two settings-less plugins) plus `{{UNDER}}_version` holding `plugin` and
`db`; `{{UNDER}}_*` hooks; WP 6.8 / PHP 8.2 in all seven places; Settings API
admin screens with `WP_List_Table` where tabular; no jQuery; no `*-rtl.css`; no
shipped raster images; the fourteen shared metadata tests.

### PHPUnit HAS now run — single site, 2026-07-30

Full log: `_standards/SWEEP-2026-07-30.log`. ~4,000 tests, ~13,000 assertions.
**5 of 19 green** (freemyinternet, wp-ban, wp-polls, wp-relativedate,
wp-showhide); 14 with fallout, since fixed down from ~80 issues.

Two causes dominated, and neither was visible to phpcs or to inspection:

* **PHP 8.2 dynamic properties.** One undeclared `private $mail` in
  wp-email's form test failed all 41 tests in that class. Fixed by declaring it.
  Only bites because the floor moved to 8.2 *and* the shared config sets
  `convertDeprecationsToExceptions`.
* **`rtrim(): Passing null`** — 19 errors in wp-print, stack inside WordPress
  core (`comment-template.php:1613` → `formatting.php:2840`) reached from
  `includes/print-posts.php:118`. A genuine PHP 8.1+ incompatibility the old 7.4
  floor hid.

The rest are individual assertions, and a notable share are each plugin's **own**
new standards tests failing — `§4.1 wants the data screen first and Settings
last`, `Section 4.2 allows zero hand-written form tables`, `the downloads table
is dropped by uninstall`. Those assert the standard correctly; the code does not
yet comply. Treat them as findings, not as broken tests.

**Multisite has still not been run** — `bash bin/test-all.sh --multisite` is the
other half, and uninstall/network-activation paths are where the family has
historically broken.

### ALL 19 PASS PHPUNIT — single site, 2026-07-30

`bash bin/test-all.sh` exits 0. ~3,900 tests, ~11,700 assertions, every tree
clean, `verify.py` 0, phpcs 0 everywhere. Log of the first run:
`_standards/SWEEP-2026-07-30.log`.

**Five real behavioural bugs were found and fixed**, all new in the unreleased
majors so no Upgrade Notice was owed. All five verified present in the code and
pinned by a test:

1. **wp-downloadmanager Add File ignored its own source radio** —
   `handle_add()` passed a hardcoded `0` instead of the posted `file_type`, so an
   upload or a remote URL was accepted by the form and then discarded, the row
   written from whatever Browse held. `handle_edit()` always read the field.
   Most user-visible bug in the programme. Pinned by
   `test_adding_a_remote_file_stores_the_url_it_was_given`, which I confirmed
   fails when the hardcoded `0` is put back.
2. **wp-print activation discarded every legacy setting** — `activate_site()`
   seeded defaults into `wp_print_options` *before* the migration, and the
   migration lets an existing value win, so a site upgrading from 2.58.3 had its
   `print_options` row read, deleted and thrown away. Order swapped; pinned by
   `test_activation_runs_the_migration`.
3. **wp-downloadmanager widget fatalled on any partial save** (block editor,
   customizer, first save) — six keys read unguarded. Pinned by
   `test_the_widget_keeps_edits_made_without_the_legacy_submit_marker`.
4. **wp-draftsforfriends** cleaned an absent duration to 1 second rather than the
   shipped two hours. Pinned by
   `test_the_sanitiser_reads_nothing_back_out_of_the_database`.
5. wp-print's activate/migrate swap also makes `add_option()` the no-op on a
   legacy install rather than the thing that wins.

**The single largest cause** of the second-round failures was one thing:
`WP_UnitTestCase_Base::tear_down()` nulls `$wp_stylesheet_path`, and
`comments_template()` reads it straight into `trailingslashit()` instead of
re-deriving it as `locate_template()` does — so it hands `null` to `rtrim()`.
**23 of 35 failures**, across wp-commentnavi and wp-print. Harness-only; the fix
restores the precondition via `wp_set_template_globals()`. Written up as §7.2.1
along with the process-wide-state traps and the
`add_menu_page()`/`add_submenu_page()` capability asymmetry.

**Task 6 (Upgrade Notice audit) is done.** All 19 stopped claiming what the
reader upgrades *from*: the released readmes declare WordPress 2.8-5.5 and
**fifteen of nineteen declare no `Requires PHP` at all**, so "up from 6.0 and
7.4" was wrong nearly everywhere, and "if your host still runs PHP 7.4" told a
reader who might be on 5.6 that they were fine. See §14.1.

### DONE: the multisite sweep (2026-07-30)

`bash bin/test-all.sh --multisite` is green across all 19. ~3,950 tests.
wp-postviews reports one deliberate skip (`test_uninstall_removes_only_our_data`
— the network branch is covered by `WP_PostViews_Multisite_Test`).

**The harness was lying, and that is the finding to remember.** The first run
reported wp-sweep as passing when it had died at test 96 of 384: a test reached
the real `wp_send_json_error()`, whose `die()` took the PHP process down
mid-run **with status 0**. 46 tests had already errored. `bin/test-all.sh` now
requires PHPUnit to have printed a verdict and treats its absence as a failure —
see §7.2.3. Do not remove that check.

Seven plugins failed. Five failed for one shared reason: **capabilities do not
mean the same thing on a network** (§7.2.2 now has the table). In every case core
was right and the test was wrong; the temptation to weaken a gate to make a test
pass would have handed network-level power to every site administrator on every
network — wp-dbmanager's Run SQL Query console being the worst case.

Two were real plugin bugs, both now fixed and pinned:

* **wp-downloadmanager** read `activate_plugins` as its proxy for "level 10", so
  on every network each site's administrator silently dropped to level 7 and lost
  the level 8–10 downloads on their own site. Now `manage_options`.
* **wp-useronline** hardcoded `edit_users` outside its own capability filter, so
  a site administrator on a network could not see the visitors to their own site
  and no site could correct it. Now `capability( 'details' )`.

Two were wrong claims in comments, corrected in code and test:

* **wp-polls** asserted `! function_exists( 'wp_get_sites' )`. That function was
  never removed — it is deprecated and still ships in `ms-deprecated.php`, loaded
  for multisite only — so the assertion passed single-site for the wrong reason.
  The old call did not fatal; it activated on only the first 100 sites.
* **wp-commentnavi** asserted the `cpage=` substring, which is really asserting
  "this install has plain permalinks". Now compares against the link core builds.

Predictions from the previous session that did **not** materialise: the three
`is_multisite()`-guarded classes all passed first time, and no table-owning
plugin hit the `SHOW TABLES` problem.

Still true and still worth knowing:

* wp-draftsforfriends' bootstrap logs real `Table 'wp_draftsforfriends' doesn't
  exist` errors during `_delete_all_posts`, because
  `WP_DraftsForFriends_Shares::delete_for_post()` is hooked to `deleted_post` and
  fires before the table exists.
* `bin/test-all.sh` triggers a wp-env deprecation about
  `testsEnvironment`/`env`/`testsPort`. §10 pins that `.wp-env.json` shape in all
  19, so it will need changing together when wp-env drops them.

### What is NOT done
2. **Tasks 5, 7 and 8 are untouched**: read the diffs for voice and comment
   density (`verify.py` cannot see those), capture screenshots into SVN assets,
   and add failure messages to inherited assertions. On that last one, the
   measured gap is **4,847 of 6,845 assertions (70.8 %)**, and it is very
   unevenly spread — freemyinternet is at 0 %, wp-useronline 15 %, but wp-email
   is 94.9 %, wp-dbmanager 86.7 % and wp-print 83.9 %. freemyinternet is the
   reference for what "done" reads like. Do it as one uniform pass, not per
   plugin, and do not write filler: a message is owed where the failure would
   otherwise be unreadable.

3. **Three new asks from Lester, 2026-07-30** (tasks 10 and 11 in the tracker):
   * **Audit every plugin's migration path from the released SVN version to the
     pending major for data loss, and pin it with tests.** The shape to hunt: a
     `sanitize()` that rebuilds the array from defaults will silently drop any
     legacy key the migration did not rename *first*, so check rename-then-
     sanitise ordering. Also defaults masquerading as migrated values (the
     wp-print `activate_site()` bug), `delete_option()` before the read, and
     partial merges that lose nested keys. Dedicated migration suites already
     exist in wp-ban, wp-downloadmanager, wp-polls, wp-postviews, wp-pagenavi and
     wp-postratings; thinnest coverage is wp-relativedate, wp-draftsforfriends,
     wp-showhide, wp-sweep and wp-commentnavi.
   * **Playwright E2E across all 19** using `@wordpress/e2e-test-utils-playwright`
     — every wp-admin screen as every relevant role, plus front-end interaction
     and display. Decide first: shared root config vs per-plugin, and how it
     joins `ci.yml`. It may well subsume the screenshot task.
   * Confirmed for the record: each plugin is its own repo with its own
     `ci.yml`, `on: push` to master and on any `pull_request`, so a push runs
     only that plugin's checks.
4. **One open API question**, deliberately left for a collection-wide decision:
   whether wp-draftsforfriends gains `wp_draftsforfriends_share_created` /
   `_extended` / `_revoked` actions and a `_share_url` filter. New public API on
   a plugin that has never had any cannot be withdrawn once shipped.

### How this went, for whoever runs the next programme like it

The spec was wrong in about **twenty-five** places and `verify.py` had **eleven**
bugs. Every one was found by an agent pushing back rather than complying, and the
pattern that made it work was: one plugin finds it, fix it centrally, the other
eighteen never see it. The pilot alone paid for itself ten times over.

The things that mattered most:

* **Commit after every step.** Two sessions died mid-flight. The first, with no
  checkpoints, lost 18 plugins' work. The second lost one step each.
* **Prefer a mechanical check to a spot-check.** Adding a `verify.py` rule for
  §4.2 immediately caught two plugins putting `add_settings_field()` on the wrong
  class — drift no human review would have seen. Same for the `phpcs.xml` and
  `ci.yml` identity checks, which caught 13 plugins between them.
* **Two invalid-XML bugs and a `composer.lock` mismatch** would each have broken
  CI before a single test ran, and none were visible to phpcs.
* **Watch for rules that cannot be satisfied.** §9's ban on inline suppressions
  was reversed twice before landing on: fix the code, put collection-wide sniffs
  in the shared ruleset, and require a reason on the residue.

### Spec fixes the pilot earned

### Spec fixes the pilot earned — all already applied

The pilot's job was to find spec bugs, and it found ten. Applied to
STANDARDS.md: `composer.lock` added to the §1 layout; §3.3's "no others" scoped
to h2 only; `### Donations` mandated with one exact wording; §2.2's `GROUP` /
`PAGE` / `CAPABILITY` marked screen-only; §7.2 declared authoritative over
wp-showhide's older file; §15 ruled that N/A steps produce no commit; sample
versions changed to `{{VERSION}}`; and the settings-row exemption above.

**The licence fix matters most.** §3.1 had mandated wp-showhide's GPL block,
which is v2-**only** — contradicting the `GPLv2 or later` header directly above
it and `GPL-2.0-or-later` in composer.json. 14 of 19 already use the correct
"or later" wording; §3.1 now mandates that, and the five v2-only plugins
(including wp-showhide) must be brought into line, never the reverse.

`verify.py` also gained two checks it was missing: `tests/index.php` (the walk
skipped `tests/` entirely) and README h2 **order** plus rejection of
non-canonical h2s.

### Calibration from the pilot

~30 tool calls and about half a comfortable budget — on the **smallest** plugin,
where §15 steps 5–9 were all no-ops. Roughly 60–70k tokens of that is fixed cost
every agent pays re-reading the spec, templates and its own plugin. **A plugin
that actually exercises steps 5–9 will cost 3–5×.** Put no more than **two** of
wp-downloadmanager / wp-polls / wp-postratings in a batch.

**freemyinternet is the exception — do not reset it.** Its commit is good work
and stands. `python3 bin/verify.py freemyinternet` reports **10 failures, every
one of them the floor change it predates** — the six places from §1.1: plugin
header (×2), README header (×2), `phpcs.xml`, `composer.json`, `.wp-env.json`,
and the CI matrix (×3). Mechanical editing, not a redo.

Nothing else in the spec changed after its agent ran: it already had the settled
version-marker rule, §5.1 RTL, the Contributors rule, the §13 WP-Stats contract
and the fourteen shared tests, and §14 does not move it off 1.0.0.

**But `verify.py` only covers the mechanical half.** It cannot tell whether the
Settings API rewrite is real or cosmetic, whether the comment density matches
its siblings, or whether the Upgrade Notice reads like the same author. So:
**read freemyinternet's diff in the verification pass with the same scrutiny as
the other 18.** If the review shows its voice or its admin work is off, reset it
*then* — on evidence, not suspicion.

Why fresh rather than resumed: those trees were built against two rules that
have since changed — version markers used to live inside the settings array, and
the floors used to be 6.0 / 7.4. Salvaging is more expensive than redoing, and
riskier, because a half-applied rename looks clean to every tool we have.

## How to run the fan-out on a limited token budget

The first attempt ran all 19 agents at once and the session ended with 18 trees
half-applied and nothing salvageable. Do not repeat that. Three rules:

**1. Agents commit after every step, not at the end.** This is now §15 step 13
and it is the single thing that makes an interruption survivable. `git log` in
each repo becomes the progress tracker — messages are prefixed `Step N: …`.

**2. Run in batches of 3–4, not 19.** Wait for a batch to finish and commit
before launching the next. When tokens run out, the finished plugins are
committed and done; only the in-flight batch is affected, and thanks to rule 1
even those are resumable from their last checkpoint.

**3. Order: one pilot, then largest first.**

| Batch | Plugins | Why |
|---|---|---|
| Pilot | wp-relativedate | Smallest. Validates the spec end-to-end cheaply — if §1.1, §2.1 or the shared tests are wrong, find out here, not on the big ones. |
| 1 | wp-downloadmanager, wp-polls, wp-postratings | The three heaviest (74 / 59 / 60 files last time). They need the largest contiguous budget, so spend it while you have it. |
| 2 | wp-email, wp-dbmanager, wp-useronline, wp-stats | Mid-size; wp-stats and wp-email carry the §13 contract. Run **wp-stats in this batch or earlier** — it defines `wp_stats_sections`, which six others consume. |
| 3 | wp-ban, wp-print, wp-postviews, wp-draftsforfriends | Mid-size, JS-bearing. |
| 4 | wp-commentnavi, wp-pagenavi, wp-sweep, wp-serverinfo | |
| 5 | wp-pluginsused, wp-showhide, + freemyinternet floor fix | Cheapest; easy to finish in whatever budget is left. |

Largest-first is deliberate: a small plugin can be finished in a scrap of
leftover session, a large one cannot. Leaving the big ones till last is how they
never get done.

**At the start of every session,** run `python3 bin/verify.py --quiet` and
`git log --oneline -3` in each repo. Between them they tell you the true state
without trusting any of these notes.

---

## PICK UP HERE (2026-08-01)

Everything below is committed. All 19 plugin repos are pushed **except five**
held back pending an E2E verification run — see "Held pushes" at the end.

### The root folder is now a git repository

`github.com/lesterchan/wordpress-plugins`, private, branch **`main`** (not
`master` — the plugins use `master`, this one does not). It tracks the shared
tooling only: `_standards/`, `bin/`, `.wp-env.json`, `.gitignore`. The 19 plugin
directories are ignored **by name**, because a pattern would also swallow
`_standards/` and `bin/`.

The line in "Decisions already made" saying the root is left untracked is now
out of date. It is tracked; the plugins inside it are not.

### Playwright E2E — 6 of 19 done

Suites exist for **wp-postratings (52 tests), wp-pagenavi (13), wp-commentnavi
(13), wp-showhide (10), wp-relativedate (10), wp-serverinfo (10)**. All green
locally, and 5 of the 6 green on GitHub Actions first time (the sixth failed on
a test bug, since fixed — see below).

Scaffolding is in `_standards/templates/`: `playwright.config.js` (reads
`testsPort` from `.wp-env.json`, so the port lives in one place),
`bin/test-e2e.sh`, `tests/e2e/global-setup.js`, `tests/e2e/index.php`, the
`package.json` entries and the `ci.yml` `e2e:` job.

**Remaining 13:** freemyinternet, wp-ban, wp-dbmanager, wp-downloadmanager,
wp-draftsforfriends, wp-email, wp-pluginsused, wp-polls, wp-postviews, wp-print,
wp-stats, wp-sweep, wp-useronline.

### E2E lessons that will recur — read before writing the next suite

* **`bin/test-e2e.sh` is the only entry point.** wp-env installs a plugin into
  the tests environment but activates neither it nor any theme; PHPUnit needs
  neither, because its bootstrap loads the plugin itself and never renders a
  page. A browser gets no plugin, no menu, and a front page returning 200 with
  an empty body. The script fixes both on every run, which also makes it
  self-healing after `bin/test.sh` reinstalls that database underneath it.
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
* **The tests site uses plain permalinks**, so `/page/2/` is not a pagination
  URL — WordPress serves page one and the navigation truthfully says "Page 1 of
  3". Navigate by clicking.
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

### Demo site: `bin/seed-demo.sh`

Fills the root harness at **http://localhost:8888** (admin / password) with the
same fixtures the suites use. `bin/seed-demo.sh [posts] [comments]`, default
200/100. Re-runnable: it clears only what it made (marked with a `_demo_fixture`
meta key). Sets pretty permalinks and comment paging, activates all 19 plugins
and Twenty Twenty-One, and maps `_standards/demo/mu-plugins` as a theme shim so
WP-PageNavi and WP-CommentNavi render at all.

### wp-polls, brought in line with wp-postratings

* "Poll Logging Method" → **"Check For Repeat Votes"**, key `logging_method` →
  `check_method`. **Every vote is now logged whatever the check says**;
  `wp_polls_log_vote` turns it off. Stored numbers unchanged.
* "Expiry Time For Cookie And Log" → **"Remember A Voter For"**. Its old hint
  said "0 to disable", which was the opposite of the truth: zero makes the block
  *permanent*. Nothing is deleted either — it only sets how far back a check
  looks.
* **"Polls AJAX Style" removed.** Loading indicator always shows; the fade now
  reads `prefers-reduced-motion` — which must be read in the *script*, because
  the transition is inline and an inline style beats a media query.
* `setcookie()` guarded by `headers_sent()`, as wp-postratings'.
* **CSS fix:** `.wp-polls input { display: inline; border: 0 }` broke every theme
  that draws its own radio. With `appearance: none` an input is a non-replaced
  inline box, so width/height do not apply — Twenty Twenty-One's 25px circles
  rendered as 6px slivers. The reset is gone; the label half stays.

### The CI lesson worth not repeating

First CI run after the E2E suites landed: **8 of 19 red, and PHPCS plus all 114
PHPUnit jobs were green.** Every failure was one rule read two wrong ways.

"A plugin with no `js/` drops the eslint job" let **five repos ship e2e specs
that nothing had ever linted** (their `package.json` had no `lint:js`), and left
**three repos with no JavaScript at all** carrying a job that died at
`actions/setup-node` for want of a lock file. §8 now says "no `js/` **and** no
`tests/e2e/`", `verify.py` enforces it, and the workflow runs
`npm run test:js --if-present`.

### Held pushes — do this first

Five repos are committed but **not pushed**, pending a background agent
verifying their suites still pass after `eslint --fix` rewrote the specs:
**wp-commentnavi, wp-pagenavi, wp-relativedate, wp-serverinfo, wp-showhide**.
Confirm each is green, then `git push origin master` in each.

wp-relativedate carries the one real CI test bug, now fixed: its "yesterday"
fixture was `Date.now() - 26 hours`, which lands **two** calendar days back when
the suite runs between midnight and 02:00 — CI ran at 01:44 UTC and the plugin
correctly said "2 days ago". It now uses a `daysAgo()` helper pinned to midday.
**A time-relative fixture asserting a calendar concept is a bug waiting for the
clock.**

### Open, not started

* **The capability tests in both navigation suites assert nothing.** "A user
  without manage_options cannot reach the screen" **passes with the plugin
  deactivated**, because the page does not exist — it cannot tell "capability
  works" from "page missing". Add a companion assertion that an admin *can*
  reach the same screen.
* **`test-metadata.php` exists in four different implementations** across the
  collection (iterator-prune, strpos, scandir skip-list, hardcoded directory
  list). Excluding `artifacts/` therefore took four different edits, and the
  hardcoded-list variant silently passes for any directory nobody added to it.
  Pick the iterator form, put it in `_standards/templates`, use it everywhere.
* **Only wp-sweep has a CLAUDE.md.** The other 18 have none, so every
  architectural decision that file records is unwritten elsewhere.
* **wp-polls logs**: leave as a sub-view (per-poll, so the poll is the entry
  point). The one misplaced control is "Delete All Logs", which is cross-poll
  but sits inside a per-poll screen.


## Remaining work, in order

1. **Finish/verify the fan-out.** Any plugin whose agent did not commit.
2. **`python3 bin/verify.py`** until it reports zero. This catches the
   mechanical half; read the diffs for the rest (voice, comment density,
   whether the Settings API rewrite is real or cosmetic).
3. **`bash bin/test-all.sh`** and **`bash bin/test-all.sh --multisite`** against
   the shared environment. This is the first time PHPUnit runs at all, so
   expect fallout, especially around renamed options and hooks.
4. **Cross-plugin uniqueness.** With all 19 mounted together, confirm no two
   plugins claim the same option row, global function, class or hook. This is
   the only check the per-plugin runs cannot do.
5. **§13 reconciliation.** Seven plugins implement the WP-Stats
   `wp_stats_sections` contract independently. Confirm all seven agree on the
   filter signature wp-stats actually defines.
6. **Upgrade Notice audit (§14.1).** For each plugin, diff the released version
   on wordpress.org against the pending major and make sure every user-visible
   break is in `## Upgrade Notice`, written for a site owner.
7. **Screenshots.** Bring up the shared wp-env, give each plugin real content,
   capture screenshots to `~/svn/wordpress_plugins/<slug>/assets/screenshot-N.png`
   — **staged only, do not `svn commit`** — and write the numbered
   `## Screenshots` section in each README.
8. **Then, and only then, release.** Manually, via SVN. Nothing here pushes,
   tags or touches SVN.

## Traps

* **Nothing in this spec has ever been run under PHPUnit.** Not once, on any
  plugin. Step 3 is the first execution of the new `phpunit.xml.dist`, and the
  template turns on three strict flags the old configs did not have:
  `beStrictAboutTestsThatDoNotTestAnything`, `failOnWarning` and `failOnRisky`.
  Expect currently-green tests to fail on the strictness alone — any test
  without an assertion is now *risky*, and risky is now fatal. That is a
  feature, but budget for it, and do not mistake it for a rename gone wrong.
  If the noise is overwhelming, turn the three flags off in the template, get
  the suites green, then turn them back on one at a time.
* Test discovery changed to `<directory prefix="test-">`. A test file not named
  `test-*.php` is now **silently not run** rather than erroring. After the
  rename step, compare the test count against what the plugin reported before —
  a suite that suddenly got smaller is the symptom.

* The local `~/svn/wordpress_plugins` checkouts are **stale** (2022-era). Query
  `plugins.svn.wordpress.org` directly for the released baseline — §14 has the
  table.
* `plugin_deploy.sh` (in `outside this repository`) globs its
  exclusions, so `phpunit*.xml*` and `vitest.config.*` are already excluded. A
  stale comment in wp-ban's old ci.yml claimed otherwise.
* `wp-serverinfo` and `wp-sweep` have extra `claude.yml` /
  `claude-code-review.yml` workflows. Those are **not** part of this standard;
  leave them alone.
* Later phase, not started: WP-CLI, REST API and Gutenberg blocks across all
  plugins. `wp-sweep` already has `WP_Sweep_Command` and `WP_Sweep_API` and is
  the reference.

---

## PICK UP HERE (2026-08-01, second session)

### The state in one line

Twelve plugins gained Playwright suites on disk that **nobody has run to
green**. Treat every one as unverified until you have run it yourself.

### What is finished and safe

* **wp-polls** — 30 E2E tests green, 261 PHPUnit green single-site and
  multisite, PHPCS and eslint clean. Committed, not pushed. Lester ships this
  one manually; do not touch SVN or tags for it.
* **All 19 READMEs** — changelog pruned to the current major only (308 entries
  dropped), Upgrade Notice sections rewritten concise and technical
  (9,600 words to 5,900). Committed per plugin, not pushed.
* **STANDARDS.md** — three new sections committed: 7.5 (E2E), 7.6 (upgrade and
  migration tests), 7.2.4 (escaping regression tests are mandatory for every
  plugin that echoes a stored value). Plus the two metadata traps below.

### The twelve unverified suites

| Plugin | specs | tests |
|---|---|---|
| freemyinternet | 4 | 37 |
| wp-pluginsused | 4 | 26 |
| wp-print | 5 | 52 |
| wp-ban | 5 | 55 |
| wp-postviews | 7 | 84 |
| wp-useronline | 5 | 73 |
| wp-stats | 8 | 84 |
| wp-sweep | 5 | 66 |
| wp-downloadmanager | 4 | 73 |
| wp-draftsforfriends | 4 | 40 |
| wp-email | 4 | 41 |
| wp-dbmanager | 4 | 50 |

For each: `bash bin/test-e2e.sh` to green, `npm run lint:js` clean, and
`bash bin/test.sh --filter Metadata` still passing. Audit each against the
plugin's own `includes/` before believing it is comprehensive — a suite can be
green and still miss half the plugin. wp-postviews' 84 tests in particular were
never checked for near-duplicate padding.

**wp-print's metadata suite is failing right now**, and it is the scaffolding
rather than the plugin: `test_the_plugin_root_holds_no_loose_files` at
`tests/test-metadata.php:513` globs `*.js` in the plugin root and finds
`playwright.config.js`, which has to live there because Playwright resolves
paths relative to it. Fix by exempting `*.config.js` from that one assertion.
STANDARDS 7.2.1 records the rule and the class it belongs to.

### Four changes Lester asked for, specified but NOT started

Tasks #17-#20, each with the decisions already made. They deliberately wait
until the E2E suites are green, and they will **break some of those suites** —
that is the suites working, not wasted effort.

1. **#17 Settings naming.** `<Name> Settings` on all 14 settings screens. Ten
   already comply; wp-print, wp-dbmanager, wp-postviews and wp-useronline say
   "Options". wp-print also has a *section* named "Print Options", the same as
   its page — rename that too.
2. **#18 wp-print + wp-email link settings.** Drop the four-way style select and
   both `post_text`/`page_text` fields; keep only the custom HTML template. Add
   `%POST_TYPE%` resolving to the post type's singular label. Migration
   synthesises the template from the old style *and* text; collapse to
   `%POST_TYPE%` only when the two texts are the stock pair, otherwise keep
   post_text verbatim and say in the Upgrade Notice that the page wording is
   lost — one template cannot express two arbitrary strings.
3. **#19 wp-postviews Display Options.** Remove the six-context matrix, but keep
   `WP_PostViews_Display::should_be_displayed()` answering a
   `wp_postviews_should_display` filter. The 2.0.0 Upgrade Notice names that
   method as the documented replacement for the old global, so removing it
   outright would break a promise in the release about to ship.
4. **#20 Proxy header.** Five plugins have one. wp-polls and wp-postratings
   carry the canonical label "Header That Contains The IP:" and the three-part
   description (see `WP_Polls_Settings::describe_ip_header()`); bring wp-email,
   wp-ban and wp-useronline to it, substituting each plugin's own constant and
   filter. wp-ban also has a "behind a reverse proxy" checkbox nobody else has —
   decide whether the header field alone should carry the meaning.

### Open from before

* The capability tests in the wp-pagenavi and wp-commentnavi suites pass with
  the plugin deactivated. STANDARDS 7.5 now forbids the one-sided form; those
  two suites still need fixing.
* `test-metadata.php` exists in four implementations, and its `$skip` array in
  five variants. Task #14.

### Bugs the E2E suites found (tasks #21, #22)

**Two stored XSS**, both invisible to PHPUnit and both exactly what
STANDARDS 7.2.4 exists to catch:

* **wp-postviews `%POST_TITLE%`** — `WP_PostViews_Query::render_item()`
  (`includes/class-wp-postviews-query.php:89-104`) escapes the title only as a
  *side effect of truncation*: `snippet_text()` runs when `$chars > 0`, and the
  default is 0. So the default path has no escaping at all, and the raw title
  lands in the default template's `title="…"` attribute. Escape
  unconditionally; do not make truncation mandatory.
* **wp-useronline `[page_useronline]`** — the admin screen and the AJAX
  endpoint each wrap `users_online_page()` in `wp_kses_post()`; the shortcode
  registration (`includes/class-wp-useronline.php:86`) passes the function
  directly and gets it raw. Fix at the source: three call sites each deciding
  escaping separately is the defect, and a third wrapper would just be a fourth
  place to forget.

**Three more**: wp-postviews counts a preview when the AJAX counter is used
(`is_preview()` guards `process()` but not `enqueue()` — two places deciding one
fact again); wp-useronline's settings screen never calls `settings_errors()` so
it saves silently, the same bug E2E found in wp-postratings; and wp-sweep writes
`<p><ol>…</ol></p>`, which the parser splits, so only the no-JavaScript details
list is broken.

All five are left as **failing tests**, not weakened. Fix the code, not the test.

### E2E suite state after the third agent

wp-postviews 96/99 (3 failures are bugs 1 and 2 above), wp-useronline 68/75
(2 real bugs; 5 test-side fixes applied but **never re-run**), wp-stats reached
46/94 and wp-sweep 26/70 before the environment was torn down. Four agents
sharing one Docker daemon is too many — run these one at a time.

---

## PICK UP HERE (2026-08-01, third session)

### Release blocker, found by the metadata unification

**wp-polls deletes the shared `stats_display` row on uninstall.** `LEGACY_STATS_DISPLAY`
(`includes/class-wp-polls-options.php:73`) is on `legacy_extra_rows()`, which
`WP_Polls_Install::option_names()` merges and `uninstall_site()` deletes. So
removing WP-Polls takes the row from the other six WP-Stats plugins — the §13.2
hazard, in the release about to ship. The other five siblings keep the shared
rows off their uninstall lists deliberately; wp-postratings documents why at
`includes/class-wp-postratings-options.php:73-89`.

Fixing it is a **two-file change**: wp-polls' own
`tests/test-uninstall.php::test_every_row_the_plugin_owns_is_on_the_uninstall_list`
currently *requires* the row to be listed, so it must move too.

**wp-useronline has the same hazard one step earlier**: `delete_option( 'stats_display' )`
at `includes/class-wp-useronline-options.php:381` sits in `maybe_migrate()`, not
the uninstaller. Its uninstall list is clean, so no test catches it — the new
family test covers uninstall only.

### Other findings, none fixed

* **wp-polls and wp-stats do not carry** "Update all seven WP-Stats plugins
  together"; the other five do. Two family tests fail them. Left failing.
* **freemyinternet** ships no "or later" GPL block (`freemyinternet.php:22-24`)
  under a `License: GPLv2 or later` header, and its Upgrade Notice never names
  the removed global `freemyinternet()`. Its changelog also still says
  "Minimum WordPress 6.0 and PHP 7.4", contradicting its own BREAKING line.
* **wp-relativedate, wp-serverinfo and wp-showhide** Upgrade Notices claim "the
  plugin now stores one row"; §2.1 and the code say they store nothing.
* **wp-serverinfo's** Upgrade Notice says "up from WordPress 4.0 and PHP 7.2",
  which §14.1 calls out by name.

### #14 state

`_standards/templates/helper-metadata-testcase.php` is the shared base: 23
tests, `abstract class Plugin_Metadata_TestCase extends Plugin_TestCase`, wired
per plugin by two lines in `tests/bootstrap.php` (`class_alias` + require). 18 of
19 plugins carry a byte-identical copy; verify with `md5 -q` across all of them
before trusting any of it.

Three defects were found **in the template itself** after it shipped to the
copies, which is the argument for the md5 check being part of the workflow:
`test_the_plugin_root_holds_no_loose_files()` compared a hand-written list
against `glob()` output, so it asserted the slug sorts after `uninstall.php` —
true of every `wp-*` plugin and false of freemyinternet; and two phpcs errors
that fired in all 19 copies at once. All three are fixed and re-synced.

### Overnight-safe work

**#11 (the E2E sweep)** is the one to run unattended: ~808 tests, ~138 ever
verified, 19 plugins at 10-25 minutes each, and it MUST be one plugin at a time
— four concurrent Playwright runs tore each other down on a 7.6 GiB Docker.
**#13 (CLAUDE.md)** can run alongside it because it needs no containers.

Not overnight: **#8** and **#16** compete for the same Docker; **#5** is
judgement work; **#7** goes near SVN; **#10** touches upgrade paths on plugins
about to ship.

### #14 finished, and it found a THIRD shared-row violation

All 19 plugins now carry a byte-identical copy
(`md5 baa236eac7b3baba83e68eaa7bf2448e`) and extend the shared base.

**wp-downloadmanager deletes BOTH shared WP-Stats rows on uninstall.**
`stats_mostlimit` is in `legacy_map()` (`includes/class-wp-downloadmanager-options.php:74`)
and `stats_display` in `legacy_structured_rows()` (`:96`), and
`uninstall.php:32-40` drives uninstall from both lists. §13.2 says the
migration deletes the shared rows and uninstall leaves them alone; here one
list does both jobs.

So three of the seven WP-Stats plugins mishandle the shared rows: **wp-polls**
and **wp-downloadmanager** on uninstall, **wp-useronline** in its migration.
Each was invisible from inside its own plugin.

### Four checks that belong in the template but are not in it

Kept in individual plugins because nothing else covers them; lifting them in
would let six plugins drop their copies:
tags count, the Donations paragraph wording and position, the GPL "or later"
block in the plugin file (`bin/verify.py` checks only the header field), and
the `BREAKING: Requires WordPress 6.8 and PHP 8.2` changelog line.

### Two things the wiring exposed

`wp-sweep/tests/test-options.php:106` did a bare `require` of `uninstall.php`;
once the metadata test loaded it too the suite died on
`Cannot redeclare wp_sweep_delete_options()` — exactly the failure the
template's own docblock warns about. Route every such include through
`run_uninstall()`.

The brief I wrote said wp-sweep's uninstaller drops tables. It does not — it
deletes two option rows. Only wp-draftsforfriends and wp-downloadmanager have
schema-touching uninstallers.
