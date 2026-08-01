# lesterchan WordPress plugin standards

The single source of truth for all 19 plugins in this folder. Every plugin must
end up looking as though one person wrote all of them on the same afternoon. The
only permitted differences between two plugins are their **name, their features
and their capability** — nothing else.

If this document and a plugin disagree, the plugin is wrong.

Placeholders used below:

| Token | Meaning | Example (`wp-ban`) | Example (`freemyinternet`) |
|---|---|---|---|
| `{{SLUG}}` | directory name / plugin slug / text domain | `wp-ban` | `freemyinternet` |
| `{{UNDER}}` | `{{SLUG}}` with `-` → `_` | `wp_ban` | `freemyinternet` |
| `{{UPPER}}` | `{{UNDER}}` uppercased | `WP_BAN` | `FREEMYINTERNET` |
| `{{NAME}}` | display name | `WP-Ban` | `FreeMyInternet` |
| `{{CLASS}}` | class prefix | `WP_Ban` | `FreeMyInternet` |

---

## 1. Repository layout

Exactly this, in this order. Anything not on this list must be deleted or moved.

```
{{SLUG}}/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .editorconfig
├── .gitignore
├── .wp-env.json
├── bin/
│   ├── index.php
│   ├── test.sh
│   └── test-multisite.sh
├── css/                      # only if the plugin has CSS
│   ├── index.php
│   ├── {{SLUG}}.css          # front end
│   └── {{SLUG}}-admin.css    # wp-admin, only if unavoidable (see §11)
├── images/                   # only where §12 could not remove it
│   └── index.php
├── includes/
│   ├── index.php
│   ├── class-{{SLUG}}-*.php
│   ├── deprecated.php        # only if the plugin has deprecated shims
│   └── template-tags.php     # only if the plugin has template tags
├── js/                       # only if the plugin has JS
│   ├── index.php
│   ├── {{SLUG}}.js           # front end
│   └── {{SLUG}}-admin.js     # wp-admin
├── tests/
│   ├── index.php
│   ├── bootstrap.php
│   ├── helper-*.php          # every non-test file in tests/ is helper-*.php
│   ├── js/                   # only if the plugin has JS
│   │   ├── index.php
│   │   └── *.test.js
│   └── test-*.php            # every test file is test-*.php
├── tinymce/                  # only wp-downloadmanager and wp-polls
├── composer.json
├── composer.lock
├── eslint.config.mjs         # only if the plugin has JS
├── index.php
├── LICENSE
├── package.json              # only if the plugin has JS
├── package-lock.json         # only if the plugin has JS; `npm ci` requires it
├── phpcs.xml
├── phpunit-multisite.xml.dist
├── phpunit.xml.dist
├── README.md
├── uninstall.php
├── vitest.config.mjs         # only if the plugin has JS
└── {{SLUG}}.php
```

Hard rules:

* **No loose PHP, JS or CSS at the plugin root** other than `{{SLUG}}.php`,
  `index.php` and `uninstall.php`. `polls-add.php`, `polls-manager.php`,
  `print-comments.php`, `download-add.php`, `email-popup.php` and friends move
  into `includes/` as classes or as `includes/screen-*.php` partials.
* A file in `includes/` is `class-*.php`, or a `screen-*.php` partial, or one
  of the small named kinds (`deprecated.php`, `template-tags.php`). **The one
  further exception is a template a theme overrides by copying it**: its
  filename is public API, so wp-print keeps `print-posts.php` and
  `print-comments.php` under those exact names. Renaming those to fit the
  convention would break every theme that has ever overridden them.
* Assets move into `css/` and `js/`. `polls-css.css` → `css/wp-polls.css`,
  `postviews-admin.js` → `js/wp-postviews-admin.js`, and so on.
* Every directory gets a silence-is-golden `index.php` (see the template). This
  includes `bin/`, `css/`, `images/`, `includes/`, `js/`, `tests/`.
* `uninstall.php` exists in **every** plugin. `wp-relativedate` and
  `wp-showhide` currently have none — they still need one, even if it only
  deletes the single option row.
* `.wp-env.override.json` is **deleted** from every repo and gitignored. Ports
  live in the committed `.wp-env.json`; the override file is for local/CI use
  only and must never be tracked.
* `.idea/` is deleted from the working tree and gitignored.
* **The list above is what the plugin *ships*, not everything the repo may
  hold.** Do not delete `CLAUDE.md`, `.claude/`, `claude.yml` or
  `claude-code-review.yml` — they are development tooling, excluded from the
  SVN deploy, and outside this standard. Same for `htaccess.txt` and
  `Web.config.txt` in wp-dbmanager, which are shipped payloads that protect the
  backup folder.

---

## 1.1 Supported floors

**WordPress 6.8, PHP 8.2.** Raised from 6.0 / 7.4 in this pass. Both numbers
appear in **seven** places per plugin and must agree everywhere: the plugin
header, the README header, `phpcs.xml`'s `minimum_wp_version`, `.wp-env.json`'s
`phpVersion`, `composer.json`'s `require.php`, the CI matrix, and
**`composer.lock`'s platform block** — raising `require.php` without
`composer update --lock` makes Composer error, so CI fails before PHPUnit
starts.

Because PHP 8.2 is the floor, the code may use everything up to it without a
polyfill or a version guard — typed properties, constructor promotion, `match`,
named arguments, nullsafe `?->`, enums, `readonly`. Delete any remaining
back-compat shim for PHP below 8.2 rather than leaving it unreachable, and drop
any WordPress version check for below 6.8.

Raising the floors is itself a breaking change; see §14.1.

---

## 2. Naming

### 2.1 Option rows — exactly two per plugin, plus data

| Row | Name | Autoloaded | Contents |
|---|---|---|---|
| Settings | `{{UNDER}}_options` | yes | nested array of every user-editable setting, and **nothing else**. Omitted entirely by a plugin that has no settings — see below |
| Version markers | `{{UNDER}}_version` | yes | `array( 'plugin' => '2.0.0', 'db' => '3' )` — exactly these two keys |
| Volatile data | `{{UNDER}}_<noun>` | **no** | only where the plugin stores accumulating data (e.g. `wp_ban_stats`, `wp_useronline_most`) |

**A plugin with no settings and no tables stores nothing at all — not even the
version row.** wp-relativedate, wp-showhide, wp-serverinfo and wp-sweep are
template tags, a shortcode, a read-only report and a maintenance screen: none of
them keeps state between requests. For those, the version markers are the only
row the plugin writes, and they exist to tell a migration what it is upgrading
from — a migration that does not exist and may never. That is an autoloaded row
on every site, a `maybe_upgrade()` on every admin load comparing two strings, and
an `uninstall.php` whose only job is to delete what should not have been written.

The fallback is already there: every plugin here treats a missing row as "fresh
or legacy". A future version that genuinely needs state introduces the row then
and reads its absence exactly that way. Do not write a row on the chance that
one day something might want to read it.

The line is **settings or tables**, not "is it useful". freemyinternet has a
settings screen, so it keeps both rows even though it has no table.

The version markers live in **their own row**, never inside the settings array,
and there is exactly one such row per plugin holding both markers:

```php
get_option( '{{UNDER}}_version' );
// array( 'plugin' => '2.0.0', 'db' => '3' )
```

* `plugin` — the last-run plugin version, compared against `{{UPPER}}_VERSION`.
  Drives non-schema upgrade steps: re-sanitising settings, flushing caches.
* `db` — the schema counter, compared against `{{UPPER}}_DB_VERSION`. Drives
  `dbDelta()` and option-shape migrations.

This replaces today's `poll_db_version`, `postratings_db_version` +
`postratings_options_version`, `views_version`, `email_db_version`,
`ban_db_version`, `download_db_version`, `draftsforfriends_db_version`,
`print_db_version`, `stats_db_version` and wp-useronline's `versions` key.

**Why not inside the settings array.** A `register_setting()` sanitize callback
is a function from *what the form posted* to *what gets stored*. The settings
form never posts the version markers, so anything living in that array has to be
manually rescued from the stored value on every single save — see
`wp-useronline/includes/class-useronline-options.php` lines 291-303, fourteen
lines of plumbing that exist for no other reason, and the wp-useronline 3.0.0
changelog entry recording the bug they fix ("the upgrade marker could not be
saved once the settings screen had been loaded, which made the sanitise step and
the table check re-run on every request"). With a separate row that failure is
impossible by construction: the settings screen writes `{{UNDER}}_options`, the
upgrade routine writes `{{UNDER}}_version`, and neither can corrupt the other.

So every `sanitize_callback` is honest — posted input in, clean settings out,
no reaching back into `get_option()`:

```php
public function sanitize( $input ) {
	return array(
		'message'       => wp_kses_post( $input['message'] ),
		'stats_display' => ! empty( $input['stats_display'] ),
	);
}
```

Both markers are written together in one `update_option()` at the end of the
upgrade routine, so a half-finished upgrade never records itself as complete.

**Plugins with no settings do not get a settings row.** wp-relativedate and
wp-showhide expose nothing a site owner can configure. They carry
`{{UNDER}}_version` only — that row earns its place by making a future migration
possible — and no `{{UNDER}}_options`, no `register_setting()`, no
`sanitize_callback`, and no settings screen. An empty autoloaded row and a
sanitiser nothing calls are not consistency, only ceremony. `uninstall.php` in
those two removes the version row alone.

Renames to apply. For most plugins the current name only exists in the
**unreleased** major, so **retarget the migration already there** rather than
adding a second one.

**But not all of them have one.** wp-commentnavi, wp-dbmanager and
wp-pluginsused store under a name their *released* version ships, so the rename
is user-facing and they gain their **first** migration. wp-pluginsused's last
release stored nothing at all. Check which case you are in before assuming a
migration exists to retarget:

| Plugin | Old | New |
|---|---|---|
| freemyinternet | `freemyinternet` | `freemyinternet_options` |
| wp-ban | `banned_options`, `banned_stats` | `wp_ban_options`, `wp_ban_stats` |
| wp-commentnavi | `commentnavi_options` | `wp_commentnavi_options` |
| wp-dbmanager | `dbmanager_options` | `wp_dbmanager_options` |
| wp-downloadmanager | `download_options` | `wp_downloadmanager_options` |
| wp-draftsforfriends | *(various)* | `wp_draftsforfriends_options` |
| wp-email | `email_options` | `wp_email_options` |
| wp-pagenavi | `pagenavi_options` | `wp_pagenavi_options` |
| wp-pluginsused | `pluginsused_options` | `wp_pluginsused_options` |
| wp-polls | `poll_options` | `wp_polls_options` |
| wp-postratings | `postratings_options` | `wp_postratings_options` |
| wp-postviews | `views_options` | `wp_postviews_options` |
| wp-print | `print_options` | `wp_print_options` |
| wp-serverinfo | *(none)* | `wp_serverinfo_options` |
| wp-showhide | *(none)* | `wp_showhide_options` |
| wp-stats | `stats_options` | `wp_stats_options` |
| wp-sweep | *(various)* | `wp_sweep_options` |
| wp-useronline | `useronline`, `useronline_most` | `wp_useronline_options`, `wp_useronline_most` |

Every plugin additionally gains a `{{UNDER}}_version` row, replacing whichever
`*_db_version` / `*_version` row or nested `versions` key it used before.

The migration must delete every old row after folding it in, and must be covered
by a test that asserts the old rows are gone and the new ones hold the values.

### 2.2 Class constants — one spelling each

```php
const OPTION     = '{{UNDER}}_options';   // settings row;  never OPTION_NAME
const VERSION    = '{{UNDER}}_version';   // marker row holding 'plugin' and 'db'
const GROUP      = '{{UNDER}}_options';   // settings group == settings row name
const PAGE       = '{{SLUG}}';            // menu/page slug
const CAPABILITY = 'manage_options';      // see §2.7
```

Every plugin defines `OPTION` and `VERSION`. `GROUP`, `PAGE` and
`CAPABILITY` are defined **only where the plugin has an admin screen** — they
are meaningless without one, and wp-relativedate and wp-showhide have none.

`PAGE` lives on `Admin` where the plugin has one screen, and `Settings` reaches
across to `WP_{{...}}_Admin::PAGE` when registering its sections.

These need not all live on one class, and a plugin with a data screen *and* a
settings screen needs two page slugs: `WP_Stats_Admin::PAGE = 'wp-stats'` for
the menu, `WP_Stats_Settings::PAGE = 'wp-stats-settings'` for the settings page.
`CAPABILITY` belongs on whichever class owns the screen it gates, read through
the `{{UNDER}}_capability` filter (§2.7) — a plugin may define it twice, as
wp-sweep does (`activate_plugins` for the data screen, `manage_options` for
settings), provided both go through the one filter. Constants the list does not
name, such as `WP_Sweep_API::REST_NAMESPACE`, live on the class that owns them.

`OPTION_NAME`, `OPTION_GROUP`, `PAGE_SLUG`, `DB_VERSION_OPTION`,
`VERSION_OPTION`, `DB_VERSION_NAME`, `DB_VERSION`, `SLUG`, `SECTION`,
`VERSIONS_KEY` and `HANDLE` are all retired in favour of the five above plus
`SECTION_*` (§4). The *expected* versions are the PHP constants in §2.3, not
class constants — there is one source of truth for each and it is the plugin
file.

### 2.3 PHP constants

Defined at the top of `{{SLUG}}.php`, in this order, all six, every plugin:

```php
define( '{{UPPER}}_VERSION', '{{VERSION}}' );   // per §14; matches header, README, package
define( '{{UPPER}}_DB_VERSION', '1' );         // schema counter; bump when a migration is needed
define( '{{UPPER}}_SLUG', '{{SLUG}}' );
define( '{{UPPER}}_MAIN_FILE', __FILE__ );
define( '{{UPPER}}_DIR', plugin_dir_path( __FILE__ ) );
define( '{{UPPER}}_URL', plugin_dir_url( __FILE__ ) );
```

Behaviour-opt-in constants are named `{{UPPER}}_<THING>`:
`USERONLINE_TRUST_PROXY` → `WP_USERONLINE_TRUST_PROXY`,
`EMAIL_SHOW_REMARKS` → `WP_EMAIL_SHOW_REMARKS`,
`RATINGS_IMG_EXT` → `WP_POSTRATINGS_IMG_EXT`,
`SERVERINFO_WIDGET_ID` → `WP_SERVERINFO_WIDGET_ID`.

### 2.4 Classes and files

Every class is `{{CLASS}}_<Component>` — `WP_Ban_Options`, `WP_Email_Admin`,
`WP_Print_Admin`, `WP_Stats_Widget`, `FreeMyInternet_Admin`. The bootstrap class
is plain `{{CLASS}}`. No unprefixed globals survive.

File name is the class name lowercased with `_` → `-`, prefixed `class-`:
`WP_Ban_Options` → `includes/class-wp-ban-options.php`.

Casing is fixed to the display name: `WP_PostRatings_*` (not `Postratings_*`),
`WP_DownloadManager_*`, `WP_DraftsForFriends_*`, `WP_CommentNavi_*`,
`WP_PageNavi_*`, `WP_PostViews_*`, `WP_UserOnline_*`, `WP_DBManager_*`,
`WP_ServerInfo_*`. The WP-Stats integration component is spelled `_WPStats`
everywhere (retire `_WpStats`).

Component names are drawn from this fixed vocabulary — use the existing name if
it is on the list, and prefer a listed name over inventing one:

`Admin`, `Cron`, `Display`, `Install`, `List_Table`, `Options`, `Settings`,
`Template`, `Widget`, `WPStats`.

`class-wp-postratings-logs-table.php`-style specific list tables keep their noun
but end in `_Table`: `WP_Email_Logs_Table`, `WP_Ban_Stats_Table`.

**The list is a preference, not a closed set.** A plugin with genuine components
of its own keeps their nouns: wp-dbmanager has `Backups`, `Database`, `Folder`,
`Mailer`, `Screens` and `Tables`; wp-commentnavi and wp-pagenavi have `Core` and
`Call`. Reach for a listed name when one fits; do not rename a meaningful
component into a worse one to satisfy the list.

`wp-sweep/includes/admin.php` becomes `class-wp-sweep-admin.php`.

### 2.5 Functions

Global functions exist only in `includes/template-tags.php` and
`includes/deprecated.php`. Everything else is a class method. Template tags keep
the names they shipped with in the last SVN release — those are the documented
public API and must not be renamed.

Any other global function is prefixed `{{UNDER}}_`.

### 2.6 Hooks

Every filter and action is `{{UNDER}}_<verb_noun>` — `wp_useronline_bots`,
`wp_pluginsused_plugins_used`, `wp_postviews_should_count`,
`freemyinternet_should_display`.

**The old unprefixed names are dropped outright** (your call). List every one
under `## Upgrade Notice` in the README. Do not add `apply_filters_deprecated()`
shims for them.

Renames required:

| Plugin | Old | New |
|---|---|---|
| wp-pluginsused | `pluginsused_hidden_plugins`, `pluginsused_plugins_used`, `pluginsused_show_version` | `wp_pluginsused_*` |
| wp-postviews | `postviews_should_count`, `the_views`, `postviews_increment_views`, `postviews_increment_views_ajax` | `wp_postviews_*` (all four; the last two have been public since 1.68) |
| wp-useronline | `useronline_bots`, `useronline_buckets`, `useronline_custom_template`, `useronline_page` | `wp_useronline_*` |
| wp-postratings | `rate_post` | `wp_postratings_rate_post` |
| wp-stats | `stats_page` | `wp_stats_page` |
| wp-downloadmanager | `download_embedded`, `downloads_page` | `wp_downloadmanager_embedded`, `wp_downloadmanager_page` |

Core hooks the plugin *consumes* (`the_content`, `widget_title`,
`comment_text`, `rss2_head`…) are untouched — this rule is about hooks the
plugin *fires*.

Every fired hook is documented with a `@since` and a docblock immediately above
it, per WPCS.

### 2.7 Capabilities

Settings screens require `manage_options`. A plugin that already ships a custom
capability keeps it for its **data** screens only, and every check of *the
plugin's own* capability goes through one filter:

```php
apply_filters( '{{UNDER}}_capability', self::CAPABILITY, $context );
```

**What belongs behind the filter:** any gate the plugin invents over its own
screens or its own data. wp-useronline's `edit_users` check over visitor
locations and IP addresses was one of these and was wrongly hardcoded; it is now
`capability( 'details' )`. A context need not be a screen.

**What must never go behind it**, because these are core's decisions and routing
them through a plugin filter would let a site filter away a protection it does
not own:

* **Core meta-capabilities** — `current_user_can( 'edit_post', $id )` and
  friends. These are per-object and already answerable by core.
* **`unfiltered_html`.** It decides whether kses runs. A plugin that lets a site
  filter this has handed out stored XSS.
* **Editor-integration gates** — the `edit_posts || edit_pages` pair that decides
  whether to register a Classic Editor button. That is core's idiom for "may use
  the editor at all", not a plugin permission.

An earlier version of this section said "every capability check goes through one
filter" with no exceptions. That was wrong, and five plugins were right to be
ignoring it.

Existing custom capabilities to preserve: `wp-email` (`manage_email`),
`wp-postratings` (`manage_ratings`), `wp-dbmanager` (`install_plugins`),
`wp-draftsforfriends` (`publish_posts`), `wp-downloadmanager`
(`manage_downloads`, which has shipped since its first release). The custom
capability gates the plugin's **data** screens; Settings stays on
`manage_options`.

---

## 3. Plugin header and README

### 3.1 `{{SLUG}}.php` header

Byte-identical structure everywhere; only the four content lines differ.

```php
<?php
/**
 * Plugin Name: {{NAME}}
 * Plugin URI: https://lesterchan.net/portfolio/programming/php/
 * Description: <one sentence, no trailing markup>
 * Version: {{VERSION}}          # per §14, NOT literally 3.0.0
 * Requires at least: 6.8
 * Requires PHP: 8.2
 * Author: Lester 'GaMerZ' Chan
 * Author URI: https://lesterchan.net
 * License: GPLv2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: {{SLUG}}
 * Domain Path: /languages
 *
 * @package {{NAME}}
 */
```

The GPL comment block that follows is the **"or later" variant**, verbatim:

```
/*
	Copyright 2026  Lester Chan  (email : lesterchan@gmail.com)

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.
	…
*/
```

Two spaces after the year and around `email :`. Normalise the one-space variants.

**This must be the "or later" form.** Five plugins — including wp-showhide —
carry a v2-**only** block (`under the terms of the GNU General Public License,
version 2, as published by the Free Software Foundation`, with no "or at your
option any later version"). That contradicts the `License: GPLv2 or later`
header two lines above it and the `GPL-2.0-or-later` in composer.json, so those
five ship a self-contradicting licence statement. Fourteen already use the
correct form; bring the other five into line, never the reverse.

### 3.2 `README.md` header

Nine lines, lines 2–9 ending in **two spaces**, line 10 with none:

```
# {{NAME}}
Contributors: GamerZ␣␣
Donate link: https://lesterchan.net/site/donation/␣␣
Tags: <five tags, comma separated>␣␣
Requires at least: 6.8␣␣
Tested up to: 7.0␣␣
Stable tag: 3.0.0␣␣
Requires PHP: 8.2␣␣
License: GPLv2 or later␣␣
License URI: https://www.gnu.org/licenses/gpl-2.0.html
```

Nine fields after the `#` heading. Exactly **five** tags.

`Contributors:` is **`GamerZ` and nothing else**, in every plugin without
exception. wp-pagenavi currently reads `GamerZ, scribu`; drop the second name.

### 3.3 `README.md` body

**Level-2** headings, in this order, and no other `##` heading. Level-3
headings are free — `## Changelog` necessarily contains `### 2.0.0`, and
`### Features` below is an h3. The closed set is the h2s:

```
## Description
### Features            (optional, only if the plugin has a bullet list)
## Usage                (h2, never "General Usage")
## Frequently Asked Questions
## Screenshots
## Changelog
## Upgrade Notice
```

* `### Development` and `### Credits` are removed. Development instructions live
  in the repo, not the wordpress.org readme.
* **`### Donations` is kept**, as the last h3 of `## Description`, with exactly
  this wording in all 19 — a plain paragraph, no bullet:

  > I spent most of my free time creating, updating, maintaining and supporting
  > these plugins, if you really love my plugins and could spare me a couple of
  > bucks, I will really appreciate it. If not feel free to use it without any
  > obligations.

  Today 17 plugins carry it in three variants: 10 exactly as above, 5 with a
  stray `* ` bullet prefix, and 2 with "as my school allowance" — drop that
  clause. freemyinternet and wp-relativedate removed it and must get it back.
* **Every breaking change goes under `## Upgrade Notice`**, keyed by version,
  written for a site owner not a developer. `## Changelog` keeps the full list
  including the `IMPORTANT:`/`BREAKING:` lines, but Upgrade Notice is where the
  "what will break for you and what to do" prose lives.
* Changelog entry prefixes are exactly one of `BREAKING:`, `NEW:`, `CHANGED:`,
  `FIXED:`, `NOTE:` — in that order within a version. wp-ban's `IMPORTANT:` is
  renamed to `BREAKING:`.
* The consistency work in this pass is **folded into the existing unreleased
  major entry**. Do not bump the version, do not add a new heading.
* Code fences are ` ```php ` or ` ```javascript ` only — `plugin_deploy.sh`
  rewrites exactly those two plus bare ` ``` ` into `~~~`, one per line.

---

## 4. Admin screens

### 4.1 Menu rule

One rule, applied everywhere:

* A plugin whose only admin surface is settings uses **`add_options_page()`**
  under Settings. Page slug is `{{SLUG}}`. No top-level menu.
* A **read-only table sitting beneath a settings form does not earn a top-level
  menu.** wp-ban has a `WP_List_Table` of ban counters under its settings
  screen and stays at `Settings → Ban`, where it has always been. The test is
  whether the plugin has screens a site owner *manages things on*, not whether
  a `WP_List_Table` appears anywhere.
* A plugin with **data-management screens** (list tables, add/edit forms, logs)
  gets **one top-level menu** (`add_menu_page()`, slug `{{SLUG}}`) whose first
  submenu is the data screen and whose last submenu is `Settings`. **Only where
  there are more screens than a tab strip can carry** — with exactly two, the
  menu holds one tabbed page instead and there are no submenus at all (§4.2.1).
* A plugin whose screen is a **read-only report** — no settings form, no list
  table, no add/edit — gets a top-level menu **only if it has a second screen to
  put under it.** wp-stats does (report, then Settings, now the two tabs of one
  page — §4.2.1), and had been split
  between a Dashboard widget and a Settings page, which is the scattering this
  rule exists to stop. wp-serverinfo does not: it is five read-only tables and
  nothing else, so it uses `add_management_page()` under **Tools**, where core
  keeps read-only screens about the installation (Site Health, Export). A
  top-level menu for a single report claims a sidebar slot it has not earned,
  and `add_options_page()` would file a report under Settings with no settings
  on it.

> **wp-sweep is under Tools, and this paragraph used to say the opposite.** The
> move to `add_management_page()` was tried on 2026-07-30 and reverted; the note
> recording that ended "do not re-litigate without deciding the tab question
> first", and by the time anyone looked again the tab question *had* been decided
> (§4.2.1) and the code had moved. Both halves of the old objection are gone:
> **wp-sweep has no settings screen at all** — no `register_setting()`, no
> sections — so the "where do the settings go" problem it described never
> existed, and a plugin with one screen and no second one to put under it does
> not earn a top-level menu by this section's own rule. Sweeping is maintenance
> against the installation, which is what core puts under Tools.
>
> The lesson is not about wp-sweep. **A decision recorded with a condition
> attached goes stale the moment the condition is met, and nobody notices,
> because the note still reads as settled.** This one disagreed with the shipped
> code for an unknown length of time. When a rule here is written as "not until
> X", come back and close it when X happens.
* **No two plugins share a dashicon.** They sit in the same sidebar, and at
  20px an icon is most of what tells one entry from another. wp-polls and
  wp-stats both shipped `dashicons-chart-bar` until somebody noticed they looked
  identical. Where two plugins have a fair claim on the same icon, it goes to
  the one whose screen literally draws that thing — wp-polls renders bars, so
  wp-stats took `dashicons-chart-area`. Current allocation: `chart-bar`
  wp-polls, `chart-area` wp-stats, `star-filled` wp-postratings, `groups`
  wp-useronline, `email-alt` wp-email, `download` wp-downloadmanager, `archive`
  wp-dbmanager.

* **The menu title is the plugin's name, exactly as the plugin header spells
  it.** `WP-Polls`, not `Polls` or `Manage Polls`; `WP-DBManager`, not
  `Database`; `WP-EMail`, not `E-Mail`. This is the second argument to
  `add_menu_page()` / `add_options_page()` / `add_management_page()`, and it
  applies whether the entry sits at the top level or under Settings.

  Three conventions were in use before this rule — the full name (5 plugins),
  the name with `WP-` stripped (5), and a plain noun (7) — which is the "written
  by different people" problem in its purest form. The full name wins for two
  reasons. A site owner installs `WP-Polls` and sees `WP-Polls` on the Plugins
  screen, so that is the string they look for in the sidebar. And these plugins
  are a family that gets installed several at a time: as plain nouns they scatter
  through the sidebar as Database, Downloads, E-Mail, Ratings, Sweep with nothing
  connecting them, where the real names sort together.

  **The page title, the `<h1>` and the submenu labels do not follow this rule**
  — they say what the screen *is*, and **never carry the `WP-` prefix**. So the
  sidebar reads `WP-Polls → Manage Polls / Add Poll / Settings`, and the heading
  on the first of those is "Manage Polls". The first submenu names the data
  screen, the last is always `Settings`.

  The prefix belongs in the sidebar, where a site owner is matching what they
  installed against a list of everything else installed. It is noise on the
  screen itself, where they already know where they are: `Ban Options`,
  `Plugins Used`, `Manage Ratings`, `Sweep`, `Server Information`, `Stats`.
* **Settings last, unless the other screen is a log.** The data screen comes
  first when it is the thing a site owner came for — Manage Polls, the download
  list, the backup list. It does not when it is a *record* rather than a
  workspace: wp-postratings' log of who rated what is for spotting abuse and
  little else, so that menu opens on Settings and the second entry is called
  **Logs**, named for what it is rather than for managing anything.

  The test is what somebody opens the menu to do. If the answer is "look
  something up occasionally", Settings goes first. wp-email's log is the same
  shape and is the other candidate; it has not been changed.

* **Never spell out an admin hook suffix, and do not derive it either. Record
  it.** `add_menu_page()` and `add_submenu_page()` each hand back the hook they
  registered. Keep those and enqueue against them:

  ```php
  self::$screen_hooks[] = add_menu_page( … );
  self::$screen_hooks[] = add_submenu_page( … );
  ```

  Anything else drifts, silently, because nothing errors when it does: the
  screen still loads and only its stylesheet and script stop being enqueued.
  wp-postratings lost its shape picker to this **twice in one day** — every
  shape is a CSS mask from that stylesheet, so the screen became a list of
  labels:

  1. `'ratings_page_'` was written out, and renaming the menu to `WP-PostRatings`
     moved the real hook to `wp-postratings_page_…`.
  2. It was then *derived* from the menu title, which fixed the rename — and
     broke again when Settings became the top-level entry, because a top-level
     page's hook is `toplevel_page_{{SLUG}}` and owes nothing to the title.

  Deriving survives a rename and not a reorder. Recording survives both.

  Assert it by comparing `screen_hooks()` against `get_plugin_page_hookname()`
  for the slugs actually in `$submenu` after `menu()` has run — never against a
  hand-built string, which is how the old test kept passing while the real
  screen had no stylesheet.

* **Settings never span more than one page.** More than one settings group
  becomes **tabs on that single page** at `?page={{SLUG}}&tab=<tab>`, rendered
  with `nav-tab-wrapper` / `nav-tab` / `nav-tab-active`. Never a second submenu
  entry.

This is what fixes wp-postratings (tabs are right, but reachable inconsistently)
and wp-downloadmanager (settings scattered across menu entries).

### 4.2 Settings API — mandatory, no exceptions

Every settings screen is built from:

`register_setting()` → `add_settings_section()` → `add_settings_field()` →
`settings_fields()` + `do_settings_sections()` + `submit_button()`.

* **Zero hand-written `<table class="form-table">`.** `do_settings_sections()`
  emits it.
* Section constants are `SECTION_<NAME>` = `'{{UNDER}}_<name>'`.
* One `sanitize_callback` per registered setting, returning the whole nested
  array. It is the only place values are cleaned, and it re-sanitises on upgrade
  as well as on save.
* Field callbacks live on the `WP_{{...}}_Settings` class, one method per field,
  named `field_<name>()`. This holds even where §2.4's component list also names
  an `Admin` class for the plugin: `Admin` owns the menu and the screens,
  `Settings` owns `register_setting()`, the sections, the fields and the
  sanitiser. A plugin small enough to have only one of the two puts everything
  there.
* `add_settings_error()` for every message. No hand-rolled `<div class="updated">`.

### 4.2.1 Tabs — when a screen becomes a tab, and what the tabs are called

**A plugin with exactly two screens is one page with tabs, not two submenus.**
It keeps its top-level menu; what goes away is the submenu list. The data screen
is the first tab and `Settings` is the last:

| Plugin | Tabs |
|---|---|
| wp-stats | `Statistics` / `Settings` |
| wp-useronline | `Users Online` / `Settings` / `Templates` |
| wp-ban | `Stats` / `Settings` / `Templates` |

**Flat, never nested.** wp-useronline has a data screen, settings and templates,
and that is one strip of three tabs — not a Settings tab containing its own
Settings/Templates strip. Two tab rows on one page is worse than the sprawl
either was meant to fix.

A plugin with **real data management** — a list table with add and edit screens,
a log — keeps submenus: wp-polls, wp-postratings, wp-downloadmanager and
wp-email all have more screens than a tab strip can carry, and their Settings
screen is itself tabbed. The dividing line is the number of screens, not their
kind.

**Two things break when a screen becomes a tab, and both are worse than the
layout.**

*Capabilities.* If the two screens are gated differently — wp-useronline has a
`wp_useronline_capability` filter with a per-screen context — the **page** takes
the lower capability and **each tab then checks its own**. Skip the second half
and filtering the report down to `list_users` silently opens the settings form
to the same role. That is privilege escalation dressed as a layout change.

*Forms.* A data screen must not post to `options.php`. A list table brings its
own bulk-action form and its own nonce, and `WP_List_Table::display_tablenav()`
emits a `_wpnonce` for `bulk-{$plural}` that overrides any `wp_nonce_field()` in
the same form — see wp-ban's `STATS_NONCE`.

### 4.2.2 Tabs — `Settings` and `Templates`, and templates always get their own

**A plugin that has a template puts it on a tab of its own.** Templates are long
text fields with a list of permitted variables under each; left inline they bury
the settings above them, and wp-email's eight templates sat below several
screenfuls of options. The split is not cosmetic — it is what stops a settings
page becoming a wall.

**The tabs are named exactly `Settings` and `Templates`.** Not "Poll Options"
and "Poll Templates", not "General". The page heading already says which plugin
this is, so repeating the name in every tab is noise. Five of the six plugins
with tabs disagreed with each other before this was written down:

| Plugin | Was | Now |
|---|---|---|
| wp-postratings | `Settings` / `Templates` | the model, unchanged |
| wp-polls | `Poll Options` / `Poll Templates` | `Settings` / `Templates` |
| wp-downloadmanager | `General` / `Templates` | `Settings` / `Templates` |
| wp-print, wp-email, wp-postviews, wp-useronline | one long page | two tabs |

**Renaming a tab is never only the label.** wp-polls printed an admin notice
linking to "Poll Templates" and its README told people to look under "Poll
Options"; wp-downloadmanager's e2e suite asserted the active tab read
"General". A rename that stops at the tab strip sends people to a screen name
that no longer exists. Grep the whole plugin, README included.

**One `register_setting()` and one option row across both tabs**, per §2.1.
Tabs are a rendering decision, not a storage one.

**The trap, and it destroys data.** `register_setting()`'s `sanitize_callback`
is handed **only the fields the submitting form posted**, so a sanitiser that
returns just what it was given wipes everything the other tab owns the moment
either tab is saved. Somebody customises eight email templates, later changes an
unrelated setting, and the templates are gone with no error. The sanitiser must
merge the submitted subset over the stored value — wp-postratings and wp-polls
both already do this, so copy one of them rather than re-deriving it.

Every tabbed plugin carries a test that **saves one tab and asserts the other
tab's values survive**. It is the regression this design invites, and it is
silent.

**`settings_errors()` cuts both ways, and the answer depends on which function
registered the page.** Core calls it from `wp-admin/options-head.php`, which
`admin-header.php` requires only when `$parent_file` is `options-general.php`.
So an `add_options_page()` screen — wp-ban, wp-print — already has its notices
printed, and calling it again renders every one of them twice. A screen under a
top-level menu or under Posts is dispatched elsewhere, core never calls it, and
a save reports nothing at all unless the plugin calls it itself. Both mistakes
look identical from the code: one line, present or absent. Check the parent
before deciding, and carry a test either way — "the notice appears exactly once"
covers both failures with one assertion.

The tab links must preserve the active tab across a save. The Settings API
posts to `options.php`, which redirects to `_wp_http_referer`; print a second
one naming the tab after `settings_fields()`, since PHP keeps the last of a
repeated name.

### 4.3 List tables

Every tabular data screen is a `WP_List_Table` subclass. No hand-rolled
`<table>`. wp-dbmanager is the reference implementation. Normally: pagination at
20, sortable columns, row actions on hover, bulk actions where destructive
operations exist, and a `no_items()` message.

**Two of those yield to a good reason, and wp-dbmanager is where both do:**

* *Pagination* is wrong for a bounded table that carries a totals row — the
  tables list would reduce "select all" to "select this page" and its totals to
  per-page sums, and the backups list is already capped by `max_backup`.
* *Hover row actions* are wrong when every action is destructive. A row action
  is a GET, and one browser prefetch away from restoring over a live database.
  Route destructive operations through POST bulk actions instead.

If you deviate, say why in the commit message, as wp-dbmanager did.

### 4.4 Markup

Only core classes — any class core itself emits, not just the common ones
listed here: `wrap`, `form-table`, `regular-text`, `large-text`, `small-text`,
`button`, `button-primary`, `notice notice-{success,error,warning,info}`,
`widefat`, `striped`, `nav-tab-wrapper`, and the list-table furniture
(`alignleft actions`, `hide-if-no-js`, `form-wrap`) that `extra_tablenav()`
exists to emit. The rule bans *invented* classes and inline styles, not core's
own vocabulary. One `<h1>` per screen. No inline
`style`, `width`, `valign` or `align` attributes anywhere.

---

## 5. Front-end styles

* Scoped under a single root class `.{{SLUG}}` on the outermost element.
* Inherit `font-family`, `font-size` and `color` from the theme. Never set them.
* Colours use `currentColor` or a CSS custom property with a sensible fallback:
  `var(--{{SLUG}}-bar-bg, #4a90d9)`. Never a hardcoded hex in a rule that a
  theme would want to override.
* No `!important`.
* `prefers-color-scheme: dark` handled where the plugin paints its own surface.
* `prefers-reduced-motion: reduce` respected by any transition.
* Enqueued with `wp_enqueue_style( '{{SLUG}}', {{UPPER}}_URL . 'css/{{SLUG}}.css', array(), {{UPPER}}_VERSION )`.

### 5.1 RTL — no separate stylesheet

There is **no `-rtl.css` in any plugin.** A second sheet is a second thing to
keep in step, and it only exists because the first sheet used physical
properties. Write direction-neutral CSS instead and one file serves both:

| Never | Always |
|---|---|
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` |
| `padding-left` / `padding-right` | `padding-inline-start` / `padding-inline-end` |
| `left` / `right` | `inset-inline-start` / `inset-inline-end` |
| `text-align: left` / `right` | `text-align: start` / `end` |
| `border-left` / `border-right` | `border-inline-start` / `border-inline-end` |
| `float: left` / `right` | `float: inline-start` / `inline-end`, or flex/grid |

All of these are supported well below the plugins' WordPress 6.8 floor.

Delete `wp-email/email-css-rtl.css` and `wp-print/print-css-rtl.css`, fold any
rule they carried that is not merely a mirrored physical property into the main
sheet, and remove the matching `wp_style_add_data( …, 'rtl', … )` call. Add a
test asserting the plugin registers no `rtl` style data and ships no `*-rtl.css`.

---

## 6. JavaScript

* **Zero jQuery.** No `jquery` in any `wp_enqueue_script()` dependency array, no
  `$`/`jQuery` in any `.js` file, and none in the two TinyMCE plugins. The
  TinyMCE Classic Editor buttons stay — rewrite `plugin.js` in vanilla JS.
* Vanilla ES2017 (`const`/`let`, arrow functions, `fetch`, `addEventListener`,
  `dataset`, `URLSearchParams`, optional chaining). No build step, no bundler.
* No global functions. Everything inside an IIFE or a module-scoped closure.
* Behaviour attaches through `data-*` attributes, never inline `on*` handlers.
* AJAX uses `fetch()` against `admin-ajax.php` with a nonce, `credentials: 'same-origin'`.
* Server data arrives via `wp_localize_script()` into a single object named
  `{{CLASS}}L10n` in lowerCamel: `wpBanL10n`, `wpPollsL10n`, `wpEmailL10n`.
  Declared as a `readonly` global in `eslint.config.mjs`.
* Every plugin with a `js/` directory has `tests/js/*.test.js` covering it, run
  by vitest + jsdom.

---

## 7. Testing

### 7.1 Structure

* `tests/bootstrap.php` — loads the WP test library and the plugin.
* `tests/helper-*.php` — every non-test file. `testcase.php`,
  `class-wp-postratings-testcase.php`, `helper-fixtures.php` etc. all become
  `helper-testcase.php`, `helper-fixtures.php`, `helper-source.php`.
* `tests/test-*.php` — every test file. One class per file, named
  `{{CLASS}}_<Area>_Test`, extending `{{CLASS}}_TestCase` (in
  `helper-testcase.php`) which itself extends `WP_UnitTestCase`.
* Test methods are `test_<what_it_asserts_in_words>()` — long and prose-like.
  They need no docblock, because the name is the documentation; add one only
  where it carries reasoning the name cannot, or where PHPUnit requires it
  (`@dataProvider`, `@covers`). Every assertion carries a message explaining the
  failure.

### 7.2 Shared tests every plugin must have

Every plugin carries `tests/test-metadata.php`. The idea and several of the
assertions come from `wp-showhide/tests/test-metadata.php`, but **the names and
structure below win over what that file currently contains** — it predates §7.1
and declares `class Test_ShowHide_Metadata extends WP_UnitTestCase`, which the
standard now forbids. wp-showhide's agent brings it into line like everyone
else; nobody copies it as-is.

* `test_every_readme_header_line_keeps_its_line_break()` — nine header fields,
  eight with two trailing spaces, the ninth with none.
* `test_canonical_lesterchan_urls()` — Plugin URI, Author URI, Donate link,
  License URI.
* `test_contributors_is_gamerz_only()` — the README `Contributors:` field is
  exactly `GamerZ`.
* `test_text_domain_is_the_plugin_slug()` — Text Domain and `/languages`.
* `test_version_matches_everywhere()` — header `Version:`, README `Stable tag:`,
  and `{{UPPER}}_VERSION` agree.
* `test_requires_headers_match_readme()` — `Requires at least` and
  `Requires PHP` agree between header and README.
* `test_readme_sections_are_the_canonical_set()` — §3.3 headings, in order.
* `test_changelog_prefixes_are_canonical()` — every changelog bullet starts with
  one of the five allowed prefixes.
* `test_no_jquery_is_enqueued()` — no script registered by the plugin declares a
  `jquery` dependency.
* `test_every_directory_has_an_index_php()`.
* `test_uninstall_removes_every_option_row()` — asserts nothing matching
  `{{UNDER}}_%` survives, single site **and** multisite.
* `test_version_row_holds_exactly_plugin_and_db()` — `{{UNDER}}_version` is an
  array whose keys are exactly `plugin` and `db`, nothing more (§2.1).
* `test_settings_sanitizer_never_stores_version_markers()` — round-trip the
  sanitize callback and assert the result contains no `version`, `db_version` or
  `versions` key. This is the regression guard for the wp-useronline bug: it
  fails the moment someone moves a marker back into the settings array.
  **Skipped by the two plugins with no settings row**, which have no sanitiser;
  they assert instead that no `{{UNDER}}_options` row is ever created.
* `test_no_rtl_stylesheet_is_registered()` — the plugin ships no `*-rtl.css` and
  registers no `rtl` style data (§5.1).

### 7.2.1 Process-wide state, and globals the harness nulls on purpose

Two families of trap accounted for most of the first PHPUnit run's fallout, each
proven across several plugins. Check for them before concluding a plugin is
broken.

**State no transaction rolls back.** A test that asserts something is *absent*
is really asking about every test that ran before it:

* `WP_Scripts` / `WP_Styles` — `wp_script_is( …, 'enqueued' )` answers for the
  whole process. Start from `new WP_Scripts()`.
* `$menu` / `$submenu` — plain globals.
* **`add_settings_error()`'s queue** — three of six plugins had a screen
  rendering an earlier screen's notices.
* The widget factory — re-firing `widgets_init` **empties it**, because core's
  `_register_widgets()` at priority 100 removes anything already in
  `$wp_registered_widgets`.

**Globals `WP_UnitTestCase_Base::tear_down()` deliberately nulls**, so a theme
switch or screen cannot leak between tests: `$wp_stylesheet_path`,
`$wp_template_path`, `$current_screen`, `$taxnow`, `$typenow`, `$wp_sitemaps`,
and the three comment globals. Core functions that re-derive them lazily are
fine; ones that read them directly are not, and fail **only** under test:

* `comments_template()` reads `$wp_stylesheet_path` straight into
  `trailingslashit()` rather than re-deriving it as `locate_template()` does, so
  it hands `null` to `rtrim()`. On a real request `wp-settings.php` has populated
  it long before any plugin loads. This one cause was **23 of the 35** failures
  left after the first pass, across wp-commentnavi and wp-print. The fix is
  `wp_set_template_globals()` in `set_up()` — restore the precondition the
  harness broke, do not work around it in the plugin.
* `WP_Site_Health::enqueue_scripts()` reads `$current_screen`, so a nulled one
  kills `do_action( 'admin_enqueue_scripts' )`.

**`add_menu_page()` and `add_submenu_page()` are asymmetric.** The first does
*not* consult the current user — it records the capability as element 1 of the
menu item and WordPress enforces it later in `_wp_menu_output()`. The second
**does** check. So a test asserting a page is absent from `$menu` for a
subscriber tests something WordPress does not do, while the same test against a
*submenu* works. Every plugin with a top-level menu plus a Settings submenu has
that exposure.

**Three of these are harder to write than they look.** wp-showhide hit all
three; do not rediscover them:

* `test_uninstall_removes_every_option_row()` has to `require_once` the
  uninstaller *inside* the test, which defines a global function. **Only one
  test file per plugin may ever do this** — a second one fatals on redeclare,
  and a plugin that already had an uninstall test now has two places wanting it.
  Put the include behind a shared `run_uninstall()` in `helper-testcase.php` and
  have both call that, as wp-pluginsused does.

  **That does not work for a plugin whose uninstaller drops a table** — the
  include would drop the table the rest of the suite runs against, and
  `require_once` fires for the first caller only, so a second test file asking
  for it silently proves nothing. wp-sweep and wp-draftsforfriends both do the
  other thing: `run_uninstall()` performs the deletions itself, and a separate
  test asserts `uninstall.php` names the same rows and delegates the drop.
  Either shape is fine; pick by whether the uninstaller touches schema.
* `test_every_directory_has_an_index_php()` needs a **pruning** iterator
  (`RecursiveCallbackFilterIterator`), not a filter applied after the fact. A
  plain filter descends into `node_modules` and `vendor` before discarding
  them, which is slow enough to look like a hang.

  **Its skip list must include `artifacts`.** Playwright writes traces,
  screenshots and its stored session there, so the first plugin to gain an e2e
  suite starts failing a metadata test that has nothing to do with e2e — and
  only after somebody has run the suite locally, which means CI stays green and
  the failure looks like it came from whatever was touched that day. wp-polls
  did exactly this. The list was five different arrays across the collection
  when this was found, so §7.2's shared `test-metadata.php` is the fix; until
  that lands, every copy carries `artifacts`.

* **A metadata test that forbids loose files in the plugin root must exempt
  `*.config.js`.** `playwright.config.js` lives in the root because Playwright
  resolves every path in it relative to itself, so a rule asserting
  `glob( '*.js' )` is empty fails the moment a plugin gains an e2e suite. The
  rule means "no *source* scripts loose in the root", and a tool config is not
  a script the plugin ships to a browser — `bin/verify.py` already draws that
  line by allowing `*.config.js` and `*.config.mjs` at the root, so the two
  agreeing is the point. Only wp-print carries this test today.

  Both of these are the same shape, and worth naming as a class: **a metadata
  rule written before e2e existed will fire on e2e scaffolding.** When one
  does, decide whether the scaffolding is genuinely violating the rule's intent
  or whether the rule simply predates it, and widen the rule rather than moving
  the file — the file is where the tool requires it to be.
* `test_no_jquery_is_enqueued()` is not just a source grep for a plugin that has
  JS. Assert **both** that the registered handle's `deps` array is empty *and*
  that `js/*.js` contains no `jQuery`/`$(` — a grep alone passes a dependency
  array built at runtime. For a plugin that registers **no** scripts at all
  there is no handle to inspect, so assert that `wp_enqueue_script(` appears
  nowhere in the source, which is a stronger claim than the two-part form.
  **Keep the opening bracket.** Without it the needle is also a substring of the
  action name `wp_enqueue_scripts`, which a plugin legitimately hooks to enqueue
  a *stylesheet* — wp-stats failed on precisely that, and four siblings were
  carrying the same assertion, passing only because they had no sheet yet.

### 7.2.2 Capabilities do not mean the same thing on a network

The multisite sweep failed in seven plugins the first time it was run, and in
five of the seven the single cause was this: **core's `map_meta_cap()` adds a
network-level requirement to several ordinary capabilities under multisite.** A
site administrator is not a weaker super admin; it is a different thing, and a
test that logs one in is testing a different user than it thinks.

The ones that bit, all verified against core rather than remembered:

| Capability | What multisite adds | Bit |
|---|---|---|
| `activate_plugins` | `manage_network_plugins`, unless the network admin has delegated the Plugins menu — not delegated by default | wp-sweep, wp-downloadmanager |
| `install_plugins` | `do_not_allow` outright for anyone who is not a super admin | wp-dbmanager |
| `edit_users` | `manage_network_users` | wp-useronline |
| `unfiltered_html` | super admins only | wp-print |

**The rule: when a network denies a capability, assume core is right and fix the
test, not the plugin's gate.** Weakening a gate to make a test pass hands a
network-level power to every site administrator on every network running the
plugin — wp-dbmanager's Run SQL Query console is the worst case. Give the test
the privilege the real operator would have:

```php
protected function create_admin() {
	$user_id = self::factory()->user->create( array( 'role' => 'administrator' ) );

	if ( is_multisite() ) {
		grant_super_admin( $user_id );
	}

	return $user_id;
}
```

Put it on the shared test case, route **every** administrator the suite creates
through it, and leave the tests that assert the *unprivileged* path setting their
own subscriber or editor explicitly — those stay meaningful and must not be
routed through this.

**Grant super admin only where the plugin's own capability needs it.** The helper
is on every plugin, but its body follows the capability, which is one of the
three things plugins are allowed to differ on. A plugin whose surface is
`manage_options` needs no grant: a site administrator holds that under both, and
granting anyway would make the test user stop representing the operator the
plugin actually has, hiding exactly the class of bug this section is about. As of
the first green multisite sweep, only wp-sweep, wp-dbmanager and wp-print need
the grant; eleven plugins still create administrators inline and should be
routed through a helper for shape, without one.

Two exceptions where the plugin *was* wrong, and which are the shape to look for:

* **A capability used as a proxy for something else.** wp-downloadmanager read
  `activate_plugins` to mean "level 10", so every site administrator on every
  network silently dropped to level 7 and lost the downloads on their own site.
  Where the question is "does this person administer *this site*", the answer is
  `manage_options`: it holds under both, and no standard role has one of the two
  without the other, so single-site behaviour does not move.
* **A gate outside the plugin's own capability filter** (§2.7). wp-useronline
  hardcoded `edit_users`, so under multisite a site administrator could not see
  the visitors to their own site and no site could correct it.

And one that is not about capabilities at all but failed for the same reason —
believing the single-site install is the whole world:

* `wp_get_sites()` was **never removed**; it is deprecated and still ships in
  `wp-includes/ms-deprecated.php`, which is loaded for multisite only. So
  `! function_exists( 'wp_get_sites' )` passes single-site for the wrong reason
  and fails as a network. wp-polls asserted exactly that.

### 7.2.3 A suite that dies is not a suite that passed

`bin/test-all.sh` must confirm PHPUnit reached a verdict, not merely that the
command exited 0. A test that reaches a real `wp_send_json_*()` or `wp_die()`
ends in `die()`, which terminates the PHP process — and PHPUnit with it —
**mid-run and with status 0**. wp-sweep did this on its first multisite run: it
stopped at test 96 of 384, printed no summary, and was recorded as passing while
46 tests had already errored. The harness now requires a line matching
`OK (`, `OK, but `, `FAILURES!`, `ERRORS!` or `No tests executed`, and treats its
absence as a failure. Do not remove that check.

### 7.2.4 Escaping a stored value is a test, not a habit

**Every plugin that echoes a value it read from the database carries an escaping
regression test for it.** The stored XSS that gated a wp-polls release was a
value going to the page without escaping; the guard against the next one is not
"we escape carefully" but a test that fails the moment an output stops
escaping. This is a shared obligation like the metadata tests, scoped to the
outputs each plugin actually has: poll questions and answers, ratings log
entries, download titles, draft names, whatever the plugin stores and renders.

The shape is the same everywhere and it asserts **both halves**:

* the payload's active form is **not** in the output — no `<script>` element, no
  `<img src=x onerror=…>`, no unescaped attribute break; and
* the payload's text **is** in the output, escaped — because escaping that
  dropped the value entirely would pass the first assertion while corrupting the
  data, and a poll answer that silently vanishes is its own bug.

The canonical payloads are a script tag (`<script>…</script>`), an attribute
breakout (`" onmouseover="…`) and an error-firing image (`<img src=x
onerror="…">`). Store them **unsanitised**, straight into the row — the row a
compromised or pre-fix install already has — because sanitising on the way in is
the assumption under test, not a step to reproduce.

Split the work by where the output lives. **A render path reachable from PHP is
tested in PHPUnit** — call the template tag, the shortcode, the list-table
column, the widget with a hostile stored value and assert on the returned
markup; it is faster and it pins the exact function. **A path that only exists
in a browser** — markup built in an AJAX response and swapped in, a value echoed
into a script or an attribute the DOM then acts on — is tested in the Playwright
suite (§7.5), where the assertion additionally checks that no sentinel the
payload would set ever became defined. Neither replaces the other: the AJAX
results path is invisible to PHPUnit, and the per-function pinning is invisible
to a browser.

### 7.3 Coverage

Target as close to 100 % on `includes/` as the plugin allows. Every public
method needs at least one test. Anything genuinely untestable (e.g. a
`phpinfo()` dump) is excluded with `@codeCoverageIgnore` and a one-line reason,
not left silently uncovered.

### 7.4 Config

`phpunit.xml.dist` and `phpunit-multisite.xml.dist` are copied verbatim from
`_standards/templates/` with only the testsuite `name` and the coverage `<file>`
entries changed. Test discovery is `<directory prefix="test-" suffix=".php">`,
so helpers need no `<exclude>` entries — this is what removes the 19 different
exclude lists.

### 7.5 End-to-end tests (Playwright)

PHPUnit calls the plugin's PHP. It cannot see a colour that came out wrong, a
vote that navigated instead of swapping in place, a script tag that a browser
executed, or a "Settings saved." notice that a scoped `settings_errors()`
filtered away. A plugin with a front end or an admin screen therefore also
carries a Playwright suite under `tests/e2e/`, and the ones already written
found bugs no unit test could — an unticked checkbox that could never be
unticked, a settings page with no success notice, a stored XSS.

**Scaffolding is copied, never invented.** `_standards/templates/` holds
`playwright.config.js` (reads `testsPort` from `.wp-env.json`, `workers: 1`,
retries CI-only), `bin/test-e2e.sh`, `tests/e2e/global-setup.js`, and
`tests/e2e/index.php`. `bin/test-e2e.sh` exists because **the tests wp-env
starts a plugin that is inactive and a site with no theme** — PHPUnit needs
neither, so wp-env provides neither, and a browser handed that site gets "not
allowed to access this page" on every screen and a blank front page. The script
activates the plugin by directory name and activates `twentytwentyone`, every
run, because running PHPUnit reinstalls that database underneath it. Do not
skip it and drive `npx playwright test` directly.

**The suite is CommonJS under Node**, not modules in a page: `eslint.config.mjs`
carries a block scoping `tests/e2e/**/*.js` and `playwright.config.js` to
`sourceType: 'commonjs'` with `globals.node` (§9, §8). `package.json` gains
`test:e2e` and the `@playwright/test` + `@wordpress/e2e-test-utils-playwright`
devDependencies; `.github/workflows/ci.yml` gains the `e2e:` job from the
template. A `tests/e2e/helpers.js` holds the fixture builders and shared
locators, so a spec reads as prose.

**Every test must fail with the plugin deactivated.** This is the one that
catches the tests that pass while asserting nothing. Prove it once per suite by
deactivating the plugin and running it: the count that survives is the count of
tests that were testing the harness. Two shapes leak through and are called out
below because they cost real time here.

* **A capability test must assert both directions.** "A subscriber sees no menu
  and cannot reach the screen" **passes with the plugin deactivated** — the
  menu and the screen are absent because the plugin is gone, not because the
  gate held. Pair it with "an administrator *can* see the menu and reach the
  screen", in the same test, so the pair can only pass when the plugin is
  present *and* gating. Both navigation suites shipped the one-sided version.
* **The login helper races a 200ms timer.** `wp-login.php` focuses and *selects*
  `#user_login` on a timer so a visitor can start typing. Fill across that
  moment and the password lands in the username box — Playwright focuses
  `#user_pass`, the timer takes focus back and selects it, and the typed text
  replaces the selection. `await expect( page.locator( '#user_login' )
  ).toBeFocused()` **before** filling waits for the timer's own effect; a
  `waitForTimeout` only makes the race less likely, which is the kind that fails
  on CI. Any suite that logs a second user in by hand needs this.

**Fixtures.** Data a person would type goes in through the screen that creates
it, so the screen is exercised by the tests that depend on it. Data a person
could not type — a question holding a `<script>`, a row shaped as an older
release wrote it — goes straight into storage. Custom tables have **no REST
route**, so those fixtures go through `npx wp-env run tests-cli wp eval`; posts
and comments go through `requestUtils`. Four rules the suites paid for:

* **Payloads travel base64-encoded, not inline.** A poll question of quotes,
  angle brackets and a script tag is exactly the string that arrives subtly
  altered through a shell argument, and a fixture that is not the payload byte
  for byte proves nothing about escaping it. Encode it, `base64_decode` it at
  the far end, and wrap what you read back in markers so wp-env's own progress
  chatter can be told from the output.
* **Create ordered fixtures sequentially, with explicit timestamps.** Comments
  or rows created in parallel land in the same second; the tie breaks on
  insertion order, which is whichever request the server reached first, and
  every assertion about "the first one" becomes a coin toss.
* **Restore anything global in `afterEach`** — templates, options, settings.
  A test that rewrites a poll template and does not put it back decides the
  outcome of the next test that reads one.
* **Each suite carries one "the fixture really is…" test** — that there is more
  than one page of results, that the poll is closed, whatever the rest leans on.
  Without it a broken fixture makes the whole file pass green while testing
  nothing.

**Assert on the far end, not on a notice.** A setting that saves but does
nothing and a setting that does something but will not save are the two failures
a screenshot cannot tell apart. Read the stored option back for the values the
logic consumes; read the *computed* style or rendered text for the ones a
visitor sees. "Settings saved." is worth asserting only as the specific
regression guard that the page did not scope `settings_errors()` to its own slug
and filter the core notice out.

**Native dialogs block everything after them.** A `confirm()` or `alert()` left
unhandled freezes the page and every later event. Register `page.on( 'dialog',
… )` and answer it — and for a delete or a max-choices guard, answer it **both
ways**: a dismissed confirm that deleted anyway is worse than no confirm, and
that is a test, not a nuisance to route around.

**Navigate by clicking.** Under the plain permalinks the tests env ships,
`/page/2/` is not a pagination URL. Reach the second page through the link the
plugin rendered, or through a `post.link` the REST helper handed back — never by
constructing a pretty URL by hand.

**Stored XSS is asserted twice over.** For every surface that renders
attacker-controlled text — the front end, the AJAX-returned results markup
(wp-polls' classic vector, built server-side and swapped in), the list table,
the log, the edit field — assert both that the sentinel the payload would set is
**undefined** *and* that the payload text is present **as text**. Escaping that
ate the payload entirely also passes the first assertion, and an answer that
silently vanishes is its own bug. The results markup is a separate test from the
ballot: a payload can be clean in the form and run in the response.

**Time fixtures use the site's clock, never this machine's.** A datetime built
from host-local parts and posted to a REST `date` field — which WordPress reads
as **site**-local — is wrong by the offset between the two, and `toISOString()`
is wrong by the whole timezone because it converts to UTC. On a UTC CI runner
host and site agree and the bug hides; on a developer machine at UTC+8 a post
"five minutes old" is stored eight hours in the future. Measure the skew rather
than assume it: publish a probe post, read back the date WordPress stamped, keep
the difference (`wp-relativedate`'s `siteNow()`). Anchoring day-scale fixtures at
**midday** buys twelve hours of slack and hides a day-scale skew; it does
nothing for a minute-scale one, and is not a substitute for measuring. When a
fixture's assertions are about *order* rather than an absolute date, a constant
offset cannot change the order, so `toISOString()` is harmless there — say so in
a comment, so the next reader does not copy it somewhere it bites.

### 7.6 Upgrade and migration tests

§2.1 and §13 govern *writing* a migration. This governs *proving* one does not
lose data — the question every major version has to answer for the sites that
have run the plugin for a decade. A plugin that owns custom tables or migrates
option rows on upgrade carries a `tests/test-migration-*.php` alongside the
option-level `test-migration.php`.

**Build the legacy shape from the released zip, not from the current install
code.** The whole point is to meet the tables a real site has, so transcribe the
`CREATE TABLE` statements from the version on wordpress.org (query the API for
the released version — the local SVN checkout is stale) into the test. If the
test copied `class-*-install.php` instead, it would assert that the code agrees
with itself. When the two disagree, this file must be the one still holding the
shape real sites carry.

**Two legacy shapes matter, and they test opposite things.** The near shape —
the last release, whose columns already match — proves the upgrade **touches
nothing**: snapshot all three tables before and `assertSame` after, row for row
and byte for byte, so an upgrade that "only" reset a vote count or re-encoded a
question fails. The ancient shape — the one the datatype conversions and index
changes in `activate()` actually exist for (a `varchar` id, a superseded index)
— proves the conversion **keeps every row**: those sites have been carried this
far, and a plugin that drops their data does it silently. Put quotes, an
ampersand and multibyte characters in the fixture; a migration that mangles
encoding passes every test written in ASCII.

**Both entry points, because they are not the same.** Reactivating runs the
activation hook; **updating through the plugins screen never fires it** and
leaves `admin_init` → `upgrade()` to run alone. Test each. And test
**idempotence**: users deactivate and reactivate to "fix" things, so a second
activation must be a bystander — same rows, same indexes.

**Present is not alive.** After the migration, cast a real vote (or the
plugin's equivalent write) against an id that came *through* the upgrade and
assert it lands in every table it should. Rows that survived the schema change
but no longer accept writes are a migration that passed and a plugin that
broke.

**DDL commits the transaction the test runner wraps each test in.** So a
migration test cannot lean on the automatic rollback: it must rebuild a clean
install in `tear_down()` **and then `COMMIT`**. Skip the commit and the parent's
rollback undoes the cleanup itself — and because the next test's own DDL makes
the leftovers durable, they leak into whichever file runs after this one. That
is not hypothetical; it cost a sibling file its expected value once already.

---

## 8. CI

`.github/workflows/ci.yml` is copied verbatim from `_standards/templates/`, with
`{{SLUG}}` substituted. Three jobs; the PHPUnit job has **six** rows — every supported stack in both modes, no special cases:

| WP | PHP | Mode |
|---|---|---|
| 6.8 | 8.2 | single |
| 6.8 | 8.2 | multisite |
| latest | 8.2 | single |
| latest | 8.2 | multisite |
| latest | 8.5 | single |
| latest | 8.5 | multisite |

Action versions, pinned identically everywhere:
`actions/checkout@v7`, `actions/setup-node@v7` (node 24),
`shivammathur/setup-php@v2` (PHP 8.2, `coverage: none`, `tools: cs2pr`).

Job names are exactly `PHP coding standards`, `JS coding standards and tests`,
and `PHPUnit (WP …, PHP …, …)`.

**A plugin with no JavaScript at all deletes the whole `eslint:` job**, from its
`eslint:` line through to the job that follows it. The template carries no
comment saying so — an instruction to the person copying the file has no
business shipping in nineteen committed workflows.

"No JavaScript" means no `js/` **and** no `tests/e2e/`. The Playwright specs are
JavaScript too, and a plugin whose only scripts are those still needs linting.
Reading the rule as "no `js/` directory" is how five repositories came to ship
e2e specs that nothing had ever linted — the first CI run after they landed
found style errors in a file that had been committed and pushed twice.

The same rule read the other way is how three plugins that ship no JavaScript at
all carried an `eslint:` job for months: it never ran a linter, because it died
at `actions/setup-node` looking for a lock file in a repository with no
`package.json`. A job that cannot pass is worse than no job; it teaches everyone
to ignore a red mark.

`npm run test:js --if-present` rather than `npm run test:js`, because a plugin
can have JavaScript worth linting and no vitest suite: a plugin whose only
scripts are Playwright specs has nothing for jsdom to load. `lint:js` is not
optional in the same way — anything lintable gets linted.

`wp-serverinfo` and `wp-sweep` keep their extra `claude.yml` /
`claude-code-review.yml`; those are not part of this standard.

---

## 9. Linting

* `phpcs.xml` is copied from `_standards/templates/phpcs.xml`, with `{{NAME}}`,
  `{{SLUG}}` substituted. **The `/tests/*` exclusions in the template are the
  only ones allowed.** Any additional `<rule>` or `phpcs:disable` in a plugin
  must be deleted and the underlying code fixed instead.
* **Fix the code first.** wp-stats reached zero suppressions by moving its whole
  query layer onto core APIs, and doing so found two real bugs; wp-postratings
  cut eleven files to eight the same way, by introducing one escaping chokepoint
  and dropping a global reassignment. Reach for a suppression only after the
  code-level answer has actually been tried and found worse.
* An inline `phpcs:ignore` is then permitted **only in `includes/`**, and **only
  with a `--` reason on the same line** saying why the sniff is wrong. A bare
  suppression is a failure; `verify.py` enforces the reason, not the absence.
* **A sniff that is wrong for the whole collection belongs in the shared
  `phpcs.xml`, not in nineteen inline ignores.** Two are there already:
  `NonceVerification` for `*-table.php` (core's sortable headers carry no nonce)
  and `DirectDatabaseQuery` for `includes/` (unanswerable for a plugin that owns
  a table). Add to that list rather than scattering.
* `PreparedSQL` is essentially never suppressed, because interpolation almost
  always has a real answer. Two of them:
  * **`%i` binds an identifier.** `prepare()` has supported it since WordPress
    6.2, which is below our floor, so
    `$wpdb->prepare( 'DROP TABLE IF EXISTS %i', $table )` replaces
    `"DROP TABLE IF EXISTS {$table}"`. That kills the commonest instance of this
    warning — the table-name interpolation in `uninstall.php`, install routines
    and test helpers. Seven plugins have it: wp-dbmanager, wp-downloadmanager,
    wp-draftsforfriends, wp-email, wp-postratings, wp-sweep, wp-useronline.
  * **A variable-length `IN ()` list** is built with
    `implode( ',', array_fill( 0, count( $ids ), '%d' ) )` and passed through
    `prepare()`, not interpolated.

  * **An optional scope binds rather than concatenates:**
    `( %d = 1 OR user_id = %d )` with `array( $show_all ? 1 : 0, $user_id )`
    replaces building the `WHERE` fragment conditionally. And a two-way
    `ORDER BY` is two literal statements chosen between, not one interpolated
    direction. wp-draftsforfriends removed four suppressions this way.

  What is genuinely left is an assembled clause — an allow-listed `ORDER BY`, an
  optional `WHERE` fragment — where each piece is one of:
  * a `prepare()` result;
  * a string from a class-local allow list;
  * **a documented raw-SQL argument of a public template tag that predates this
    work.** wp-downloadmanager's `download_embedded( $condition )` is one: every
    in-plugin caller builds it from `intval`'d ids and no request reaches it, but
    by contract it is theme-author SQL. Suppress it and note that the tag is
    itself the thing to remove in a future major, rather than pretending the
    fragment is safe by construction.

  The reason must name which of the three it is. Anything else is a bug, not a
  false positive.

  One mechanical detail: a bare `phpcs:ignore` on its own line covers only the
  **next** line, and trailing on a code line covers only **that** line. A
  multi-line `$wpdb->prepare()` that needs both `InterpolatedNotPrepared` (on the
  SQL string) and `ReplacementsWrongNumber` (on the `prepare(` line) therefore
  cannot be covered by one `phpcs:ignore` — use a `phpcs:disable` /
  `phpcs:enable` pair, as wp-postratings does.
* `uninstall.php` is **not** covered by the shared `DirectDatabaseQuery`
  exclusion, which is scoped to `/includes/*` — and `verify.py` rejects any
  suppression outside `includes/`, so an inline ignore there is not an option.
  **Delegate instead:** the drop lives in `WP_{{...}}_Install::drop_table()` and
  `uninstall.php` calls it, which puts the schema change inside `includes/`
  where the exclusion applies and needs no suppression at all.
  wp-draftsforfriends, wp-email and wp-downloadmanager all do this. Note the
  helper must fall back to `$wpdb->prefix . '<table>'`, because uninstall runs
  with the plugin inactive and `$wpdb-><table>` unregistered.
* The one genuine false positive found so far — `NonceVerification` firing on a
  `WP_List_Table` reading `$_GET['orderby']` — is handled by a **scoped
  exclusion in the shared `phpcs.xml`**, not by nineteen inline ignores. If you
  find another sniff that is genuinely wrong for every plugin, it belongs in the
  template the same way, so the answer stays identical across the collection.
* `eslint.config.mjs` is copied from the template, with the single localised
  global name substituted. `npm run lint:js` must pass clean.
* Both must pass with **no** warnings, not just no errors.

---

## 10. wp-env

`.wp-env.json`, committed, identical apart from the two ports:

```json
{
	"$schema": "https://schemas.wp.org/trunk/wp-env.json",
	"core": null,
	"plugins": [ "." ],
	"phpVersion": "8.2",
	"port": <PORT>,
	"testsPort": <PORT+1>,
	"config": {
		"WP_DEBUG": true,
		"WP_DEBUG_DISPLAY": true,
		"SCRIPT_DEBUG": true
	},
	"env": {
		"tests": {
			"config": {
				"WP_DEBUG": true
			}
		}
	}
}
```

`.wp-env.override.json` is **deleted and gitignored** in every repo. It is a
local-and-CI override mechanism; committing it is what caused the port
collisions. CI writes its own when it needs one.

Ports, assigned in slug-alphabetical order, two apart so `port` and `testsPort`
can never collide. `8888`/`8889` are reserved for the all-plugins environment at
the root of this folder.

| # | Plugin | port | testsPort |
|---|---|---|---|
| 1 | freemyinternet | 8890 | 8891 |
| 2 | wp-ban | 8892 | 8893 |
| 3 | wp-commentnavi | 8894 | 8895 |
| 4 | wp-dbmanager | 8896 | 8897 |
| 5 | wp-downloadmanager | 8898 | 8899 |
| 6 | wp-draftsforfriends | 8900 | 8901 |
| 7 | wp-email | 8902 | 8903 |
| 8 | wp-pagenavi | 8904 | 8905 |
| 9 | wp-pluginsused | 8906 | 8907 |
| 10 | wp-polls | 8908 | 8909 |
| 11 | wp-postratings | 8910 | 8911 |
| 12 | wp-postviews | 8912 | 8913 |
| 13 | wp-print | 8914 | 8915 |
| 14 | wp-relativedate | 8916 | 8917 |
| 15 | wp-serverinfo | 8918 | 8919 |
| 16 | wp-showhide | 8920 | 8921 |
| 17 | wp-stats | 8922 | 8923 |
| 18 | wp-sweep | 8924 | 8925 |
| 19 | wp-useronline | 8926 | 8927 |

---

## 11. Images

Ship no raster images. Replace with inline SVG (an `<svg>` printed by PHP, or a
CSS `mask-image` with a data URI) or a CSS-only construction.

| Plugin | File | Replacement |
|---|---|---|
| wp-polls | `images/loading.gif` | CSS-only spinner, `prefers-reduced-motion` aware |
| wp-print | `images/print.gif`, `images/printer_famfamfam.gif` | inline SVG printer glyph |
| wp-email | `images/loading.gif` | same CSS spinner as wp-polls |
| wp-email | `images/email.gif`, `images/email_famfamfam.png` | inline SVG envelope glyph |
| wp-downloadmanager | `images/drive.png`, `images/drive_go.gif` | inline SVG |
| wp-downloadmanager | `images/ext/*.gif` (34 files) | one inline SVG sprite with a `<symbol>` per extension family, referenced by `<use>`; unknown extensions fall back to a generic document symbol |

Delete `images/` entirely once empty. Emoji are **not** acceptable — they render
differently per platform and cannot inherit `currentColor`.

---

## 12. Composer / npm

`composer.json`: same shape as `wp-ban/composer.json` — `name`
`lesterchan/{{SLUG}}`, `type` `wordpress-plugin`, `homepage`
`https://wordpress.org/plugins/{{SLUG}}/`, `license` `GPL-2.0-or-later`, author
Lester Chan, `require` `php >=8.2`, `require-dev` `phpunit/phpunit ^9.6` +
`yoast/phpunit-polyfills ^2.0`, `scripts.test` `phpunit`,
`config.allow-plugins` `false`. `description` matches the plugin header
`Description:` exactly.

`composer.lock` is committed. `vendor/` is not.

`package.json`: same shape as `wp-ban/package.json`. Scripts are exactly
`lint:js`, `lint:js:fix`, `test`, `test:js`, `test:js:watch`. Same devDependency
versions across all plugins.

---

## 13. WP-Stats integration — the one cross-plugin contract

Seven plugins currently read the bare `stats_display` row, and five read
`stats_mostlimit`: wp-downloadmanager, wp-email, wp-polls, wp-postratings,
wp-postviews, wp-stats and wp-useronline. These are unprefixed, shared, legacy
`wp_options` rows — exactly what §2.1 forbids, and the one place where changing
a plugin in isolation breaks a sibling.

The contract, applied identically by every plugin involved:

* The values move **into each plugin's own** `{{UNDER}}_options` array, under the
  keys `stats_display` (bool) and `stats_most_limit` (int). The shared
  `stats_display` and `stats_mostlimit` rows are deleted by each plugin's
  migration.
* wp-stats **never reads a sibling's option row.** It collects sections by
  firing one filter:

  ```php
  $sections = apply_filters( 'wp_stats_sections', array() );
  ```

  Each contributing plugin's `WP_{{...}}_WPStats` class hooks that filter and
  returns its own entry, honouring its own `stats_display` setting. It is
  therefore impossible for wp-stats to render a section for a plugin that is
  not installed, which the shared-option approach never guaranteed.
* A contributing plugin renders its section through
  `wp_stats_section_{{UNDER}}`, so a theme can override one plugin's block
  without touching the others.
* `WP_{{...}}_WPStats` is loaded unconditionally; it is inert if wp-stats is
  absent. No `class_exists`/`function_exists` probing between plugins.

wp-stats owns `wp_stats_sections` and must define it before the other six are
finished. It is written into this document so all seven agents implement the
same two hook names without needing to coordinate.

### 13.1 The exact shape — do not improvise

Seven plugins implement this in seven separate sessions, so the array shape is
pinned here rather than discovered. A contributor returns **one entry keyed by
its own `{{UNDER}}`**:

```php
add_filter( 'wp_stats_sections', array( $this, 'register_section' ) );

/**
 * @param array $sections Sections keyed by plugin slug with underscores.
 * @return array
 */
public function register_section( $sections ) {
	$options = get_option( WP_Polls_Options::OPTION, array() );

	if ( empty( $options['stats_display'] ) ) {
		return $sections;   // opted out; contribute nothing
	}

	$sections['wp_polls'] = array(
		'title'    => __( 'Polls', 'wp-polls' ),
		'priority' => 10,
		'render'   => array( $this, 'render' ),
	);

	return $sections;
}
```

| Key | Type | Meaning |
|---|---|---|
| `title` | string | Translated heading. Required. |
| `priority` | int | Sort order, ascending, ties broken by `strcmp()` on the key. **Optional — a missing or non-numeric value becomes 10** rather than invalidating the entry. Send it explicitly anyway. |
| `render` | callable | Echoes the section body. Required. Takes no arguments. |

wp-stats sorts by `priority`, then for each entry echoes the title and calls
`render` inside `wp_stats_section_{key}`:

```php
$sections = apply_filters( 'wp_stats_sections', array() );
uksort( $sections, /* by priority, ties by key */ );

foreach ( $sections as $key => $section ) {
	do_action( 'wp_stats_section_' . $key, $section );
}
```

### 13.2 The shared-row deletion hazard — read this before writing the migration

§2.1 requires each migration to delete the rows it folds in, and the shared
`stats_display` / `stats_mostlimit` rows are read by **seven** plugins. So
whichever plugin a site upgrades **first** deletes them, and the other six then
find nothing to migrate.

Left alone this silently turns blocks off: a site that updates wp-stats before
wp-polls loses the polls block, with no error anywhere.

**The rule, in all seven plugins:** when the shared row is absent, `stats_display`
defaults to **on**.

```php
$legacy = get_option( 'stats_display', null );

if ( null === $legacy ) {
	$display = true;              // a sibling already migrated and deleted it
} elseif ( ! is_array( $legacy ) ) {
	$display = (bool) $legacy;
} elseif ( array_key_exists( '{{THIS}}', $legacy ) ) {
	$display = (bool) $legacy['{{THIS}}'];   // e.g. 'polls', 'useronline'
} else {
	$display = in_array( '{{THIS}}', $legacy, true );
}
```

**The row is an array keyed per plugin**, not a bare boolean — a site chose
which blocks to show. A plain `(bool) $legacy` casts any non-empty array to
`true`, so a block the owner had deliberately switched off comes back on. Both
array shapes are in the wild: `array( 'polls' => 1 )` and `array( 'polls' )`.
Store the result as a **bool**.

Never `get_option( 'stats_display', false )` and never `! empty()` on the raw
read — both read a deleted row as a deliberate opt-out.

**Read it through your own options reader, not `get_option()` directly.** The
snippet above is the migration's view. Everywhere else, go through
`WP_{{...}}_Options::get( 'stats_display' )` so the shipped default applies:
there are two ways the shared row can be missing — a sibling deleted it, or this
is a fresh install that never had one — and only the options reader knows the
plugin's own default. Reading the raw row makes a brand-new install look opted
out. The worst case under the
correct rule is a block a site owner has to switch off again; under the wrong
one it is a block that vanishes with no explanation.

Each plugin's Upgrade Notice says to update all seven together, and where to
switch a block back on.

**And the mirror of the rule: `uninstall.php` must NOT delete the shared rows.**
The migration deletes them because it has folded them in; uninstall must leave
them alone, because up to six siblings that have not upgraded are still reading
them. Deleting `stats_display` while removing one plugin would silently
reconfigure the others. Exclude the shared rows from the uninstaller's option
list and assert it with a test.

Rules that keep the seven implementations honest:

* A contributor **reads only its own option row** to decide whether to
  contribute. wp-stats reads none of them.
* A contributor that is opted out returns `$sections` untouched — it does not
  add an entry with an empty body.
* `render` echoes; it does not return markup.
* wp-stats must tolerate a malformed entry by skipping it, never fatalling — a
  sibling is third-party code as far as it is concerned. Skip when: the key is
  not a non-empty string, the entry is not an array, `title` is missing, empty
  or not a string, or `render` is not `is_callable()`. A non-array filter return
  yields no sections.
* **wp-stats echoes the heading, not the contributor.** Its own listener sits on
  `wp_stats_section_{key}` at priority 10, echoes the title, then calls `render`.
  A contributor supplies `title` and `render` and hooks nothing else. A theme
  overrides one block by hooking the same action earlier and removing that
  listener — which is the whole reason the action exists.
* **`render` echoes, it does not return.** wp-stats assembles the page with
  `ob_start()` for the shortcode, so a returned string is silently dropped.
* A contributor namespaces its copy of the foreign setting as `stats_display` /
  `stats_most_limit` inside its own options row. wp-stats, being the owner,
  calls its own `most_limit` without the redundant prefix.

---

## 13.3 WP-CLI and REST naming — the phase-2 reference

Not yet rolled out, but wp-sweep has set it and the rest of the collection
copies it when that phase starts:

* **WP-CLI command name is the plugin slug**: `wp wp-sweep`, registered as
  `WP_CLI::add_command( WP_SWEEP_SLUG, … )`.
* **REST namespace is `{{SLUG}}/v1`**: `wp-sweep/v1`.

Both were previously bare nouns — `wp sweep`, `sweep/v1` — that any plugin
could have claimed, and neither WordPress nor WP-CLI detects the collision.

---

## 14. Versions and the release baseline

Queried from `plugins.svn.wordpress.org` — the local `~/svn/wordpress_plugins`
checkouts are stale (2022-era) and must not be used as the baseline.

| Plugin | Released on .org | Ships as | Note |
|---|---|---|---|
| freemyinternet | *trunk* (0.01) | 1.0.0 | |
| wp-ban | 1.69.2 | 2.0.0 | |
| wp-commentnavi | *trunk* (tag 1.10) | 2.0.0 | |
| wp-dbmanager | **3.0.0** | **4.0.0** | 3.0.0 is already live — do not reuse it |
| wp-downloadmanager | 1.69.2 | 2.0.0 | |
| wp-draftsforfriends | *trunk* (1.0.2) | 2.0.0 | Upgrade Notice is written against 1.0.2 |
| wp-email | 2.69.4 | 3.0.0 | |
| wp-pagenavi | 2.94.6 | 3.0.0 | |
| wp-pluginsused | *trunk* (tag 1.50) | 2.0.0 | |
| wp-polls | 2.77.3 | 3.0.0 | |
| wp-postratings | 1.91.3 | 2.0.0 | |
| wp-postviews | 1.78.1 | 2.0.0 | |
| wp-print | 2.58.3 | 3.0.0 | |
| wp-relativedate | 1.51.1 | 2.0.0 | |
| wp-serverinfo | 2.0.0 | 3.0.0 | |
| wp-showhide | 2.0.0 | 3.0.0 | |
| wp-stats | 2.56.1 | 3.0.0 | |
| wp-sweep | 1.2.0 | 2.0.0 | |
| wp-useronline | **3.0.0** | **4.0.0** | see below |

Two plugins need their version changed from what is currently in the repo:

* **wp-dbmanager 3.0.0 → 4.0.0.** 3.0.0 is already on wordpress.org, so the
  repo's unreleased entry collides with shipped history. Rename the changelog
  heading, the plugin header `Version:`, the README `Stable tag:` and
  `WP_DBMANAGER_VERSION` to 4.0.0.
* **wp-useronline 3.0.1 → 4.0.0.** 3.0.0 shipped a changelog entry promising
  *"Template tags, the `[page_useronline]` shortcode and all four filters are
  unchanged."* This release renames all four filters and
  `USERONLINE_TRUST_PROXY`, which a patch number cannot carry. Merge the 3.0.1
  entry into a 4.0.0 entry, and make the Upgrade Notice state plainly that the
  filters promised stable in 3.0.0 have been renamed, listing all five
  old → new pairs.

Four plugins currently have `Stable tag: trunk` on wordpress.org
(freemyinternet, wp-commentnavi, wp-draftsforfriends, wp-pluginsused). Their
README `Stable tag:` must be the real version per §3.2, and at release time the
SVN tag must be created rather than left pointing at trunk.

### 14.1 Upgrade Notice must cover the whole SVN → major gap

`## Upgrade Notice` is written against the **released** version in the table
above, not against the previous git commit. Everything a site owner updating
from that released version would notice must appear there:

* renamed or removed hooks, with old → new pairs
* renamed option rows (only where the *released* version's name changes)
* settings screens that moved URL
* global functions and classes that no longer exist
* capability changes
* renamed constants
* changed defaults or changed storage formats
* **the raised floors** — every plugin now requires WordPress 6.8 and PHP 8.2.
  This is the break most likely to actually bite: a site on an older stack
  simply will not receive the update. Every plugin's Upgrade Notice must say so
  plainly, as its own `BREAKING:` changelog line too.

  **Do not say what the reader is upgrading *from*.** "up from 6.0 and 7.4" was
  written into fourteen plugins and is wrong in nearly all of them: the released
  readmes declare WordPress 2.8 to 5.5, and **fifteen of the nineteen declare no
  `Requires PHP` at all**. Three plugins ended up asserting three different
  predecessors, none of them right. Equally, "if your host still runs PHP 7.4"
  tells a reader who may be on 5.6 that they are on 7.4.

  State the requirement, the consequence and the check — all true regardless of
  where the reader is coming from:

  > **Your site must be on WordPress 6.8 or later and PHP 8.2 or later.** A site
  > on anything older is simply not offered the update, so if <NAME> has stopped
  > appearing in your updates list, that is why. Check
  > `WP-Admin -> Tools -> Site Health -> Info -> Server` for your PHP version; if
  > it is below 8.2, ask your host to move you up. PHP 8.1 and everything before
  > it stopped receiving security fixes.

Write it for a site owner, not a developer: what breaks, and what to do.

---

## 15. Order of work, per plugin

1. Layout: move files, add `index.php`, delete `.idea`, `.wp-env.override.json`.
2. Copy the shared config files from `_standards/templates/`.
3. Rename classes and files (§2.4), then constants (§2.3), then class constants
    (§2.2) — except `GROUP`, whose value is the settings row name and so has to
    wait for step 4.
4. Rename option rows and retarget the existing migration (§2.1).
5. Rename hooks (§2.6) and record every one under `## Upgrade Notice`.
6. Rewrite admin screens onto the Settings API + `WP_List_Table` (§4).
7. Drop jQuery, move JS to `js/`, add `tests/js/` (§6).
8. Replace images with SVG/CSS (§11).
9. Normalise styles (§5).
10. README: header line breaks, canonical sections, Upgrade Notice (§3).
11. Tests: rename to convention, add the fourteen shared tests, push coverage
    up (§7).
12. Run `phpcs`, `eslint`, `bash bin/test.sh`, `bash bin/test-multisite.sh`,
    `npm run test:js`. All must pass clean.
    A step that is genuinely N/A for your plugin — no hooks to rename, no
    admin screen, no JS, no images — produces **no commit**. Do not create an
    empty one. Say which steps you skipped and why in the final commit message,
    so the gap in the `Step N:` sequence is explained rather than suspicious.

13. **Commit after every numbered step above, not once at the end.**

    This is not tidiness — it is the difference between an interrupted plugin
    being resumable and being garbage. A session that dies mid-step leaves a
    clean tree at a known checkpoint instead of seventy half-applied files that
    look fine to `phpcs` and are silently broken. It has already cost one full
    fan-out.

    Prefix each message with the step it completes, so `git log` *is* the
    progress tracker and the next session can see exactly where to pick up:

    ```sh
    git commit --no-gpg-sign -m "Step 4: move options to wp_polls_options"
    ```

    Leave the tree clean and the plugin loadable at every commit. If a step is
    too big to finish in one go, commit the coherent part of it and say so in
    the message.

    **Do not push. Do not tag. Do not touch SVN.**

    Global git config sets `commit.gpgsign = true`, but the existing history in
    these repos is unsigned and stays that way. `--no-gpg-sign` is required
    explicitly on every commit; do not change the global config, and do not
    amend earlier commits to add signatures.
