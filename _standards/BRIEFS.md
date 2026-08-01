# Per-plugin agent briefs

Launch an agent with **the preamble below, with placeholders filled in, plus
that plugin's section**. The preamble carries the rules; the section carries
what the survey found in that specific plugin, which is knowledge that exists
nowhere else and is expensive to re-derive.

Everything here was verified against the repos on 2026-07-28. Treat it as a
starting point, not gospel — tell the agent to check each claim.

---

## Preamble (use verbatim, substituting the table values)

> Bring ONE plugin into line with a written standard shared by all 19 plugins in
> /Users/lesterchan/git/wordpress_plugins. End goal: all 19 must read as though
> one person wrote them on the same afternoon. The ONLY permitted differences
> between two plugins are name, features and capability.
>
> STEP 1 — read IN FULL before touching anything:
>   /Users/lesterchan/git/wordpress_plugins/_standards/STANDARDS.md
> Templates to copy verbatim (substituting `{{...}}` placeholders):
>   /Users/lesterchan/git/wordpress_plugins/_standards/templates/
>
> YOUR PLUGIN: `<SLUG>` at /Users/lesterchan/git/wordpress_plugins/`<SLUG>`
>   `{{NAME}}`=… `{{CLASS}}`=… `{{UNDER}}`=… `{{UPPER}}`=…
>   wp-env port=… testsPort=…   Has JS: yes/no
>
> HARD CONSTRAINTS
> - Work ONLY inside your own plugin directory. Never modify a sibling plugin,
>   the repo root, or `_standards/`.
> - DO NOT start Docker. No `wp-env`, no `npx @wordpress/env`, no `bin/test.sh`,
>   no `bin/test-multisite.sh`. Sibling agents run concurrently and the machine
>   cannot host multiple wp-env stacks. The PHPUnit sweep runs centrally after.
> - DO run and DO make pass: `$(composer global config bin-dir --absolute)/phpcs
>   -q .`, `php -l` on every changed file, and for a JS plugin `npm run lint:js`
>   and `npm run test:js` (vitest needs no Docker).
> - You cannot run PHPUnit, so be rigorous by inspection: after every rename,
>   grep the WHOLE plugin including `tests/` for the old identifier and confirm
>   zero hits. Re-read and update every test that exercises code you changed.
> - **Commit after every numbered step of §15**, message prefixed `Step N: …`,
>   with `--no-gpg-sign`. Leave the tree clean and the plugin loadable at every
>   commit. Do NOT push, tag, or touch SVN.
> - Do NOT change the version number; §14 fixes what each plugin ships as.
> - Floors are WordPress 6.8 / PHP 8.2 (§1.1) — six places per plugin, and
>   delete any now-dead back-compat shim rather than leaving it unreachable.
>
> **Learned from the pilot (wp-relativedate) — these will hit you too:**
> - `phpcs.xml` no longer excludes `Generic.Commenting.DocComment.ShortNotCapital`
>   from `tests/`, and it fires on any test docblock opening with a lowercase
>   function name — `the_date() builds…`, `ago_only="false" is…`. The pilot had
>   14. **Reword them.** Do NOT re-add the exclusion; §9 forbids it.
> - `bin/test.sh` and `bin/test-multisite.sh` are 0755 in the template. `cp`
>   preserves that but `sed >` does not, and test.sh needs `{{SLUG}}`
>   substituted. `chmod +x` both afterwards.
> - §7.2's method names are authoritative. `wp-showhide/tests/test-metadata.php`
>   is the ancestor of those tests but predates §7.1 and does not match — do not
>   copy it as-is.
> - A step that is genuinely N/A for your plugin produces **no commit**. Do not
>   create an empty one; explain the gap in the final commit message.
> - Test discovery is now by the `test-` filename prefix, so a misnamed test file
>   is **silently not run**. Count the tests before and after your rename step
>   and confirm the number did not drop.
>
> REPORT BACK: what changed, what you could not complete and why, and any place
> the standard was ambiguous or wrong for this plugin.

---

## Identity table

| Slug | `{{NAME}}` | `{{CLASS}}` | port | JS | ships as |
|---|---|---|---|---|---|
| freemyinternet | FreeMyInternet | FreeMyInternet | 8890 | no | 1.0.0 |
| wp-ban | WP-Ban | WP_Ban | 8892 | yes | 2.0.0 |
| wp-commentnavi | WP-CommentNavi | WP_CommentNavi | 8894 | no | 2.0.0 |
| wp-dbmanager | WP-DBManager | WP_DBManager | 8896 | yes | 4.0.0 |
| wp-downloadmanager | WP-DownloadManager | WP_DownloadManager | 8898 | yes | 2.0.0 |
| wp-draftsforfriends | WP-DraftsForFriends | WP_DraftsForFriends | 8900 | yes | 2.0.0 |
| wp-email | WP-EMail | WP_Email | 8902 | yes | 3.0.0 |
| wp-pagenavi | WP-PageNavi | WP_PageNavi | 8904 | no | 3.0.0 |
| wp-pluginsused | WP-PluginsUsed | WP_PluginsUsed | 8906 | no | 2.0.0 |
| wp-polls | WP-Polls | WP_Polls | 8908 | yes | 3.0.0 |
| wp-postratings | WP-PostRatings | WP_PostRatings | 8910 | yes | 2.0.0 |
| wp-postviews | WP-PostViews | WP_PostViews | 8912 | yes | 2.0.0 |
| wp-print | WP-Print | WP_Print | 8914 | yes | 3.0.0 |
| wp-relativedate | WP-RelativeDate | WP_RelativeDate | 8916 | no | 2.0.0 |
| wp-serverinfo | WP-ServerInfo | WP_ServerInfo | 8918 | no | 3.0.0 |
| wp-showhide | WP-ShowHide | WP_ShowHide | 8920 | yes | 3.0.0 |
| wp-stats | WP-Stats | WP_Stats | 8922 | no | 3.0.0 |
| wp-sweep | WP-Sweep | WP_Sweep | 8924 | yes | 2.0.0 |
| wp-useronline | WP-UserOnline | WP_UserOnline | 8926 | yes | 4.0.0 |

Plugins with no `js/` omit the eslint job from `ci.yml` and create no
`package.json` / `eslint.config.mjs` / `vitest.config.mjs`.

---

## freemyinternet

* Only plugin without a `wp-` slug. Classes stay `FreeMyInternet_*`, constants
  `FREEMYINTERNET_*`. Do **not** add a `WP_` prefix.
* **Already done and committed at `2a2eaf7`.** Needs only the §1.1 floor fix in
  six places. Read its diff in the verification pass, don't re-run an agent.
* Old ci.yml was the pre-`permissions`/`concurrency` generation that wrote
  `.wp-env.override.json` from the matrix — already replaced.

## wp-ban

* Classes `Ban*` → `WP_Ban*`. Option `banned_options` → `wp_ban_options`,
  `banned_stats` → `wp_ban_stats` (**not** autoloaded). `ban_db_version` row →
  `wp_ban_version`.
* `ban.js` at the root, jQuery → `js/wp-ban-admin.js`, vanilla, `wpBanL10n`.
* Hooks already `wp_ban_*`; no renames.
* Changelog uses `IMPORTANT:` → rename to `BREAKING:`; each also under
  `## Upgrade Notice`. README `License:` line missing its two trailing spaces.
* Constants: add `WP_BAN_SLUG`, `WP_BAN_DB_VERSION`. No `.editorconfig`.
* Its old ci.yml comment claiming `plugin_deploy.sh` lacks a `vitest.config.*`
  exclusion is **stale** — the script globs it.

## wp-commentnavi

* Old-generation ci.yml. Committed `.wp-env.override.json` (8896/8897) → delete.
* `commentnavi-css.css` at root → `css/wp-commentnavi.css`.
* Classes `CommentNavi_*` → `WP_CommentNavi_*`. Option → `wp_commentnavi_options`.
* tests: `class-commentnavi-testcase.php` → `helper-testcase.php`;
  `fixture-comments-template.php` → `helper-comments-template.php`.
* Sibling-by-design with wp-pagenavi; keep the `*_class_*` filter family
  consistent but do not edit wp-pagenavi.

## wp-dbmanager

* **Ships as 4.0.0** — 3.0.0 is already live on wordpress.org (§14).
* **Reference implementation for §4.3 `WP_List_Table`.** Preserve its quality;
  flag genuine conflicts rather than degrading it.
* Classes `DBManager*` → `WP_DBManager_*`. Option → `wp_dbmanager_options`.
* `CAPABILITY = 'install_plugins'` is deliberate (it can drop your database) —
  keep, route through `wp_dbmanager_capability`.
* `TRANSIENT = 'dbmanager_backup_folder_public'` → prefix it.
* `htaccess.txt` and `Web.config.txt` are shipped files protecting the backup
  folder — they stay at the root. `.idea/` committed → delete.
* tests: `testcase.php` → `helper-testcase.php`. ci.yml lints JS but never
  tests it.

## wp-downloadmanager

* **The largest job.** Loose root files: `download-add.php`, `download-rss.php`,
  `download-manager.php` → `includes/`; `download-css.css` → `css/`;
  `download-admin.js`, `download-forms.js`, `download-quicktag.js` → `js/`.
* **36 images.** `images/ext/*.gif` is 34 extension icons → ONE inline SVG
  sprite (`<symbol>` per family, `<use>`, generic fallback). `drive.png`,
  `drive_go.gif` → inline SVG. Delete `images/`.
* `tinymce/plugins/downloadmanager/plugin.js` uses jQuery — button STAYS,
  rewrite vanilla. `download-quicktag.js`, `download-forms.js` too.
* Settings scattered across menu entries → ONE top-level menu, settings groups
  as TABS (§4.1).
* Option `download_options` → `wp_downloadmanager_options`; bare
  `download_nice_permalink` row folds in; `download_db_version` →
  `wp_downloadmanager_version`.
* Hooks: `download_embedded` → `wp_downloadmanager_embedded`, `downloads_page`
  → `wp_downloadmanager_page`. Dropped outright, documented.
* §13 WP-Stats consumer. `.idea/` committed → delete.

## wp-draftsforfriends

* Classes → `WP_DraftsForFriends_*`; `DraftsForFriends_Table` →
  `WP_DraftsForFriends_List_Table`.
* No consolidated option row today — create `wp_draftsforfriends_options` and
  `wp_draftsforfriends_version`, migrate whatever exists, cover with a test.
* `CAPABILITY = 'publish_posts'` deliberate — keep.
* `SECTION` → `SECTION_SHARE`; `SLUG` → `PAGE`.
* `js/draftsforfriends-admin.js` jQuery → vanilla, `wpDraftsForFriendsL10n`.
* Fires no hooks of its own today.

## wp-email

* Loose root: `email-css.css`, `email-css-rtl.css` → `css/`; `email.js`,
  `email-admin.js` → `js/`.
* **`email-css-rtl.css` must go** (§5.1) — one of only two RTL sheets.
* Images: `email.gif`, `email_famfamfam.png` → inline SVG envelope;
  `loading.gif` → the same CSS spinner as wp-polls.
* Classes `Email*` → `WP_Email_*`; `Email_WpStats` → `WP_Email_WPStats`.
* Option `email_options` → `wp_email_options`; bare `email_fields` and
  `email_template_*` rows fold in; `email_db_version` → `wp_email_version`.
* `CAPABILITY = 'manage_email'` deliberate — keep. `EMAIL_SHOW_REMARKS` →
  `WP_EMAIL_SHOW_REMARKS`. Add `WP_EMAIL_DIR/URL/SLUG`.
* §13 WP-Stats consumer. README `License:` missing trailing spaces.

## wp-pagenavi

* Old-generation ci.yml; no port/`$schema`/`config` in `.wp-env.json`.
* `pagenavi-css.css` → `css/wp-pagenavi.css`, convert to logical properties.
* Classes `PageNavi_*` → `WP_PageNavi_*`. Option → `wp_pagenavi_options`.
* **`Contributors: GamerZ, scribu` → `GamerZ`** — the only plugin with a second
  name. This removes the sole record of that authorship and §3.3 also deletes
  `### Credits`; consider a line in `## Description`.
* Twelve `wp_pagenavi_class_*` filters keep their names.

## wp-pluginsused

* **Three unprefixed public hooks**, dropped outright, each documented:
  `pluginsused_hidden_plugins`, `pluginsused_plugins_used`,
  `pluginsused_show_version` → `wp_pluginsused_*`.
* Classes → `WP_PluginsUsed_*`. Option → `wp_pluginsused_options`.
* `GROUP = 'pluginsused_options_group'` → `wp_pluginsused_options`.
* Reads core's `active_plugins` — leave that alone.
* `includes/deprecated.php` exists; renamed hooks get no shims, but genuinely
  deprecated *functions* may stay.

## wp-polls

* Loose root: `polls-add.php`, `polls-logs.php`, `polls-manager.php`,
  `polls-options.php`, `polls-templates.php` → `includes/`; two CSS and two JS
  files → `css/` and `js/`.
* `images/loading.gif` → CSS-only spinner, `prefers-reduced-motion` aware.
  Same spinner as wp-email.
* `tinymce/plugins/*/plugin.js` jQuery — button STAYS, rewrite vanilla.
* Classes `Polls_*` → `WP_Polls_*`. Option `poll_options` → `wp_polls_options`;
  **both** `poll_db_version` and `poll_version` collapse into `wp_polls_version`.
* Already uses Settings API + `WP_List_Table` — **verify against §4, don't
  rewrite**.
* ~32 `wp_polls_*` hooks are the documented public API — do NOT rename.
* §13: has no WPStats class; create `WP_Polls_WPStats`.
* Largest test suite of the nineteen. Changelog already very long — extend it.

## wp-postratings

* **Worst casing offender**: `Postratings*` → `WP_PostRatings_*` (capital R).
  Grep case-sensitively afterwards.
* **Two version rows collapse**: `postratings_db_version` AND
  `postratings_options_version` → one `wp_postratings_version`.
* **Two settings groups** `GROUP_SETTINGS` / `GROUP_TEMPLATES` → TABS on one
  page (§4.1). This is the case that rule exists for.
* `CAPABILITY = 'manage_ratings'` deliberate — keep. `RATINGS_IMG_EXT` →
  `WP_POSTRATINGS_IMG_EXT`.
* Hook `rate_post` → `wp_postratings_rate_post`, dropped outright.
* **Delete `tests/phpunit-multisite.xml`** (stray); replace
  `bin/test-multisite.sh` with the template. `class-wp-postratings-testcase.php`
  → `helper-testcase.php`. `vitest.config.js` → `.mjs`.
* `includes/class-postratings.php` uses jQuery. §13 WP-Stats consumer.

## wp-postviews

* Loose root: `postviews-admin.js`, `postviews-cache.js` → `js/`.
* Classes `PostViews_*` → `WP_PostViews_*`. Option `views_options` →
  `wp_postviews_options` (renamed to the slug, not the old `views` noun);
  `views_version` → `wp_postviews_version`.
* Constants: `GROUP`, `SECTION_DISPLAY`, `SECTION_GENERAL` all re-prefixed.
* Hooks dropped outright: `postviews_should_count` →
  `wp_postviews_should_count`; **`the_views` → `wp_postviews_the_views`** —
  very generic, likely in people's themes, so the Upgrade Notice matters.
* `postviews-admin.js` jQuery. `.wp-env.json` sets `WP_CACHE: true` in tests —
  keep only if a test depends on it. §13 WP-Stats consumer.

## wp-print

* Loose root: `print-comments.php`, `print-posts.php` → `includes/`; two CSS →
  `css/`; `print.js`, `print-admin.js` → `js/`.
* **`print-css-rtl.css` must go** (§5.1) — the other of the two RTL sheets.
* Images `print.gif`, `printer_famfamfam.gif` → one inline SVG printer glyph
  inheriting `currentColor`.
* Classes `Print_*` → `WP_Print_*` — `Print_*` is a dangerously common
  unprefixed global.
* **Option name conflict**: `OPTION_NAME = 'print_options'` but the code also
  references a literal `'wp_print_options'`. Reconcile to `wp_print_options`.
* `QUERY_VAR = 'print'` is a public query var from the last SVN release — keep
  the value, do not prefix.
* Committed `.wp-env.override.json` (8898/8899) → delete.
* jQuery in `class-print-admin.php` and `print-admin.js`.

## wp-relativedate

* **Suggested pilot** — smallest plugin, validates the spec end-to-end cheaply.
* **No `uninstall.php` and no options at all** (wp-showhide is the other).
  Create `uninstall.php`, `wp_relativedate_options`, `wp_relativedate_version`.
  If there are genuinely no settings the options row may be empty — say so,
  because this is consistency for its own sake and may deserve an exemption.
* Classes → `WP_RelativeDate_*`. No admin screen at all — do **not** invent a
  settings page to satisfy §4. No CSS, no JS — do not add either.
* Template tags and shortcodes are the public API; names unchanged.

## wp-serverinfo

* Classes → `WP_ServerInfo_*`, keeping `MySQL` / `PHP` acronym casing.
* No option row today — create both. `SERVERINFO_WIDGET_ID` →
  `WP_SERVERINFO_WIDGET_ID` (grep tests too).
* §7.3: `phpinfo()` and the Redis/Memcached probes are the legitimate case for
  `@codeCoverageIgnore` with a reason. Push real coverage on `_Format`,
  `_Cache`, `_PHP`.
* Informational screen, not settings — `add_management_page()` or
  `add_options_page()`, no top-level menu.
* **Has extra `claude.yml` / `claude-code-review.yml` — leave them alone**,
  replace only `ci.yml`.

## wp-showhide

* **Owns the canonical `tests/test-metadata.php`** — the shared tests in §7.2
  derive from it. Make it the most complete version; the others copy it.
* **Its plugin-header GPL block is the wording §3.1 tells everyone to adopt** —
  do not change it.
* **No `uninstall.php`, no options** — same situation as wp-relativedate.
* Classes → `WP_ShowHide*`. Committed `.wp-env.override.json` (8912/8913).
* **Delete `bin/lint-js.mjs`** — bespoke linter no other plugin has;
  `npm run lint:js` → `eslint .` is the standard.
* `package.json` and `node_modules` exist but no root `.js` — find where the
  script lives, land it at `js/wp-showhide.js`.
* `[showhide]` shortcode is the public API. No admin screen.

## wp-stats

* **Owns the §13 contract.** Defines `wp_stats_sections`; six siblings consume
  it. Must never read a sibling's option row, and no `class_exists` probing.
* Classes `Stats*` → `WP_Stats_*` — bare `Stats` is exactly the unprefixed
  global the standard exists to kill.
* Option `stats_options` → `wp_stats_options`; bare `stats_url` folds in;
  `stats_db_version` → `wp_stats_version`.
* `SECTION_DISPLAY` / `SECTION_GENERAL` already correctly prefixed.
* There is a `filter_legacy_option` mechanism — check it; it may be the existing
  shim for the very problem §13 replaces.
* Hook `stats_page` → `wp_stats_page`, dropped outright.
* `.wp-env.json` sets `WP_CACHE: true` in tests — keep only if a test needs it.

## wp-sweep

* `includes/admin.php` is the only non-class file of its kind →
  `class-wp-sweep-admin.php` with a `WP_Sweep_Admin` class.
* Classes → `WP_Sweep`, `WP_Sweep_API` (acronym casing), `WP_Sweep_Command`.
* No consolidated option row — create both. Watch the existing transients
  `wp_sweep_transient_options` / `wp_sweep_details_transient_options` do not
  collide with the new `wp_sweep_options` row.
* jQuery in `includes/class-sweep.php`.
* ~16 `wp_sweep_*` hooks are the public API — do NOT rename.
* **Already has WP-CLI (`WP_Sweep_Command`) and REST (`WP_Sweep_API`)** — the
  reference for the later phase. Preserve and polish.
* `.idea/` committed. **Extra `claude.yml` / `claude-code-review.yml` and a
  `.claude/` directory — leave all three alone.**
* Destructive-operations screen: §4.3 wants bulk actions and `no_items()`.

## wp-useronline

* **Ships as 4.0.0** — 3.0.0 is live, and its published changelog promises the
  four filters are unchanged. That promise is now void; correct the line and
  spell it out in `## Upgrade Notice`.
* **The cautionary tale behind §2.1.** `class-useronline-options.php` keeps
  version markers inside the settings array under `VERSIONS_KEY`, forcing ~14
  lines (≈291-303) of re-merge plumbing. Move markers to `wp_useronline_version`
  and **delete that plumbing** — the sanitize callback must end up free of
  `get_option()`.
* Classes → `WP_UserOnline_*`; `UserOnline_WpStats` → `WP_UserOnline_WPStats`.
* Options `useronline` → `wp_useronline_options`, `useronline_most` →
  `wp_useronline_most` (not autoloaded).
* **Four hooks dropped outright**: `useronline_bots`, `useronline_buckets`,
  `useronline_custom_template`, `useronline_page` → `wp_useronline_*`.
  `USERONLINE_TRUST_PROXY` → `WP_USERONLINE_TRUST_PROXY` and
  `useronline_trust_proxy` → `wp_useronline_trust_proxy` — both documented in
  the README FAQ, so update it.
* `useronline.js` at root, jQuery → `js/wp-useronline.js`, `fetch()`.
* `includes/bots.php` is a data file, not a class — that is fine.
* §13 WP-Stats consumer.
