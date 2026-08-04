# Resume here

State of the consistency programme as of **2026-08-04**. Read this, then
`_standards/STANDARDS.md`, which is the contract everything else follows.

**In one line:** all nineteen plugins are green on CI, the pre-revamp tags are
cut and pushed, and **four items are open** — the rest of the §7.6.1 migration
test work, the spec-against-checks audit, the WP-CLI/REST/blocks phase, and a
screenshot recapture Lester asked for on 2026-08-04. Nothing is waiting on
Lester except the scope call in item 3.

**The release blocker is closed, and so is all of item 1 except (c).** Items
1(a), 1(b), 1(d), 1(e) and 1(f) all landed on 2026-08-04: wp-dbmanager's
migration is fixed with a `verify.py` rule behind it, eight plugins gained a
stock-defaults fixture, and the false `register_setting()` docblock turned out
to be in three plugins rather than one. **1(c) — eleven end-to-end migration
tests — is what remains**, and the notes below say what to write them against.

**§7.6.1 was overstated, and the correction matters before writing 1(c).**
Core's `update_option()` already falls back to `add_option()` when the
`default_option_*` filter is what answered `$old_value`, so the *write* half of
the shape is mostly core's problem and not ours. The *read* half is the real
defect and always was: a bare `get_option()` behind an `is_array()` guard skips
the fold-in while the legacy row is deleted regardless. Measured, not assumed —
see "Rules earned the hard way".

**Green tools were not enough, and that is the lesson of the day.** Nineteen
suites, `verify.py` at zero and CI green across the board, while a data-loss
migration sat one hook-ordering accident away from firing — because §7.6.1 was
a rule the spec stated and nothing checked. Item 2 counts how much else is in
that position: **16 of 48 sections**, now that §7.6.1 has a check of its own.

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
  32 of the 48 have something mechanical behind them; see item 2.
* `_standards/templates/` — the files each plugin copies verbatim, placeholders
  `{{SLUG}}` `{{NAME}}` `{{CLASS}}` `{{UNDER}}` `{{UPPER}}` `{{L10N}}`
  `{{DESCRIPTION}}`.
* `.wp-env.json` — all 19 plugins in one WordPress on 8888/8889.
* `bin/verify.py` — mechanical checker, **93 `check()` call sites**, not all of
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

## Current state — verified 2026-08-03

* **CI green on all 19**, checked run by run rather than assumed. This line is
  the one in this file most likely to be out of date by the time you read it —
  it is true only of the commits listed by `git log --oneline -1` in each repo
  on the date above. Re-check rather than trust it.
* `verify.py` 0 across all 19.
* PHPUnit green single site and multisite; Playwright green.
* **Every assertion in the collection carries a failure message** — 7,879 of
  7,879, up from 3,360 of 7,860 (42.7 %) when the work started. The total moves
  with every commit; the ratio is the claim, and
  `python3 bin/measure_assertions.py /path/to/plugins/*` re-derives both.
* The permalink audit of the E2E suites is complete — see below.
* **No known plugin bug is outstanding.** wp-dbmanager's was fixed on
  2026-08-04 (item 1a) and now has both a rule and a test behind it. The lesson
  stands even though the line has flipped: it was latent rather than firing,
  every suite was green, and nothing here caught it because `verify.py` had no
  rule for it and no test took the admin path.

## Remaining work, in order

**Four items are open: one (partly), two, three and eight.** Four is a human read
with nothing mechanical left in it; five, six and seven are done.

1. **Close the §7.6.1 migration gap.** Audited 2026-08-03 and every figure below
   re-checked by hand afterwards, because the audit came from an agent and this
   file has been wrong about counted things before. **(a), (b), (e) and (f) are
   done — 2026-08-04. (c) and (d) remain, and are the grind.**

   ~~**(a) wp-dbmanager reads the settings row bare.**~~ **Fixed 2026-08-04**,
   commit `472101e`. `includes/class-wp-dbmanager-options.php:211` was
   `get_option( self::OPTION )` with no second argument while
   `class-wp-dbmanager-settings.php:86` passes `'default' => …`, so the read
   answered with the defaults array, `is_array( $current )` was true, the
   fold-in was skipped and `dbmanager_options` was deleted anyway. Latent only
   because `maybe_upgrade()` ran on `plugins_loaded` and `register_setting()` on
   `admin_init`, one hook later.

   It now reads `get_option( self::OPTION, false )`, which is what the plugin's
   own `write()` already did. The count held up: **bare reads of the current
   settings row, whole collection, one — this one.** A regression test seeds the
   shipped defaults, registers the setting first so the filter is live, and
   asserts the raw row; **confirmed to fail with the fix reverted.** The
   pre-existing customised-fixture test passed throughout, which is item 1(d) in
   miniature.

   ~~**(b) Make it a `verify.py` rule.**~~ **Done 2026-08-04**, commit `a4b3b0c`.
   Fails any shipped file reading the plugin's own settings row through a
   one-argument `get_option()`. Proven both ways: planting a bare read in
   wp-print reports `includes/class-wp-print-options.php:109`, and all nineteen
   are green with it removed.

   Two scoping decisions worth keeping. **The legacy row is deliberately not
   covered** — `register_setting()` names the *current* row, so no
   `default_option` filter exists for the old one and a bare read of it is
   correct, which is what five plugins do. And it is **shipped code only, by
   allow list** (`includes/` plus the root entry points), because tests read the
   row bare on purpose to assert what is actually in the database — there are
   about sixty such reads across the suites, every one of them right.

   **(c) Eleven plugins have a migration and no end-to-end test of it.**
   Counted, not assumed: fifteen plugins migrate, and four have
   `tests/e2e/upgrade.spec.js` — freemyinternet, wp-ban, wp-pluginsused and
   wp-print. Missing: **wp-commentnavi, wp-dbmanager, wp-downloadmanager,
   wp-draftsforfriends, wp-email, wp-pagenavi, wp-polls, wp-postratings,
   wp-postviews, wp-stats, wp-useronline.**

   `wp-print/tests/e2e/upgrade.spec.js` is the reference and the shape is fixed:
   seed the legacy rows with `wpEval`, **assert the fixture really is
   pre-migration**, then `page.goto( '/wp-admin/index.php' )` — an ordinary
   admin request, *never* a reactivation, because reactivating is the WP-CLI
   path in disguise and takes the easy branch. Then assert the legacy rows are
   gone, the new row is present **read raw with the two-argument
   `get_option()`**, and the value shows up on the far end. Reading it back
   through the plugin's own getter proves nothing: the getter merges the
   defaults, so a write that never happened is indistinguishable from one that
   did. That is the trap wp-email, wp-postviews and wp-useronline are already in
   — each has a defaults-equal fixture but asserts through the merging getter.

   ~~**(d) Seed the shipped defaults, not just customised values.**~~ **Done
   2026-08-04, across eight plugins rather than the seven this said.** The seven
   named — wp-commentnavi, wp-dbmanager, wp-downloadmanager, wp-pagenavi,
   wp-polls, wp-postratings, wp-stats — each seeded a fixture where every field
   differs from the defaults, which cannot see the defect because the write
   lands precisely *because* the values differ. Each now has a stock fixture
   beside the customised one, not replacing it: the all-customised policy is
   right for "did the values carry across" and is stated deliberately at
   `wp-polls/tests/test-migration.php:14-18`.

   Every stock fixture is **built from the plugin's own `defaults()`** — through
   `legacy_map()` where one exists — rather than typed out, so a changed default
   cannot quietly turn it back into a second customised fixture.

   The eighth is the trap named in (c): wp-email, wp-postviews and wp-useronline
   asserted the migrated row with a **one-argument `get_option()`**. All three
   register a `default`, so once that filter is live an absent row reads back as
   the defaults array and `assertIsArray()` passes whether or not anything was
   written — wp-useronline's idempotency test compared two such reads, which
   agree with each other either way. **Demonstrated rather than argued:** with
   wp-postviews' write mutated to a no-op, the one-argument form passes and the
   two-argument form fails on the same broken migration. wp-postviews also
   gained the stock fixture; its `stage_legacy_install()` with no arguments was
   already exactly defaults-equal and nothing had ever used it for this.

   **What (d) actually established, and it refines §7.6.1 again.** Whether a
   plugin survives the write-side gap is decided by **whether its sanitiser
   returns the defaults unchanged** — `update_option()` sanitises before it
   compares, so a sanitiser that alters its input pushes execution past the
   early return and into core's `add_option()` fallback. Measured across the
   collection on 2026-08-04 by asking each plugin whether
   `sanitize_option( OPTION, defaults() )` comes back identical to `defaults()`:
   **three do — wp-dbmanager, wp-pluginsused, wp-stats — and all three already
   have a `write()` helper**, so nothing was live. The rest are held up by their
   sanitiser and nothing else.

   The sharpest illustration is wp-commentnavi and wp-pagenavi, which carry
   **byte-identical migrations**. Remove `write()`'s `add_option()` branch and
   wp-commentnavi goes red while wp-pagenavi stays green, purely because one
   sanitiser is idempotent on the defaults and the other is not. That is the
   argument for `write()` being explicit rather than inheriting whichever
   accident happens to hold — and it was found by running the mutation on both
   instead of assuming the second behaved like the first.

   ~~**(e) wp-polls decides its own correctness by two adjacent lines.**~~
   **Done 2026-08-04**, commit `6eaa803` — but the premise was wrong and the
   correction is the useful part. `WP_Polls_Options::save()` did go through a
   bare `update_option()`, and `WP_Polls_Install::init()` (wp-polls.php:71) and
   `WP_Polls_Settings::init()` (:77) do both hook `admin_init` at priority 10 —
   **but no data was ever at risk**, because core covers the write side. See the
   corrected §7.6.1 note under "Rules earned the hard way".

   `save()` adds the row itself now, so neither the hook order nor the
   sanitiser's behaviour has to hold. It is hardening and is committed as
   hardening. **Two tests came with it** and are the item 1(d) fixture for this
   plugin — a stock-defaults install built from `legacy_map()` rather than typed
   out. Both were confirmed to fail against a `save()` mutated to write nothing;
   **neither fails against the bare `update_option()`, because there is nothing
   there to catch**, and a test that was left in claiming otherwise would have
   been the collection's fourth "test that cannot fail". One such test was
   written and deleted rather than committed.

   ~~**(f) Two comments that will mislead the next reader.**~~ **Done
   2026-08-04**, commits `38c7b39` (wp-pluginsused) and `e19f8ba`
   (freemyinternet). The first said "This assertion currently fails, and it is
   right to" about an assertion that passes — **verified by running the suite,
   6/6 green**, not by reading the code — so it was telling somebody to wave
   through a real regression. It now says what the assertion pins, keeps the
   original defect in the past tense because the shape is worth recognising, and
   ends by forbidding the weakening to the reactivation path.

   The second claimed `register_setting()` is passed a `default` when
   `class-freemyinternet-settings.php` passes only `type` and
   `sanitize_callback`. The code was right either way; the comment is what gets
   copied into the next plugin, and it was describing a trap as though it were
   armed.

   **That second one was three plugins, not one**, found while doing (d):
   wp-commentnavi and wp-pagenavi carry the identical false claim and were fixed
   the same day (`72ee34b`, `83ed675`). Exactly three plugins pass no `default`
   — freemyinternet, wp-commentnavi, wp-pagenavi — and all three had a docblock
   saying they did. One wrong sentence, copied to precisely the set of plugins
   it was wrong about. Their tests now register the setting **with** a default,
   which is the change a future release makes without thinking about
   migrations, and require the fold-in to land anyway.

   **Docker, wp-env and Playwright all run on Lester's machine** — the
   egress block that made these CI-only was the cloud sandbox, not here. So (c)
   and (d) can be written *and run* locally. Check
   `wp option get permalink_structure` in the tests container first; see the
   permalink section below.

2. **Audit the spec against the checks — 17 of 48 sections have nothing behind
   them.** This is the audit that keeps finding real defects, and the one item 1
   is a product of. Re-reading nineteen plugins against the spec buys nothing:
   the mechanical half is checked on every push and is green. Reading the *spec*
   and asking "what enforces this?" has found every defect of the last week —
   `@package` split along file age, §11's raster ban satisfied by all nineteen
   and enforced by nothing, §12's script list stale in all nineteen identically,
   and §7.6.1, which is item 1.

   Measured 2026-08-03 by cross-referencing the `§` citations in `bin/verify.py`
   and `templates/helper-metadata-testcase.php` against the section headings in
   STANDARDS. It was 31 with a check and 17 without; §7.6.1 gained one on
   2026-08-04, so it is now **32 with a check and these 16 without:**

   | Section | Mechanisable? |
   |---|---|
   | §2.2 Class constants — one spelling each | **yes** — compare the constant names across the nineteen |
   | §2.5 Functions | **yes** — same shape as §2.4, which is already checked |
   | §2.7 Capabilities | **yes** — the custom-capability list is fixed and named in the section |
   | §4.2.1 / §4.2.2 Tabs, and their names | **yes** — the tab labels are a closed set |
   | §4.3 List tables | partly — "uses `WP_List_Table`" is checkable, "well" is not |
   | §4.4 Markup | no — judgement |
   | §7.1 Structure | **yes** — file naming and the `test-`/`helper-` split |
   | §7.2.1 Process-wide state | no — needs the suite running |
   | §7.2.3 A suite that dies is not one that passed | already enforced, but by `bin/test-all.sh` rather than a rule; **say so in the section** |
   | §7.2.4 Escaping a stored value | partly |
   | §7.3 Coverage | no — a number, and gaming it is worse than missing it |
   | §13.1 The exact shape | **yes** — the fixture pins §13.2 already |
   | §13.3 WP-CLI and REST naming | not yet — nothing to check until item 3 ships |
   | §15 Order of work | no — process, not state |

   Roughly nine are worth a rule. Do them one at a time and **prove each both
   ways**: plant the violation, watch it fail, remove it, watch it pass. That is
   what caught the §4.2 drift in two plugins and the §11 gap.

   **The generalisation, already in §7.2.2 and now earned twice:** a rule the
   spec implies and nothing enforces is a rule nineteen copies will drift from,
   and the drift is invisible precisely because every tool is green.

3. **WP-CLI, REST API and Gutenberg blocks across the collection.** The only
   substantial item, and a phase of its own rather than a cleanup. `wp-sweep`
   already has `WP_Sweep_Command` and `WP_Sweep_API` and is the reference.

   **§13.3's naming was reversed on 2026-08-04, by Lester.** It is now the slug
   **without** the `wp-` prefix — `wp sweep`, `sweep/v1` — not `wp wp-sweep`.
   The `wp-` prefix is a wordpress.org directory convention rather than a
   command-naming one, the ecosystem norm is the brand (`wp wc`, `wp yoast`),
   and these are the names the released 1.2.0 already shipped. So the change
   **deletes a breaking change** this campaign had invented and documented:
   wp-sweep's README carried a FAQ entry, two `BREAKING:` changelog lines and an
   Upgrade Notice paragraph telling scripted callers to edit, all of which
   became false. §13.3 has the full reasoning.

   **Three names are deliberately left open**: `email`, `print` and `stats` are
   bare nouns a dozen plugins might want, and §13.3 says explicitly that it does
   not settle them. Decide each if and when it earns a command — a qualified
   name, or a shared `wp lc <plugin>` parent.

   **§13.3 pins only the naming, not who gets what** — the scope call (which
   plugins earn a command, a namespace or a block, and whether a block wraps the
   existing shortcode or replaces it) is still open and is Lester's.

4. **Read the diffs for voice.** The mechanical half is done and closed. What
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

   The mechanical half, all clean: **every function in shipped code has a
   docblock** — about 1,890 of them across the nineteen, a figure that moves
   with every commit and is checked rather than tracked — every file has a
   file-level docblock, and `@package` is the display name everywhere. That last
   one was a real find — four plugins
   (wp-useronline, wp-postratings, wp-draftsforfriends, wp-sweep) carried the
   lowercase slug in their older files and the display name in their newer ones,
   splitting each plugin along age rather than meaning, and canonicalisation
   walked past it because nothing compared the halves. `verify.py` checks it now.

5. ~~**The wp-draftsforfriends API question.**~~ **Decided and shipped
   2026-08-03.** Lester's call: ship the three actions, and do the URL filter
   properly rather than cheaply.

   `wp_draftsforfriends_share_created`, `_extended` and `_revoked` each fire
   after the write has succeeded, so a listener sees the stored row rather than
   what the caller asked for. `extend()` passes the previous expiry alongside
   the new one, because it cannot be recovered afterwards.

   **The URL filter needed a refactor first, and this is the part worth
   remembering.** `Shares::url()` wrote `?p=<id>&draftsforfriends=<hash>` and
   `Preview::requested_hash()` read the query argument back — each holding the
   string separately, so the link a friend was given and the check that lets
   them read it agreed only by coincidence. Filtering the URL alone would have
   let a site rewrite the link into a shape the plugin could not recognise, and
   every share would have 404'd with nothing on the admin screens looking
   wrong — which is the field bug fixed on 2026-08-02, reintroduced through an
   extension point.

   So the query argument is one constant both halves use, and the pair is
   filterable together: `wp_draftsforfriends_share_url` writes the link,
   `wp_draftsforfriends_requested_hash` reads it back. **They are one contract**,
   documented as such, and pinned by a test that rewrites the URL into a path
   segment, reads it back and still gets the draft — plus its mirror, which
   honours only half and correctly gets nothing. The filtered hash is sanitised
   on the way out, since it is the credential the preview is gated on.

   The general rule: **before exposing a value through a filter, find out who
   else depends on its shape.** A producer and a parser that never share a code
   path are a bug the moment either becomes public.

6. ~~**Sweep for assertions whose two operands are both literals.**~~ **Done
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

7. ~~**Route administrator creation through a helper (§7.2.2).**~~ **Done
   2026-08-03.** Eleven plugins got a `create_admin()` on their shared test case
   and **52 call sites now go through it**. None of the eleven takes a grant:
   every one gates on `manage_options` or on a custom capability of its own, and
   core's `map_meta_cap()` remaps neither. Only wp-sweep, wp-dbmanager and
   wp-print grant super admin, which is what §7.2.2 always said.

   Two things fell out of doing it. wp-ban's metadata fixture was granting super
   admin to register a `manage_options` page — a fourth grant the section could
   not account for, and now gone. And `verify.py` fails any plugin that reaches
   the user factory for an administrator outside `helper-*.php`.

   **The check is the point, not the refactor.** This paragraph's own numbers
   were wrong twice: first "the helper is on every plugin" when it was on five,
   then "twelve plugins, 55 sites" — that count included
   `get_role( 'administrator' )`, which asserts a capability rather than creating
   a user, and called wp-downloadmanager non-compliant one sentence after
   describing its idiom as compliant. Both were prose about a number nothing
   measured. The generalisation is in STANDARDS §7.2.2 and worth repeating here:
   **audit the spec against the checks, not the plugins against the spec.**

8. **Recapture every plugin's wordpress.org screenshots.** Asked for by Lester
   on 2026-08-04, which is what puts it on this list at all — see the note below
   about SVN. **Deferred deliberately, not forgotten:** it wants Playwright and
   a seeded WordPress, item 1(c) wants Playwright and eleven fresh E2E suites,
   and this file's own E2E lesson is that four concurrent Playwright runs tore
   each other down on a 7.6 GiB Docker. Lester's call was to record it and run
   it after the E2E work lands. Do not start it alongside item 1(c).

   **Every screenshot in the collection is pre-revamp.** The admin UI was rebuilt
   wholesale — Settings API everywhere, `WP_List_Table` on every tabular screen,
   one menu rule, renamed settings headings (§17's `<Name> Settings`) — so the
   images no longer show the software. That is the reason to redo all nineteen
   rather than only the five that fail the count check below.

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

   The rule wordpress.org actually applies is positional: `screenshot-N.png` is
   captioned by the Nth line of the `== Screenshots ==` list, so a missing file
   silently shifts every caption after it onto the wrong image. **The count
   matching is necessary and not sufficient** — the fourteen that agree have
   never been checked for whether each line still *describes* its image, and
   after a UI rebuild the safe assumption is that none of them do.

   How many to take is a judgement per plugin, not a number to preserve: the old
   counts were set against the old screens. Lester's brief was explicit that the
   current count is stale and the new one is ours to choose.

   Notes for whoever runs it. `bin/seed-demo.sh` fills the root harness at
   http://localhost:8888 (admin / password) with the fixtures the suites use,
   which is the site to photograph — it is a separate wp-env from any plugin's
   tests environment. Read
   https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/ for the
   naming and size rules before capturing. **Write only into
   `~/svn/wordpress_plugins/<slug>/assets/`**, touch nothing else in those
   checkouts, and do not `svn add`, commit or push — the checkouts are otherwise
   stale 2022-era trees (see Traps) and everything except the assets directory
   should be left exactly as found.

**Off this list on purpose:** the SVN release itself. Lester does it by hand.
Nothing here pushes, tags or touches SVN — **except item 8**, which Lester
explicitly asked for on 2026-08-04 and which writes screenshots into
`assets/` and nothing else.

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

Asked on 2026-08-03, and worth keeping because the answer is not "run
`verify.py` again".

**The mechanical half is continuously checked and green**, so re-auditing
nineteen plugins against fifteen sections by hand buys nothing. `bin/verify.py`
is 93 checks covering §1, §1.1, §2, §3, §4, §5, §6, §7, §7.6.1, §8, §9, §10 and §14;
the shared metadata fixture covers §13, including the shared-row contract that
two plugins violated. Both run on every push.

**The audit worth doing is the spec against the checks, not the plugins against
the spec.** Every defect found today — `@package` split along file age, the
metadata fixture free to drift, the hook copied twenty times with nothing
comparing it — was a rule the spec implied and nothing enforced. That audit
found two more:

* **§11, ship no raster image.** Satisfied by all nineteen and enforced by
  nothing: the GIFs and PNGs were replaced with inline SVG during the fan-out
  and never compared since, so the next one added would have shipped. Now a
  `verify.py` check, proven by planting a GIF in wp-ban.
* ~~**§12's `package.json` script list is stale.**~~ **Rewritten and checked
  2026-08-03.** The spec named five scripts *exactly*; every plugin also carried
  `test:e2e` and `test:e2e:headed`, added when Playwright landed and never
  written back, and seven had no `test:js`/`test:js:watch` at all. So all
  nineteen diverged from the spec, identically, and nothing noticed — there was
  no check.

  §12 now derives the set from what the plugin has rather than listing it: five
  unconditional, plus the vitest pair **only** where `tests/js/` exists, which
  is twelve of nineteen. The correlation was verified exact before the rule was
  written — `test:js` present if and only if `tests/js/` present, no exceptions.
  A `test:js` with no suite behind it is a green result that means nothing,
  which is why the rule forbids rather than merely permits it.

  `verify.py` derives the same set and compares, proven both ways: removing
  `test:e2e` reports it missing, adding `test:js` to a plugin without a suite
  reports it unexpected. §12's other claim — identical devDependency versions —
  was checked at the same time and is true: seven packages, one version each
  across all nineteen.

§15 is the order of work per plugin — process rather than state, and not
checkable.

## Rules earned the hard way

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

  The practical consequence for item 1(c): **assert the raw row, but do not
  expect the bare `update_option()` to be what fails.** A migration test that
  goes red only when the read is bare is testing the thing that actually breaks.

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

The programme found roughly **twenty-five spec bugs and eleven `verify.py`
bugs**, every one because an agent pushed back rather than complied. The pattern
that made it work: one plugin finds it, fix it centrally, the other eighteen
never see it.
