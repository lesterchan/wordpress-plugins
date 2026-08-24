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
│       ├── ci.yml
│       ├── claude-code-review.yml
│       └── claude.yml
├── .editorconfig
├── .gitignore
├── .wp-env.json
├── bin/
│   ├── build                 # only the plugins with src/ (§13.4); makes build/
│   ├── index.php
│   ├── test.sh
│   ├── test-e2e.sh
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
│   ├── {{SLUG}}-admin.js     # wp-admin
│   └── {{SLUG}}-<thing>.js   # a further script earns a purpose suffix
├── src/                      # only the plugins with blocks (§13.4); committed,
│                             # never shipped -- bin/build compiles it to build/,
│                             # which is gitignored and ships
├── tests/
│   ├── index.php
│   ├── bootstrap.php
│   ├── helper-*.php          # every non-test file in tests/ is helper-*.php
│   ├── e2e/                  # the Playwright suite (§7.5)
│   │   ├── index.php
│   │   ├── helpers.js        # single-spec suites may inline it
│   │   ├── mu-plugins/       # only where the suite needs one (§7.5)
│   │   └── *.spec.js
│   ├── js/                   # only if the plugin has JS
│   │   ├── index.php
│   │   ├── helpers.js        # loads the shipped script into jsdom
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
├── playwright.config.js
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
* `uninstall.php` exists in **every** plugin, even where it only deletes a
  single option row. `wp-relativedate` and `wp-showhide` had none when this was
  written; both do now.
* `.wp-env.override.json` is **deleted** from every repo and gitignored. Ports
  live in the committed `.wp-env.json`; the override file is for local/CI use
  only and must never be tracked.
* `.idea/` is deleted from the working tree and gitignored.
* **The list above is what the repo *tracks*, not what the plugin *ships*.**
  The SVN deploy excludes everything development-only — `.github/`, `bin/`,
  `tests/`, `src/`, the configs — and ships `build/` in its place for the
  block plugins. Do not delete `CLAUDE.md` or `.claude/` either; they are
  development tooling outside this standard, and the two `claude*.yml`
  workflows (§8) are in the tree because every repo carries them. Same for `htaccess.txt` and
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

The renames, all shipped in the 2026-08 majors. The table stays because the
migrations implementing it are live code: every site upgrading from a
pre-revamp version still crosses them, and the old names are what those
migrations read.

For most plugins the new name first existed in the 2026-08 major, so the rename
retargeted a migration that already existed. wp-commentnavi, wp-dbmanager and
wp-pluginsused stored under a name their pre-revamp release shipped, so for
them the rename was user-facing and their migration was their first
(wp-pluginsused's last release stored nothing at all):

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

Every plugin **that stores a row** defines `OPTION` and `VERSION`. The four
§2.1 plugins that store nothing at all — wp-relativedate, wp-serverinfo,
wp-showhide and wp-sweep — define neither, and that is not an omission: a
constant naming a row the plugin never writes is a promise it does not keep.

`PAGE` and `CAPABILITY` are defined **only where the plugin has an admin
screen** — wp-relativedate and wp-showhide have none. `GROUP` follows a
**settings** screen specifically, which is not the same test: wp-serverinfo and
wp-sweep both have admin screens and correctly define no `GROUP`, because
neither calls `register_setting()`.

`PAGE` lives on `Admin` where the plugin has one screen, and `Settings` reaches
across to `WP_{{...}}_Admin::PAGE` when registering its sections.

These need not all live on one class, and a plugin with a data screen *and* a
settings screen needs two page slugs: `WP_Stats_Admin::PAGE = 'wp-stats'` for
the menu, `WP_Stats_Settings::PAGE = 'wp-stats-settings'` for the settings page.
`CAPABILITY` belongs on whichever class owns the screen it gates, read through
the `{{UNDER}}_capability` filter (§2.7) — a plugin may define it twice, as
wp-email does (`manage_email` for the Logs screen, `manage_options` for
settings) and wp-draftsforfriends does (`manage_options` and `publish_posts`),
provided both go through the one filter. **This used to cite wp-sweep, which
cannot illustrate it:** wp-sweep has no settings screen at all — §4.1 says so —
and defines `CAPABILITY` once. That example outlived the code it described, in
the section next door to the one warning about exactly that. Constants the list does not
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

Global functions live in four places and nowhere else:

* `includes/template-tags.php` — the documented public API. Template tags keep
  the names they shipped with in the last SVN release and must not be renamed,
  which is why they alone are exempt from the prefix rule below.
* `includes/deprecated.php` — the same, for names being retired.
* `uninstall.php` — the per-site work is callable rather than living only in
  the file body, because §7.2.1 depends on re-running it without including the
  file twice. Two shapes satisfy that and no third does: a declared
  `{{UNDER}}_uninstall_site()` the file's own network loop calls, or a file
  that only dispatches to the `Install` component, whose methods are just as
  reachable — the shape wp-polls, wp-postratings and wp-useronline carry
  because their row lists and table drops live beside their installers. `_uninstall_site` is
  the verb the loop calls; a `_delete_options` spelling was the loop's verb in
  three plugins and survives only as a sub-helper the verb calls in two.
* the main plugin file — activation and deactivation callbacks that have to be
  registered while it loads.

Everything else is a class method.

**Any global function outside `template-tags.php` is prefixed `{{UNDER}}_`, and
that is the half that is enforced.** This section used to name only the first
two files, which was false in all nineteen plugins on the day it was written —
every `uninstall.php` has always declared one. The rule nothing checked was the
rule everything broke.

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

**Exactly four plugins invent a capability**, and the distinction matters more
than the count: a capability is custom when the plugin has to *create* it with
`add_cap()`. Those four are `wp-downloadmanager` (`manage_downloads`),
`wp-email` (`manage_email`), `wp-polls` (`manage_polls`) and `wp-postratings`
(`manage_ratings`). `wp-dbmanager` (`install_plugins`), `wp-sweep`
(`activate_plugins`) and `wp-draftsforfriends` (`publish_posts`) gate on **core**
capabilities, which every administrator already holds and which are nobody's to
grant or revoke.

**The capability a plugin grants must be the capability it checks.** Screens gate
on the filtered value, so `add_cap()` and `remove_cap()` take
`capability()` — never the `CAPABILITY` constant and never its literal string. A
site that filters the capability would otherwise be handed one nothing looks at
while every screen is gated on one nobody holds: locked out of its own plugin
with nothing in any log to say why. Three of the four had this on 2026-08-04;
`verify.py` checks it now. A literal naming a **retired** capability is still
legal, because there is no accessor for one that no longer exists —
wp-dbmanager's `remove_cap( 'manage_database' )` is the case.

**Settings normally stays on `manage_options`, and there are argued
exceptions.** The rule is that the custom capability gates the plugin's **data**
screens. Where a plugin's settings are themselves at least as sensitive as its
data, the settings screen may take the same or a higher capability, and **the
reason goes in a docblock at the gate**. wp-dbmanager is why this is not
absolute: its settings screen sets the `mysqldump` and `mysql` binary paths, so
whoever can write them can make the plugin execute an arbitrary binary as the
web user. That screen is *more* dangerous than its data screens, and
`install_plugins` is correct. wp-polls and wp-postratings gate settings on their
own capability because those settings govern exactly the data it covers.

What is **not** permitted is a third capability belonging to neither set: the
settings screen takes `manage_options` or the plugin's own, and nothing else.

### 2.7.1 Differences that are load-bearing — do not converge these

A consistency pass will keep rediscovering these and proposing to unify them.
Each is deliberate; the reason is the entry:

* **Widget `id_base` strings are frozen** (`polls-widget`, `downloads`,
  `views`, …). They are stored inside every site's widget instances; renaming
  one orphans the widget on every site that placed it.
* **Front-end AJAX action names `polls` and `email` are frozen.** Pages cached
  with the old script keep posting to the old action for as long as the cache
  lives; renaming breaks voting and sending on every such page mid-rollout.
  wp-postratings paid that price knowingly in its major; a patch release must
  not. Handler *method* names converge; the action strings do not.
* **The asset-gate mechanism follows what the page can know.** Two passes
  (head scan + render flag, wp-polls and wp-postratings) only where markup can
  appear later than the head *and* a stylesheet needs the head; flag-only
  where there is no stylesheet (wp-useronline); scan-only where nothing
  renders late (wp-stats); unconditional where the output is on effectively
  every page (wp-email). The gate name states what it gates: `needs_assets`
  (both), `needs_styles` (CSS), `needs_script` (JS).
* **`capability()` lives beside the admin-page registration**, and its
  `$context` default names the plugin's primary surface — which is why the
  defaults differ. wp-ban and wp-stats take no default because no surface of
  theirs is privileged; wp-serverinfo's `NETWORK_CAPABILITY` branch is the
  §7.2.2 rule expressed in code.
* **The Options API family follows the option's shape**: flat rows speak
  `get`/`update`/`write`/`migrate`; the nested-array plugins speak
  `all`/`set`/`save`/`flush`. Where an Install class exists it owns activation
  and upgrade; otherwise Options does.
* **wp-email ships no theme-override stylesheet lookup** — removed on purpose,
  with the reason in the enqueue docblock. wp-showhide's stylesheet is
  unconditional for the FOUC reason its comment gives.

### 2.7.2 One name per job — the method-name canon

The 2026-08 consistency campaign found the same feature under different names
across the nineteen and converged them. These are now the names; a new plugin
takes them, and a rename away from them is drift:

* **Options**: `defaults()`, `get()`, `update()`, `sanitize( $input )`,
  `maybe_upgrade()`, `migrate()` / `migrate_legacy_rows()`, `write()`,
  `markers()`, `update_markers()` (no arguments — it stamps the constants),
  `flush()`. Constants: `OPTION`, `VERSION`, `LEGACY_OPTION`.
* **Activation**: the entry point is `activate( $network_wide = false )`; the
  per-site work is `install()`. The hook is registered from the bootstrap
  class, pointing at the Install class where one exists.
* **The upgrade runs on `init` at priority 5** — never `admin_init` or
  `plugins_loaded`. Activation does not fire on a plugin update, and an
  automatic background update runs on cron, which never reaches an admin
  hook; an `admin_init` migration leaves such a site serving its front end
  unmigrated until somebody logs in. A direct unconditional call from the
  bootstrap is the one acceptable alternative (it runs even earlier). A
  consequence the e2e suites carry: WP-CLI boots fire `init` too, so a
  fixture that seeds legacy rows must seed and read back in one `wp eval`
  call, or the migration has already eaten them.
* **Admin**: the `admin_menu` callback is `add_page()`; the Settings API
  registration is `register()`; the `admin_enqueue_scripts` callback is
  `enqueue()` — never named after its hook. Every plugin with an admin page
  carries `action_links()` on the `plugin_action_links_` filter, linking its
  first screen.
* **Front end**: the asset pair is `scripts()` / `styles()`; a CSS-only
  callback is `enqueue_styles()`. Handles are the literal `'wp-slug'` string,
  never the SLUG constant. Asset URLs use the `{{UPPER}}_URL` constant, never
  `plugins_url()`. The theme-override stylesheet lookup, where a plugin keeps
  one, is child theme → parent theme → plugin.
* **Widgets**: wired by a bootstrap `register_widget()` method on
  `widgets_init`; constructors pass the options array inline and translate
  with `__()`.
* **AJAX**: handler methods are `ajax_*`; the registered action strings are
  frozen per §2.7.1. Nonce constants are `NONCE_ACTION` / `NONCE_FIELD`.
* **WP-CLI**: `register_command()` in the shape all nine copies share —
  negative guard, `require_once` of the command file, `add_command`.
* **WPStats bridges**: static `init()`; the most-listing limit helper is
  `most_limit()`.
* **Singletons**: `private function __construct()`; the `get_instance()`
  summary reads "Get the instance, creating it on first call." Component
  `init()` docblocks read "Hook registration."
* **The recurring sentences are verbatim**, because seven phrasings of one
  sentence is how drift was discovered in the first place:
  * `// 'number' => 0 lifts WP_Site_Query's default cap of 100, which would otherwise skip every site past the hundredth while reporting success.`
  * `// Inside the loop: switch_to_blog() pushes onto a stack, so restoring once after the loop unwinds it by exactly one.`
  * `// Must be registered at file-load time, which is when this runs.`
  * docblock line: `Activation does not fire on a plugin update, which is the single most common reason a migration never runs.`
  * `@param bool $network_wide Whether the plugin is being activated network-wide.`

Where any of this collides with a frozen public surface — template-tag names,
hook names, shortcodes, option rows, widget ids, the two legacy AJAX actions —
§2.7.1 wins and the frozen name stays.

### 2.8 Comments — concise, and as few as possible

A comment earns its place by stating a constraint the code cannot show — why,
never what. One or two sentences; not an essay. The history of a decision, what
the code replaced and how it once went wrong belong in the commit message, the
changelog or `_standards/`, not above the code. Docblocks are the one-line
summary plus the tags WPCS requires. (Lester's call, 2026-08-10; earlier code
predates it and is trimmed as it is touched, not in a sweep.)

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

The GPL comment block that follows is the **"or later" variant**, and it is
reproduced here **in full and verbatim** — tabs for indentation, two spaces
after the year, around `email :`, and either side of the postal code:

```
/*
	Copyright 2026  Lester Chan  (email : lesterchan@gmail.com)

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/
```

`bin/verify.py` compares this byte for byte, and the year lives in one constant
there so that rolling it over is one edit rather than nineteen.

**The tail used to be elided with a `…`, and that is how the address drifted.**
Sixteen plugins carried `59 Temple Place, Suite 330, Boston, MA  02111-1307` —
the address the FSF left in **2005**, which survives across most of the
WordPress plugin directory purely by copy-and-paste — and three carried
`51 Franklin St`, the right building with the street name abbreviated. Neither
group matched what the FSF publishes with GPL-2.0 today.

Of the two ways to make nineteen files agree, only one of them is also true:
this is a postal address the block instructs a reader to write to. **A rule
this document elides is a rule nothing enforces**, which is the same lesson §9
and §4.1 each learned separately.

**This must be the "or later" form.** A v2-**only** block (`under the terms of
the GNU General Public License, version 2, as published by the Free Software
Foundation`, with no "or at your option any later version") contradicts the
`License: GPLv2 or later` header two lines above it and the `GPL-2.0-or-later`
in composer.json, so a plugin carrying one ships a self-contradicting licence
statement. Five did; the last of them, freemyinternet, was corrected on
2026-08-02, and `verify.py` now checks for the "or later" clauses by name as
well as comparing the whole block, so the failure says which of the two is
wrong.

### 3.2 `README.md` header

Nine lines, lines 2–9 ending in **two spaces**, line 10 with none:

```
# {{NAME}}
Contributors: GamerZ␣␣
Donate link: https://lesterchan.net/site/donation/␣␣
Tags: <five tags, comma separated>␣␣
Requires at least: 6.8␣␣
Tested up to: 7.1␣␣
Stable tag: 3.0.0␣␣
Requires PHP: 8.2␣␣
License: GPLv2 or later␣␣
License URI: https://www.gnu.org/licenses/gpl-2.0.html
```

Nine fields after the `#` heading. Exactly **five** tags.

`Contributors:` is **`GamerZ` and nothing else**, in every plugin without
exception. wp-pagenavi read `GamerZ, scribu` when this was written; the second
name is gone.

### 3.3 `README.md` body

**Level-2** headings, in this order, and no other `##` heading. Level-3
headings are free — `## Changelog` necessarily contains `### 2.0.0`, and
`### Features` below is an h3. The closed set is the h2s:

```
## Description
### Features            (optional, only if the plugin has a bullet list)
## Installation         (every plugin, even the ones with nothing to do)
## Usage                (h2, never "General Usage")
## Frequently Asked Questions
## Screenshots
## Changelog
## Upgrade Notice
```

**`## Installation` is required of all nineteen** — Lester's call, 2026-08-08,
overruling a proposal to give it only to the four plugins with a real first-run
step. The reasoning is that wordpress.org renders it as its own tab, so a tab
present on some of these plugins and missing on others reads to a user as an
omission rather than as a decision. It sits between Description and Usage
because that is the order a reader works in: install, then use.

**It is not boilerplate, and must not become boilerplate.** "Upload to
`wp-content/plugins/`" is advice from before WordPress had a plugin installer
and is not to be reintroduced. Step one is *install and activate*; everything
after it is specific to the plugin. Where a plugin genuinely needs nothing, say
so plainly and say what happens instead — wp-relativedate's whole section is
one step and a sentence explaining that dates are rewritten the moment it is
active.

**Four plugins do nothing useful until something is done, and that step belongs
here rather than in Usage**: wp-print and wp-email register rewrite endpoints
and wp-downloadmanager registers rewrite rules, so all three need permalinks
re-saved — wp-print's printable page 404s until then. wp-dbmanager needs its
backup folder created, writable and **secured**, which is the one step in the
collection with a security consequence, and it was previously the fourth bullet
of a Usage list where somebody skimming for how to use the plugin scrolled
past it. wp-print's steps were in `## Description`, which is the section meant
to tell a stranger what the plugin is.

* `### Development` and `### Credits` are removed. Development instructions live
  in the repo, not the wordpress.org readme.
* **`### Donations` is kept**, as the last h3 of `## Description`, with exactly
  this wording in all 19 — a plain paragraph, no bullet:

  > I spent most of my free time creating, updating, maintaining and supporting
  > these plugins, if you really love my plugins and could spare me a couple of
  > bucks, I will really appreciate it. If not feel free to use it without any
  > obligations.

  It was in three variants when this was written: 10 exactly as above, 5 with
  a stray `* ` bullet prefix, and 2 with an "as my school allowance" clause,
  while freemyinternet and wp-relativedate had dropped it altogether. All
  nineteen now carry the wording above verbatim.
* **`## Upgrade Notice` is not project history.** It answers two questions and
  only those: what will break for the reader, and what they must do about it.
  wp-useronline opened with a paragraph explaining why the release was numbered
  4.0.0 rather than 3.0.1 — true, and of no use whatsoever to somebody deciding
  whether to press update. Reasoning about version numbering, what a previous
  changelog claimed, and why a decision was taken belong in the commit message
  or the changelog. The same test kills the padding removed in the same pass:
  "a major release", "five things are worth knowing before you update", and the
  paragraph explaining that WordPress will not offer the update on an old stack,
  which describes WordPress rather than the plugin. If a sentence would not
  change what the reader does, cut it.
* **Every breaking change goes under `## Upgrade Notice`**, keyed by version,
  written for a site owner not a developer. `## Changelog` keeps the full list
  including the `IMPORTANT:`/`BREAKING:` lines, but Upgrade Notice is where the
  "what will break for you and what to do" prose lives.
* **A version with no `BREAKING:` changelog entry needs no Upgrade Notice
  section** — a notice saying "nothing breaks" answers a question nobody asked
  (Lester's call, 2026-08-10). A non-breaking release that still rewrites data
  on upgrade, as wp-downloadmanager's 2.0.1 renumbering does, may keep one.
* Changelog entry prefixes are exactly one of `BREAKING:`, `NEW:`, `CHANGED:`,
  `FIXED:`, `NOTE:` — in that order within a version. wp-ban's `IMPORTANT:` is
  renamed to `BREAKING:`.
* The consistency work shipped inside the 2026-08 major entries. Anything after
  those releases is a new version: bump per §14 (starting with `SHIPS_AS` in
  `bin/verify.py`) and give it its own changelog heading.
* Code fences are ` ```php ` or ` ```javascript ` only — the deploy
  rewrites exactly those two plus bare ` ``` ` into `~~~`, one per line.
* **An admin path is written `` `WP-Admin -> Settings -> WP-Print` ``** — ASCII
  `->` for the separator, and the whole path in backticks or bold so it is not
  mistaken for prose. Both halves had drifted and nothing compared them: four
  plugins used a Unicode arrow, three of them mixing both spellings inside one
  file, and wp-print left four paths unmarked. `verify.py` checks both now.
* **The path names the menu entry, not the plugin.** wp-print's install steps
  said `Settings -> Print` while the menu reads `WP-Print` — and the same file
  had it right seven lines later. Read the second argument of the
  `add_*_page()` call rather than shortening the name by eye.

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
  screen itself, where they already know where they are: `Ban Settings`,
  `Plugins Used Settings`, `Manage Ratings`, `Sweep`, `Server Information`,
  `Stats`.

  **A settings screen's heading ends in the word `Settings`, never `Options`.**
  That is a separate rule from the prefix one above and the two are easily
  confused, because both are about the same string. The prefix rule says what a
  heading must **not** carry; this says what a settings heading must **end** in.
  `Ban Settings` satisfies both; `WP-Ban Settings` fails the first and
  `Ban Options` the second.

  So the fifteen settings screens read `Print Settings`, `Database Settings`,
  `Post Views Settings`, `UserOnline Settings`, `E-Mail Settings`,
  `Poll Settings`, `Ratings Settings`, `Download Settings`,
  `FreeMyInternet Settings`, `CommentNavi Settings`, `PageNavi Settings`,
  `Ban Settings`, `Plugins Used Settings`, and the `Settings` tab of wp-stats
  and wp-draftsforfriends. `Manage Ratings`, `Sweep`, `Server Information` and
  `Stats` are **not** settings screens and keep their own nouns — a data screen
  or a report says what it shows.

  The two examples in the list above used to read `Ban Options` and
  `Plugins Used`, which is how this section spent a while teaching the opposite
  of what the collection was converging on. **An example is a rule.** When one
  contradicts the prose beside it, the example is the thing people copy.
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
is the first tab and `Settings` is the last **of the settings tabs**:
where a plugin has templates, `Templates` follows `Settings`, as wp-ban and
wp-useronline do — §4.2.2 requires that and this section's own table shows it.

| Plugin | Tabs |
|---|---|
| wp-stats | `Statistics` / `Settings` |
| wp-useronline | `Users Online` / `Settings` / `Templates` |
| wp-ban | `Stats` / `Settings` / `Templates` |

**Every section is named for what its fields do — except the one that is alone
on its tab.** There the tab label is already the heading, and a section
repeating it says the same word twice in a row. Three habits to avoid, all of
which had taken hold: suffixing `Options` onto a page that is already Settings
(`Download Options`, `WP-Stats Options`), naming a section after the tab
directly above it (`E-Mail Templates`, on the Templates tab), and repeating a
word the surrounding context already supplies.

That last one needs stating carefully, because the obvious phrasing — "drop the
plugin name" — is wrong and leads somewhere silly. `E-Mail Link` and
`Print Link` really did repeat the plugin's name. But wp-polls' sections said
`Poll`, which is the domain's noun rather than the plugin's name, and under an
`<h1>` reading `Poll Settings` it was the *heading* that made it redundant, not
the plugin. **The test is whether the word is doing work where it stands.**
`Sorting Of Poll Answers` became `Answer Order` and `Poll Archive` became
`Archive`, because the heading already said which archive. `Current Active Poll`
became `Current Poll` and kept the word, because `Current` on its own names
nothing. Strip by that test, not by matching the plugin's name.

`General` is a legitimate name for a genuine grab-bag — wp-useronline's timeout,
URL and link-names sit together under nothing more specific — but reach for it
last. `Appearance` belongs to sections that govern how something *looks*
(wp-postratings' shapes and colours, wp-polls' bar), and not to sections holding
markup or behaviour: wp-email's and wp-print's link sections carry a link type
and a template, so they are `Link`. Forcing one word onto sections that do
different jobs moves the inaccuracy somewhere harder to see.

**A tabbed page need not sit under the plugin's own menu.** wp-draftsforfriends
is two tabs under core's **Posts**, because it acts on posts and is gated on
`publish_posts`. The table above says "keeps its top-level menu" because that is
what those three plugins did; the rule is that two screens become one tabbed
page, not that the page must hang off a menu of the plugin's own.

**The merge is required only where more than one tab owns settings.** Where a
tab is a list table posting to itself and holding no key in the option row, no
save can wipe another tab, and reading `get_option()` inside the sanitiser to
merge would break §2.1. Pin the invariant instead — a test that fails the moment
a second tab gains a settings field is the point at which the merge becomes
mandatory, and it fails before anybody loses data rather than after.

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

**Case: buttons, row actions and column headers are title case; prose is
sentence case.** That is core's own split — `Quick Edit`, `Delete Permanently`,
`Move to Trash`, `Add New Post` beside "Allowed variables:" and every
description under a field. So `Edit Draft` and `Copy Link`, not `Copy link`.
The test is where the string sits, not how long it is: a label the user acts on
is title case, a sentence explaining something is not (Lester's call,
2026-08-10, on a row action reading `Copy link` beside core's `Quick Edit`).

Labels already shipped are brought into line as they are touched, not swept —
renaming one is a user-visible change and belongs in the changelog of a release
that had a reason to touch it.

### 4.4.1 A field's hint goes under the field

A hint describing one control sits **in the field cell, directly after the
control**, wrapped in `<p class="description">` — which is where WordPress puts
one, and the only placement a screen reader reaches in the right order.

Five plugins list the `%TOKEN%` variables a template accepts, and before this
rule existed they did it four different ways: wp-postviews in the *heading* cell
as a bulleted column with a capitalised "Allowed Variables:", wp-useronline
*above* the textarea, wp-postratings and wp-email below it, and wp-ban a whole
section-intro away from the field it applied to. Each was defensible alone. Read
together they were one setting with four appearances.

So, for a token list specifically:

```php
echo '<p class="description">' . esc_html__( 'Allowed variables:', 'my-plugin' ) . ' ';

foreach ( $tokens as $token ) {
	echo '<code>' . esc_html( $token ) . '</code> ';
}

echo '</p>';
```

Sentence case — "Allowed variables:", never "Allowed Variables:". Inline
`<code>` separated by a space, not `<ul><li>`: the list is a handful of short
tokens and a bulleted column pushes the field it belongs to off the screen.

**Keep the tokens out of the translatable string.** `phpcbf` reads a `%` inside
one as a printf placeholder and renumbers it, so `%SITE_NAME%` is rewritten to
`%1$SITE_NAME%` and the mangled form is what the user sees. Only the
"Allowed variables:" label is translated; the tokens are concatenated after it.

The heading cell holds the label and nothing else, which means these fields can
use `label_for` and let `do_settings_fields()` write the `<label>` — the reason
wp-postviews hand-built one was that it had a `<ul>` in the title, and a list has
no business inside a label.

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

**A block's editor script is the one exception to the empty dependency array,
and it is a narrow one.** Everything above is about scripts the plugin
hand-registers: those name no dependency, because a dependency there is either
jQuery or something the plugin does not need. A block's editor script is not
one of those. Its handle is minted by core from `block.json`, its dependency
array is written by the build from what the source actually imports, and
`wp-blocks`, `wp-block-editor`, `wp-components`, `wp-i18n`,
`wp-server-side-render` and `react-jsx-runtime` are not extras a block could do
without — they are what a block *is*. The rule for these, and only these, is
therefore: **every dependency must be a handle WordPress itself registers, and
none of them may be jQuery.** Core ships `jquery`, so "core provides it" on its
own would let jQuery back in through the one door §6 exists to close.

Nothing else moves. `js/*.js` is still hand-written, still bundler-free, still
grepped for `jQuery` and `$(`; `build/` is generated and is never edited, never
linted as source, and never counted as a `js/` directory for the vitest rule.

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

  **An AJAX suite is the sanctioned second base**, because it cannot use the
  first: only `WP_Ajax_UnitTestCase` installs the handler that turns
  `wp_send_json_*()` into a catchable exception, and without it the test takes
  the process down (§7.2.3). Such a suite extends a plugin-owned
  `{{CLASS}}_Ajax_TestCase` in `helper-ajax-testcase.php`, which extends
  `WP_Ajax_UnitTestCase`. wp-email and wp-sweep both do this. What is not
  permitted is extending core's class directly — the base has to be the
  plugin's, so there is one place to put what the suite shares.
* Test methods are `test_<what_it_asserts_in_words>()` — long and prose-like.
  They need no docblock, because the name is the documentation; add one only
  where it carries reasoning the name cannot, or where PHPUnit requires it
  (`@dataProvider`, `@covers`). Every assertion carries a message explaining the
  failure.

### 7.2 Shared tests every plugin must have

Every plugin carries `tests/test-metadata.php`. The idea and several of the
assertions came from `wp-showhide/tests/test-metadata.php`; its pre-§7.1 naming
(`Test_ShowHide_Metadata`) is long gone, and every plugin now follows the
structure below through the shared `helper-metadata-testcase.php` template.

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
  **Skipped by the four plugins with no settings row** — wp-relativedate,
  wp-serverinfo, wp-showhide and wp-sweep — which have no sanitiser; they assert
  instead that no `{{UNDER}}_options` row is ever created, through the
  `has_settings_row()` opt-out. This said "two" until 2026-08-03, while
  `helper-metadata-testcase.php` — the file that implements the opt-out — said
  four in its own docblock. The template was right. Prefer naming the plugins to
  counting them: a list can be checked against the overrides, and a bare number
  cannot.
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

  **Do not read a block's dependencies out of `wp_scripts()`.** A block's script
  handles are registered once, at the `init` that the bootstrap fires, and the
  registry they land in is a process-wide global that several plugins rebuild in
  `set_up()` for the reasons at the top of this section — wp-showhide assigns a
  fresh `WP_Scripts` before every test, wp-polls and wp-useronline null it before
  some. In those plugins the handle has simply gone by the time the metadata test
  loops over the registry, so the assertion runs against nothing and passes
  without ever seeing the block. That is how wp-polls shipped a block through a
  green CI run while wp-postratings, which rebuilds nothing, failed on the
  identical dependency array. **The block half is read off disk instead**, from
  the `build/*/*.asset.php` manifest the build wrote and the release ships: same
  answer, same in every plugin, same in every run order.

**Firing `init` a second time re-registers the blocks.** `init` has already
fired once before the first test runs — the bootstrap loads the plugin, then
finishes booting WordPress. A test that fires it again to watch what a plain
front-end request does (§7.6's migration tests do exactly this, and so do the
two shared opt-out branches for a plugin that stores nothing) re-runs everything
hooked there, and `register_block_type_from_metadata()` on an already-registered
name is a `_doing_it_wrong()` notice, which this suite turns into a failure. The
fix is **not** a guard inside the plugin's `register()`: `init` fires once per
request, a second registration in production would be a real bug, and a guard
would swallow it. It is the test's simulation that is imperfect — one process
standing in for two requests — so the shared fixture's `fire_init()` empties the
block registry of the plugin's own blocks first, which is the state a real
second request would start from, and then fires `init`. Anything that re-fires
`init` goes through it.

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

**Grant super admin only where the plugin's own capability needs it.** The
helper's body follows the capability, which is one of the three things plugins
are allowed to differ on. A plugin whose surface is `manage_options` needs no
grant: a site administrator holds that under both, and granting anyway would
make the test user stop representing the operator the plugin actually has,
hiding exactly the class of bug this section is about. **Only wp-sweep,
wp-dbmanager and wp-print need the grant.**

**Adoption: complete as of 2026-08-03, and checked.** All sixteen plugins that
create an administrator now route every one through a helper; the other three —
wp-commentnavi, wp-relativedate and wp-showhide — create none and need nothing.
`verify.py` fails any plugin that reaches the user factory for an administrator
outside `helper-*.php`, which is the only file the helper itself may live in.
Two idioms count as routed: a `create_admin()` that calls the factory, and a
`login_as( 'administrator' )` taking the role as an argument, which is what
wp-downloadmanager's `become_download_admin()` wraps.

Getting there took eleven helpers and 52 call sites, and the count is worth
recording because this paragraph was wrong twice before it was checked. It first
claimed the helper was on every plugin when it was on five. The correction then
said twelve plugins and 55 sites, which was also wrong: it counted
`get_role( 'administrator' )` — a capability assertion, not a user — and listed
wp-downloadmanager as non-compliant in the same breath as calling its idiom
compliant. **A figure nothing measures is a figure that rots**, which is the
argument for the check rather than for a more careful sentence.

Removing the inline calls also settled the one grant this section could not
account for. wp-ban's metadata fixture called `grant_super_admin()` to register
its settings page under multisite, though the page takes `manage_options` and
core leaves that alone on a network. It went with the refactor: a plain
administrator was always the right fixture there, and the grant made the test
user stronger than any operator wp-ban has.

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

**This section is enforced by `bin/test-all.sh`, not by `bin/verify.py`**, and
is the one rule in the standard whose check lives in the harness rather than in
the checker. Said here so that an audit of the spec against the checks does not
read it as unenforced and write a second one.

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

#### 7.6.1 A migration test that does not call `register_setting()` first is testing WP-CLI

The two entry points differ by more than which hook fires, and the difference is
what makes this the collection's most-repeated bug. `register_setting()` runs on
`admin_init`, and it attaches **two** things to the settings row:

* a `sanitize_option_{$option}` filter, so **every** `update_option()` the
  migration makes runs through the settings screen's sanitiser; and
* where a `default` is passed, a `default_option_{$option}` filter, so
  `get_option( $option )` answers with the shipped defaults for a row **that does
  not exist**.

Activation and WP-CLI run neither. So a migration can be correct everywhere a
test looks and lose data on the one path every real update takes — a site owner
pressing *Update* on the Plugins screen, where activation hooks do not fire and
`admin_init` runs the migration alone, after registration.

Four variants of this have now been found, all in different plugins:

1. **wp-print**, ordering — the migration read a row its own earlier step had
   already emptied, because the sanitiser drops retired keys on every write.
2. **wp-postviews** — a retired key had to be dropped in both `Settings::sanitize()`
   and `Options::save()`, because `maybe_upgrade()` runs on `init` and
   `register_setting()` on `admin_init`.
3. **wp-pluginsused**, the read — `false === get_option( self::OPTION )` as
   "there is no row yet" is false once a `default` is registered, so the fold-in
   was skipped and the legacy row deleted anyway.
4. **wp-print**, the write — `update_option()` declines to write a value equal to
   the one `get_option()` would return, and with a registered `default` that is
   the shipped defaults. A migration whose *result* is the defaults therefore
   wrote no row at all, deleted the legacy row it had read, and stamped the
   markers complete.

**Two rules follow, and they are cheap:**

* **Ask for the raw row.** `get_option( $option, false )` inside a migration,
  never the bare one-argument form. `filter_default_option()` returns early when a
  default was passed, so this is the whole fix for the read side.
* **Write through a helper that can tell an absent row from a defaulted one**, and
  `add_option()` when it is absent. `add_option()` runs the sanitiser exactly as
  `update_option()` does, so nothing else changes. `WP_Print_Options::write()` is
  the reference.

**And one about the fixture.** wp-print already had a test that called
`WP_Print_Settings::register()` before the migration, and it passed throughout,
because its fixture was *customised* and so differed from the defaults. **A
fixture that differs from the defaults cannot see a defect that only shows when
it does not.** Every migration suite needs the shipped-settings case — which is
the commonest install in the world — and it must read the **raw** row, because
through a registered default a row that was never written is indistinguishable
from one holding the defaults.

**DDL commits the transaction the test runner wraps each test in.** So a
migration test cannot lean on the automatic rollback: it must rebuild a clean
install in `tear_down()` **and then `COMMIT`**. Skip the commit and the parent's
rollback undoes the cleanup itself — and because the next test's own DDL makes
the leftovers durable, they leak into whichever file runs after this one. That
is not hypothetical; it cost a sibling file its expected value once already.

#### 7.6.2 The migration creates the row, even when the migrated value is the defaults

The fourth variant above is the one with a shape worth pinning, because the fix
is three lines and the failure is total. `update_option()` declines to write a
value equal to the one `get_option()` already answers with; where
`register_setting()` was passed a `default`, an absent row answers with the
shipped defaults. Core's `add_option()` fallback sits immediately below that
comparison — `wp-includes/option.php` lines 921-928 — and is unreachable once the
two compare equal. So a migration whose *result* happens to be the defaults
writes no row at all, deletes the legacy rows it read, and stamps the markers
complete. Nothing errors, nothing logs, and the upgrade can never run again.

Every write a migration makes therefore goes through this shape:

```php
if ( false === get_option( self::OPTION, false ) ) {
	add_option( self::OPTION, $options );

	return;
}

update_option( self::OPTION, $options );
```

The explicit `false` is load-bearing and is the whole trick:
`filter_default_option()` returns early when a default was passed, so an explicit
default defeats the registered one, and that is the only way to tell an absent
row from a defaulted one. `add_option()` runs the `sanitize_option_{$option}`
filter exactly as `update_option()` does, so nothing else about the write
changes. **`WP_Print_Options::write()` is the reference implementation.**

**A plugin may keep a bare `update()` beside it, and two do.** wp-dbmanager and
wp-stats each have a public `update()` the settings screen writes through and a
private `write()` the migration uses; the bare one is correct there, because
`options.php` has already created the row by the time a screen can save one. The
guard is owed on the path *the migration* takes, not on every writer in the
class. Where a plugin puts it is its own business — wp-postratings put it inside
its single `update()`, wp-draftsforfriends inline in `migrate()` and only then
calls the bare `update()` — provided no migration can reach a write that cannot
tell the two cases apart.

**A plugin that passes no `default` is not exposed**, and must not be made to
guard against something that cannot happen to it: with no `default_option` filter
`get_option()` answers `false`, and core's own `add_option()` fallback fires.
freemyinternet, wp-commentnavi and wp-pagenavi are in that position.

This was stated and enforced nowhere, which is exactly why six plugins carried
the guard and six did not. `verify.py` checks it now: a migration that reaches a
bare `update_option()` of the plugin's own settings row fails, and only where a
`default` is registered. It finds migrations **by name** — anything with
`migrate` or `upgrade` in it, which is what all nineteen call them — so a
migration named something else is a migration nothing checks. Name it the way
its siblings are named.

---

## 8. CI

`.github/workflows/ci.yml` is copied verbatim from `_standards/templates/`, with
`{{SLUG}}` substituted. Four jobs — `phpcs`, `eslint`, `e2e`, `phpunit`; the
PHPUnit job has **six** rows — every supported stack in both modes, no special
cases:

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
`shivammathur/setup-php@v2` (PHP 8.2, `coverage: none`, `tools: cs2pr`), and
`actions/upload-artifact@v4` for the Playwright traces the `e2e` job keeps on
failure — a passing run uploads nothing.

Job names are exactly `PHP coding standards`, `JS coding standards and tests`,
`End-to-end (Playwright)` and `PHPUnit (WP …, PHP …, …)`.

**A plugin with no JavaScript at all deletes the whole `eslint:` job**, from its
`eslint:` line through to the job that follows it. The template carries no
comment saying so — an instruction to the person copying the file has no
business shipping in nineteen committed workflows.

"No JavaScript" means no `js/` **and** no `tests/e2e/`. The Playwright specs are
JavaScript too, and a plugin whose only scripts are those still needs linting.
Reading the rule as "no `js/` directory" is how five repositories came to ship
e2e specs that nothing had ever linted — the first CI run after they landed
found style errors in a file that had been committed and pushed twice.

The same rule read the other way is how three plugins with no JavaScript once
carried an `eslint:` job for months: it never ran a linter, because it died at
`actions/setup-node` looking for a lock file in a repository with no
`package.json`. A job that cannot pass is worse than no job; it teaches everyone
to ignore a red mark.

**As of 2026-08-03 this rule has no subjects.** Every one of the nineteen has a
`tests/e2e/` suite, so every one has JavaScript by the definition above and
every one keeps its `eslint:` job. The rule stays for the next plugin, not for
these — and it is written as a derivation from `js/` and `tests/e2e/` rather
than as a list of names precisely so that a nineteen-to-zero change needs no
edit here beyond this paragraph.

`npm run test:js --if-present` rather than `npm run test:js`, because a plugin
can have JavaScript worth linting and no vitest suite: a plugin whose only
scripts are Playwright specs has nothing for jsdom to load. `lint:js` is not
optional in the same way — anything lintable gets linted.

Every repository also carries `claude.yml` and `claude-code-review.yml` —
@claude on issues and PR comments, and a Claude review posted inline on every
pull request. They are copied verbatim from wp-postviews' current revision and
need the `CLAUDE_CODE_OAUTH_TOKEN` secret in each repository to run; they are
not part of the CI contract above and verify.py does not check them.

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

Ship no raster images — inline SVG (an `<svg>` printed by PHP, or a CSS
`mask-image` with a data URI) or a CSS-only construction instead. The
replacements the revamp made:

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

`package.json`: same shape as `wp-ban/package.json`. Same devDependency versions
across all plugins.

The script set follows from what the plugin has, and nothing else. Five are
unconditional:

| Script | Runs |
|---|---|
| `lint:js` | `eslint .` |
| `lint:js:fix` | `eslint . --fix` |
| `test` | `bin/test.sh` — the PHPUnit suite |
| `test:e2e` | `bin/test-e2e.sh` |
| `test:e2e:headed` | `bin/test-e2e.sh --headed` |

Two more **only** where the plugin has a `tests/js/` directory, which twelve of
the nineteen do:

| Script | Runs |
|---|---|
| `test:js` | `vitest run` |
| `test:js:watch` | `vitest` |

A plugin with no vitest suite carries neither: a script pointing at a runner
with nothing to run is a green result that means nothing. Every plugin has
`tests/e2e/`, so the two E2E scripts are unconditional today; they follow the
directory, not the count.

> This section named five scripts and no E2E entry until 2026-08-03. The two
> E2E scripts arrived with the Playwright work and were never written back, so
> **every plugin diverged from the spec, identically, and nothing noticed** —
> there was no check. `verify.py` now derives the expected set from `tests/js/`
> and `tests/e2e/` and compares it. A rule nothing compares is a rule that goes
> out of date silently.

---

## 13. WP-Stats integration — the one cross-plugin contract

Seven plugins read the bare `stats_display` row when this was written, and
five read `stats_mostlimit`: wp-downloadmanager, wp-email, wp-polls,
wp-postratings, wp-postviews, wp-stats and wp-useronline. None reads either
outside its migration now, which is what the contract below achieved. These are unprefixed, shared, legacy
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

## 13.3 WP-CLI and REST naming

wp-sweep set it, and the collection copied it — shipped in the 2026-08 majors:

* **WP-CLI command name is the slug without the `wp-` prefix**: `wp sweep`,
  not `wp wp-sweep`.
* **REST namespace is the same name plus a version**: `sweep/v1`.

**This reverses a decision, and the reversal is Lester's, 2026-08-04.** The
section previously required the full slug — `wp wp-sweep`, `wp-sweep/v1` — on the
grounds that a bare noun is a name any plugin could claim and that neither
WordPress nor WP-CLI detects the collision. That risk is real and is accepted.
Three things outweigh it:

* **The `wp-` prefix is a wordpress.org directory convention, not a naming
  convention for commands.** It exists because the directory is a flat namespace
  of WordPress plugins. Carrying it into the command spells `wp` twice, and
  `wp wp-sweep` reads as a mistake.
* **The ecosystem settled this**: `wp wc`, `wp yoast`, `wp jetpack`. The norm is
  the brand, not the slug. A collection that departs from it looks wrong rather
  than looks careful.
* **These are the names the released 1.2.0 already shipped**, so keeping them
  costs nothing and changing them would have broken every script calling
  `wp sweep` for a cosmetic gain. The prefixed form was a breaking change
  invented by this campaign; dropping it deletes that breakage rather than
  documenting it.

**Where the collision risk actually lands.** Most of these slugs are distinctive
enough that the bare noun is nobody else's plausible claim — `commentnavi`,
`pagenavi`, `draftsforfriends`, `postratings`, `postviews`, `dbmanager`,
`pluginsused`, `relativedate`, `showhide`, `useronline`, `freemyinternet`. Three
are not: **`email`, `print` and `stats`** are names a dozen plugins might want.
Those three are **not** settled by this section. If any of them ever earns a
command or a namespace, decide it then — either a qualified name or a shared
`wp lc <plugin>` parent — and record the answer here. Do not let this section be
read as blanket permission to claim `wp email`.

---

## 13.4 What earns a command, a namespace and a block

§13.3 pins what these things are *called*. This pins which plugins get one, and
the two are separate questions because **the three surfaces do not select the
same plugins**:

* A **block** follows the front-end surface. Twelve plugins register a public
  shortcode or a widget; seven register neither and cannot have one.
* A **command** follows the admin action. The two most scriptable things in the
  collection — wp-dbmanager's backup and optimise, wp-ban's ban list — render
  nothing on the front end at all, so they appear in no block column.
* A **namespace** follows a client that is not a browser following a link, which
  is the smallest of the three for the reason immediately below.

### 13.4.1 A block does not earn a namespace

The tempting argument for registering nineteen REST namespaces is that a block
needs one to preview itself in the editor. **It does not.** Core routes
`@wordpress/server-side-render` through `/wp/v2/block-renderer/<name>`, a core
endpoint that renders any block registered with a `render_callback` and
PHP-side attributes. A dynamic block that wraps a shortcode gets its editor
preview from core and registers no route of its own.

So a namespace has to earn its place on its own evidence: an existing
`admin-ajax.php` action that would be better as a route, or a client that is
neither the editor nor a form post. Seven plugins touch `admin-ajax.php` —
wp-ban, wp-email, wp-polls, wp-postratings, wp-postviews, wp-sweep and
wp-useronline — and **those, not the twelve with shortcodes, are where the
question is live**.

### 13.4.2 Blocks wrap the shortcode. They never replace it.

**Lester's call, 2026-08-07.** The block's `render_callback` calls the same
method the shortcode callback calls. The shortcode stays registered, documented
and supported, with no deprecation notice attached to it.

The reason is arithmetic rather than taste: these plugins have shipped for
fifteen years and more, and `[poll]`, `[ratings]` and `[views]` sit in an
unknowable number of published posts on sites nobody here can survey. **A block
is an addition to the collection's surface, never a replacement for part of
it.** Two consequences follow and both are load-bearing:

* **No migration, no Upgrade Notice, no breaking change.** A block is the one
  thing in this campaign that costs an existing install nothing.
* **No plugin's major version moves for a block.** §14's table is unaffected.

Every shortcode callback in the collection is already a callable returning a
string, so the wrapping is mechanical: the two entry points share one renderer
and neither is the other's caller.

### 13.4.3 An inline shortcode is not a block

A block is a top-level chunk of a post. A shortcode that produces a fragment
inside somebody's sentence is a **rich-text format**, and one that wraps content
to suppress it is neither:

* **Chunk output, so a block is right**: `poll`, `page_polls`, `ratings`,
  `views`, `page_useronline`, `page_stats`, `download`, `page_download`,
  `showhide`, and wp-pluginsused' three list shortcodes. `page_downloads` is not
  listed separately: it is an alias of `page_download` on the same callback, and
  listing it here read as a second thing to build.
* **Inline, so a block is wrong**: `relativedate`, `relativetime`, `print_link`,
  `print_link_tag`, `email_link`. These belong in a sentence and a block would
  put each on its own line.
* **Enclosing markers, so neither**: `donotprint`, `donotemail`. They mark a
  region for another plugin to strip and render nothing themselves.

### 13.4.4 The scope

Proposed 2026-08-07 from the counts above; built in full and shipped in the
2026-08 majors.

| Plugin | Command | Namespace | Block |
|---|---|---|---|
| wp-sweep | `wp sweep` | `sweep/v1` | — |
| wp-polls | `wp polls` | `polls/v1` | `poll`, `page_polls` |
| wp-postratings | `wp postratings` | `postratings/v1` | `ratings` |
| wp-postviews | `wp postviews` | `postviews/v1` | `views` |
| wp-useronline | `wp useronline` | `useronline/v1` | `page_useronline` |
| wp-downloadmanager | `wp downloadmanager` | — | `download`, `page_download` |
| wp-dbmanager | `wp dbmanager` | — | — |
| wp-ban | `wp ban` | — | — |
| wp-draftsforfriends | `wp draftsforfriends` | — | — |
| wp-showhide | — | — | `showhide` |
| wp-stats | — | — | `page_stats` |
| wp-pluginsused | — | — | its three list shortcodes |
| wp-email | — | — *(excluded, see 13.4.5)* | — |
| wp-print | — | — | — |
| wp-relativedate | — | — | — |
| freemyinternet, wp-commentnavi, wp-pagenavi, wp-serverinfo | — | — | — |

The four plugins with nothing in any column earn nothing, and that is a result
rather than an omission: freemyinternet, wp-commentnavi, wp-pagenavi and
wp-serverinfo have no scriptable admin action and no self-contained front-end
chunk. **Adding a command to a plugin that has no action to script is how a
collection acquires nineteen commands nobody runs.**

**wp-downloadmanager registers three shortcodes and earns two blocks, because
two of the three are the same shortcode.** `page_download` and `page_downloads`
are both registered to `WP_DownloadManager_Display::page_shortcode()`, which
takes `$atts` and never the tag, so it cannot tell which one invoked it —
identical output, identical single `category` attribute. Both have been there
since the first commit, so the plural is long-standing typo tolerance rather
than anything this campaign introduced.

**The singular is the canonical one** — corrected 2026-08-08, Lester, after this
table had picked the plural. Everything else in the plugin already agreed:
README documents `[page_download]` and never mentions the plural, the e2e
helper defaults to it, and the PHPUnit pair is named
`test_the_page_download_shortcode_renders_the_listing` against
`test_the_page_downloads_shortcode_is_an_alias`. For a shortcode the choice
would be cosmetic, since both stay registered either way — but **a block name is
written into `post_content` and outlives the post's edit history**, so the block
wraps the documented spelling and the alias gets no block of its own.

**The alias stays registered** — Lester, 2026-08-08, asked directly. Dropping it
from this document is a documentation change and nothing more. Anyone who typed
`[page_downloads]` has that string in `post_content`, so deregistering it would
render literal text on a live page, which is the failure §13.4.2 exists to
prevent, and it would move the plugin's major version to remove a line that
costs nothing to keep. `test_the_page_downloads_shortcode_is_an_alias` pins it.

### 13.4.5 None of the three names has to be claimed — but read *why*

§13.3 deliberately left `email`, `print` and `stats` unsettled, being bare nouns
a dozen plugins might want. None of the three ends up being claimed, and **the
reason differs by plugin.** An earlier draft gave one reason for all three, and
it was false for one of them.

**`print` and `stats`: nothing to build.** wp-print registers no
`admin-ajax.php` action at all and already serves its printable page from the
`/print/` rewrite endpoint — a JSON route returning that same HTML as a string
has no client. wp-stats registers none either, and owns no data of its own: it
renders whatever the `wp_stats_sections` filter collects from its companion
plugins. A stats feed is a plausible thing to want, but it would be **surface
this campaign invented**, which is what §13.4.1 exists to prevent.

**`email`: there is something to build, and Lester's call on 2026-08-08 was not
to.** This is the correction that matters, because the obvious reading of the
code says otherwise and a future reader will find it. wp-email registers four
`admin-ajax.php` actions and **two are `nopriv`**, so the earlier claim that it
"earns nothing" was simply wrong. What they are, and why only one was ever a
candidate:

* `wp_ajax_nopriv_email` → `WP_Email_Form::process()` validates the
  send-to-a-friend submission and sends it, **returning HTML either way** — a
  rendered error list or a confirmation. A route answering
  `{ sent, errors[] }` would genuinely improve on that, because today the
  validation errors are expressible only as markup and no non-browser client can
  read them.
* `wp_ajax_nopriv_wp_email_captcha` → serves a **PNG** keyed by a one-shot
  transient token, 404 on an unknown one, deliberately nonce-free because it is
  an `<img src>` for a logged-out visitor. **This was never a REST candidate**:
  REST is JSON, an image tag wants a binary body and cache headers, and a route
  bypassing `rest_ensure_response()` is all cost.

So wp-email would have gained exactly **one** route — and claiming a noun as
contested as `email` on every site that installs the plugin, to host a single
send endpoint, is a bad trade. The form stays on `admin-ajax.php`, where it
works and where nothing is broken. **Do not "finish the job" by adding
`email/v1` later**: the omission is the decision.

If that is ever revisited, the alternatives are a qualified namespace
(`lc-email/v1`) or the REST analogue of §13.3's shared parent
(`lc/v1/email/send`) — not the bare noun.

**The lesson underneath** is the one this collection keeps relearning: the scope
table above was built by counting what each plugin registers, and two cells were
filled in from memory instead. wp-email was given a blanket dash, and
wp-postviews was given no namespace while registering
`wp_ajax_nopriv_wp_postviews` — a logged-out visitor incrementing a counter,
which is the definition of a route this section wants. Both were found by
re-running the grep rather than by re-reading the table.

### 13.4.6 Order of work

**Complete.** WP-CLI and REST went out across the collection first, then the
blocks as a phase of their own — Lester's call, 2026-08-08, reversing the
plugin-by-plugin order set on 2026-08-07. Both decisions are kept because the
reasoning binds the next surface anyone adds.

**Why plugin by plugin was right at the time.** wp-polls earns all three, so
taking one plugin end to end was the only way to get a complete worked example
before anything was copied eighteen times. That has now happened for two of the
three surfaces: `wp polls` and `polls/v1` are written, tested and merged into
the reference, and §13.4.7's naming came out of building them rather than being
guessed in advance.

**Why it changed.** Blocks are the one surface that is not more of the same.
They add a JavaScript build to a collection that has never had one — `src/`,
`build/`, `@wordpress/scripts`, a CI step, committed build output, and the
deploy-exclusion hazard in §13.4.9. **Carrying that per plugin, interleaved with
seven commands that need none of it, spreads a one-time decision across
seventeen repositories.** The two surfaces that *are* more of the same should
finish first, from a reference that already works.

Both of the conditions that order imposed were met: §13.4.9's
`--exclude='src'` landed **before** the first `src/` directory existed, and the
first block was wp-polls' — the reference plugin's third surface, built where
the other two already were.

### 13.4.6a What a route answers when it will not do the thing

**Lester's call, 2026-08-08: a refusal is 403.** Three codes, and the line
between them is *who decided*:

| Code | When | Examples |
|---|---|---|
| **400** | the REST layer's own parameter validation rejected the request before the plugin saw it | a `validate_callback` failing — an unknown `mode`, a value outside a fixed list |
| **403** | the request was well formed and understood, and **the plugin declined to act** | already voted, already rated, poll closed, rating off the scale, bad nonce, a site that counts views during the render |
| **404** | the request named a resource that is not there | a poll or post id matching no row |

The first draft used 400 for every refusal, which conflates "you sent me
nonsense" with "I understood you and the answer is no". A client cannot tell
from a 400 whether retrying differently would help; a 403 says plainly that it
would not.

**A missing resource stays 404 and is not folded into this**, for the reason
§13.4.4's routes already record: existence is deliberately not a
`validate_callback`, because a failed validator is a 400 and a deleted poll is
not a malformed request.

### 13.4.7 What the files are called

Two of the three surfaces already have a reference and are copied rather than
decided. The naming rule they follow, stated once because it is not obvious from
either example on its own: **the shipped class is named for the thing it is, and
the test is named for the surface it exercises.** That is why `WP_Sweep_Command`
is tested by `test-cli.php` and `WP_Sweep_API` by `test-rest-api.php`, and it is
why the test files sit in an alphabetical row with `test-admin-ajax.php` — all
named for what a user of the plugin can reach, not for the class behind it.

| | Shipped class | Its file | Test class | Its file | Browser test |
|---|---|---|---|---|---|
| WP-CLI | `WP_{{...}}_Command` | `includes/class-{{SLUG}}-command.php` | `WP_{{...}}_CLI_Test` | `tests/test-cli.php` | — |
| REST | `WP_{{...}}_API` | `includes/class-{{SLUG}}-api.php` | `WP_{{...}}_REST_API_Test` | `tests/test-rest-api.php` | `tests/e2e/rest.spec.js` |
| Blocks | `WP_{{...}}_Blocks` | `includes/class-{{SLUG}}-blocks.php` | `WP_{{...}}_Blocks_Test` | `tests/test-blocks.php` | `tests/e2e/blocks.spec.js` |

The class name is not free: §2.4's rule that a class lives in the file named
after it is enforced by the shared metadata fixture, so `WP_Polls_Command` can
only ever live in `class-wp-polls-command.php`.

**One `WP_{{...}}_Blocks` class registers all of a plugin's blocks**, rather
than a class per block. wp-polls has two and wp-downloadmanager has two; a class
whose whole body is one `register_block_type_from_metadata()` call is a file per
block for no gain, and the one-class-per-file rule would make it exactly that.

Where the WP-CLI stand-ins are needed, they are `tests/helper-wp-cli.php` (the
facade), `tests/helper-wp-cli-command.php` (the base class the command extends)
and, only where the command prints a table, `tests/helper-wp-cli-utils.php` (the
namespaced `format_items()`). Three files because the coding standard allows one
class per file and that rule is not relaxed for the suite.

**A command or a namespace is not finished until the README says so.** This was
missed on the first three plugins and caught by Lester rather than by any check,
which is what makes it worth stating: a command nobody is told about is a
command nobody runs, and `README.md` ships to wordpress.org as `readme.txt`, so
it is the only documentation most users will ever see. Two additions, both
following wp-sweep, which has carried them since 1.2.0:

* **`## Usage` gains a `### WP-CLI` block and a `### REST API` block** — a fenced
  list of the actual invocations and routes, then anything a caller cannot
  guess: what is public, what credential a write needs, and that the response
  carries rendered markup because the site's templates decide what it looks
  like.

  **Where they go is settled by wp-sweep and is not the end of the section.**
  Its `## Usage` runs: prose about the screen, `### WP-CLI`, `### REST API`,
  then the reference material — `### Item names`, `### Filters`, `### Actions`.
  So the order is **how a person uses it, then the two machine interfaces, then
  the extension points**, and WP-CLI comes before REST. Appending them after a
  plugin's filters and template-variable documentation is wrong; wp-polls was
  written that way and moved.
* **`## Changelog` gains `NEW:` bullets** under the version being prepared —
  `NEW:` is one of the five prefixes the shared metadata fixture enforces, and
  the right one, since none of this changes existing behaviour.

**Say in both places that the `admin-ajax.php` action survives.** §13.4.2's
promise about shortcodes applies here too, and a reader who sees a new REST
route and no such sentence will reasonably assume the old endpoint is going
away.

### 13.4.8 A block's name is permanent, so it keeps the `wp-` prefix

**This is the one place §13.3's reasoning does not carry**, and the difference is
worth stating because the surface consistency argument points the wrong way.

A block is `wp-polls/poll`, not `polls/poll`.

§13.3 drops the `wp-` prefix for commands and namespaces because a collision
there is survivable: WP-CLI gives the name to whichever plugin registered last
and the loser's command is simply absent, which is visible immediately and fixed
by deactivating something. **A block name is written into post content** — `<!--
wp:wp-polls/poll -->` is saved in `post_content` and stays there for the life of
the post. Two plugins claiming one block name means one of them renders the
other's block inside somebody's published posts, and the damage is in the
database rather than in a shell session.

So blocks take the collision-resistant name, and the fact that it matches the
plugin's directory on wordpress.org is a convenience rather than the reason.

### 13.4.9 Blocks change what the deploy ships — read this before the first one

> Written against the deploy script, which is retired; the deploy now lives in
> the `release-wp-plugin` skill, whose Steps 4b–4c carry the same build guard
> and exclusion list. The history stays because it is why those guards exist.

The deploy rsyncs the working tree against an **exclusion list**, so
anything a build step leaves on disk ships unless it is named. Adding blocks
adds two directories and they want opposite treatment:

* **`build/` must ship.** It is what `register_block_type_from_metadata()`
  loads, and it is correctly not excluded today.
* **`src/` must not.** Unbuilt JSX is of no use to a site, and this rsyncs the
  working tree rather than a clean export, so sources on disk would ship.

**`--exclude='src'` is in the script as of 2026-08-08, added while no plugin had
a `src/` directory yet** — the only moment the change costs nothing and cannot
be tested against a real deploy. The comment beside it warns the next reader not
to add `build/` alongside it for symmetry: excluding `build/` ships a plugin
whose blocks cannot render.

The build itself needs no new mechanism: the script already runs `$SRC_DIR/bin/build`
before the rsync if that file exists, and `bin` is excluded from what ships. That
ordering is also what makes the `src/` exclusion safe — the build has already
turned `src/` into `build/` before anything is copied.

**Verified by dry run rather than by reading**, per the rule below, using a
scratch plugin containing both directories and the exclusion list parsed out of
the real script rather than retyped. `build/poll/index.js` and
`build/poll/block.json` shipped; `src/` did not. Then the mutation: with
`--exclude='src'` dropped from the parsed list and nothing else changed, both
`src/` files shipped. So the line is what stops them, and not some other
exclusion catching them by accident.

This is the fifth entry in a list whose lesson is that **a deny list acquires a
new member every time the toolchain grows** — the same trap §7.2.1 records for
metadata tests scanning the plugin root. The four before it were found by
dry-running the rsync into a scratch directory and reading what came out. Do
that again when the first real `src/` exists, rather than trusting this
paragraph: a scratch fixture proves the pattern matches, not that the toolchain
puts everything where this assumed it would.

**A failed build now stops the deploy, and did not before — added 2026-08-08.**
The old deploy ran `bin/build` without checking whether it worked, and the
rsync copies the **working tree**, so a build that failed for any reason — no
Node, a malformed `block.json`, a webpack error — left the previous `build/` on
disk, or none at all, and the deploy published it. `build/` being gitignored is
what makes this bite: on a fresh clone a failed build means the directory does
not exist, `register()` skips registration, and the release reaches users as a
plugin whose blocks silently never appear in the editor.

Two guards, both checked by running them: a non-zero exit from `bin/build`
aborts before anything is copied, and a plugin with a `src/` but no `bin/build`
aborts too, because that combination cannot produce a `build/` at all. Not
`set -e` for the whole script — `svn mkdir` on an existing directory and the
`rm -rf` loop both fail harmlessly by design, and aborting on those would break
every deploy including the eleven plugins with no blocks.

**Done, against wp-polls' real `src/`, 2026-08-08** — and it found nothing new,
which is the outcome worth recording because the instruction above assumed it
might. `src/` absent, `build/` shipped complete with the nine files webpack and
`bin/build` put there, and no leak of `tests`, `bin`, `CLAUDE.md`, `AGENTS.md`,
`package.json`, `artifacts` or `node_modules`. Re-run it anyway for the first
plugin whose build emits something wp-polls' does not — a stylesheet, a
`viewScript`, a `render.php`.

### 13.4.10 What the first block plugin cost, and what the next seven inherit

wp-polls is built and is the reference. Five things came out of it that were not
in the plan, and all five are the toolchain rather than the blocks:

* **`build/` is generated, gitignored, and shipped.** That combination is
  unusual here and every rule below follows from it. `src/` is the opposite:
  committed and not shipped.
* **Three scripts had to learn to build.** The deploy already ran
  `bin/build`; `bin/test.sh` and `bin/test-e2e.sh` did not, and without them a
  checkout that has never been built fails the block tests for a reason
  unrelated to the code — or worse, on a checkout where `src/` changed since the
  last build, **silently tests the previous build and passes**.
* **CI's PHPUnit job builds too**, because it invokes phpunit directly rather
  than through `bin/test.sh` — the matrix picks the config file — so the build
  step is repeated there rather than inherited. Six matrix rows, so it is an
  `npm ci` six times; that is the price and it is why the step is conditional.
* **The shared metadata suite requires an `index.php` in every directory, and
  webpack does not know that.** `build/` and each block's directory under it
  need one, so `bin/build` writes them after the compile — *walked*, not listed,
  or a block added later ships without one. This is §7.2.1's trap arriving from
  a new direction: the suite scans what is on disk, and a generated directory is
  on disk.
* **phpcs must exclude `build/`.** webpack writes each block an
  `index.asset.php` on one line, and its formatting is webpack's to decide
  rather than ours to sniff. ESLint covers `src/` instead.

**The three shared files became conditional rather than uniform.** `ci.yml`,
`package.json` and `phpcs.xml` all now carry block support that `bin/verify.py`
drops for a plugin with no `src/`, the way the eslint job is already dropped for
a plugin with no JavaScript. Eleven of the nineteen will never have blocks. A
`build` script in a plugin with nothing to build is not merely redundant — it is
a command that fails the first time anybody runs it — so the two `wp-scripts`
entries are an **error** when `src/` is absent, not merely tolerated.

**Two things in the block sources that lint will demand.** `edit` must be a
capitalised named component rather than an `edit()` shorthand, because
`useBlockProps` is a hook and the hook rules identify a component by that
capital; and `__experimentalNumberControl` is forbidden, so a numeric field is
`TextControl` with `type="number"`. Both are ESLint errors, not opinions.

**The poll is chosen by id typed into a field, not from a dropdown.** A dropdown
needs a route listing every poll, and §13.4.1 is why there isn't one: the
namespace carries what the AJAX endpoint already carried and no more. If a
picker is ever wanted, that is a decision to make on its own evidence, not a
control to add and a route to invent for it.

**What to assert, in the order the value falls.** The PHPUnit suite should pin
that the block and the shortcode render **identical** markup — two entry points
that merely both work can drift; byte-identical output is evidence they are
going through one renderer — and that **neither is implemented in terms of the
other**, by unregistering each and watching the other carry on. The browser
suite should not repeat any of that. Its whole justification is that `build/` is
generated, so every assertion in it is also an assertion that the build ran and
produced something a browser can load: the editor script registering both
blocks, and a poll rendered from a block actually being votable.

---

## 14. Versions and the release baseline

**All nineteen were released to wordpress.org on 2026-08-09/10**, so the
repositories and the directory agree for the first time: each README's
`Stable tag:` is the version being served, and every plugin has a real SVN
tag — including the five that had sat on `Stable tag: trunk` for years
(freemyinternet, wp-commentnavi, wp-draftsforfriends, wp-pluginsused,
wp-relativedate; an earlier version of this section counted four).

**Seven of the ten staged patches went out on 2026-08-24**, leaving three.
wp-downloadmanager 2.0.1 was **re-tagged** the same day rather than superseded:
its category migration wrote the shifted list before it moved the rows and took
no lock, so an interrupted or doubled run could leave every file reading its
neighbour's category. Lester's call was that the directory takes about a day to
propagate and almost nobody could have had the first cut yet. That is the
exception and not a precedent — the default for a version already published is
a new number, because a re-tag leaves whoever did download it holding different
bytes under the same version for ever.

**The machine-readable half of this table is `SHIPS_AS` in `bin/verify.py`**,
which pins every version marker in a repo — header, `Stable tag`, constant — to
the version that repo intends to ship. It moves when a new version is
**staged**, so bumping a plugin's version starts there. For what is actually
*live*, query the directory rather than any table or checkout:
`https://api.wordpress.org/plugins/info/1.2/` per slug, or the comparison loop
at the end of the `release-wp-plugin` skill for the whole set.

What is live now, with the pre-revamp release each migration still has to carry
sites forward from. A row reading `staged in git` is one whose repository is
ahead of the directory:

| Plugin | Live on wordpress.org | Pre-revamp release |
|---|---|---|
| freemyinternet | 1.0.1 | *trunk* (0.01) |
| wp-ban | 2.0.0 | 1.69.2 |
| wp-commentnavi | 2.0.0 | *trunk* (tag 1.10) |
| wp-dbmanager | 4.0.0 | 3.0.0 |
| wp-downloadmanager | 2.0.1 | 1.69.2 |
| wp-draftsforfriends | 2.0.1 | *trunk* (1.0.2) |
| wp-email | 3.0.0 | 2.69.4 |
| wp-pagenavi | 3.0.0 — 3.0.1 staged in git | 2.94.6 |
| wp-pluginsused | 2.0.1 | *trunk* (tag 1.50) |
| wp-polls | 3.0.0 — 3.0.1 staged in git | 2.77.3 |
| wp-postratings | 2.0.0 — 2.0.1 staged in git | 1.91.3 |
| wp-postviews | 2.0.1 | 1.78.1 |
| wp-print | 3.0.0 | 2.58.3 |
| wp-relativedate | 2.0.0 | 1.51.1 |
| wp-serverinfo | 3.0.0 | 2.0.0 |
| wp-showhide | 3.0.0 | 2.0.0 |
| wp-stats | 3.0.0 | 2.56.1 |
| wp-sweep | 2.0.1 | 1.2.0 |
| wp-useronline | 4.0.1 | 3.0.0 |

Two plugins shipped a different major from what the repo long carried, and the
reasons are kept because they generalise:

* **wp-dbmanager went to 4.0.0** because 3.0.0 was already live on
  wordpress.org — an unreleased entry must never collide with shipped history.
* **wp-useronline went to 4.0.0** because its 3.0.0 changelog promised the
  template tags, shortcode and all four filters unchanged, and this release
  renamed the filters and `USERONLINE_TRUST_PROXY` — a promise a patch number
  cannot break. Its Upgrade Notice lists the five old → new pairs.

### 14.1 Upgrade Notice must cover the whole SVN → major gap

`## Upgrade Notice` is written against the oldest version a site owner may
still be running — for the 2026-08 majors that meant the pre-revamp release in
the table above — never against the previous git commit. Everything a site
owner updating from that version would notice must appear there:

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

All nineteen have been through this; it stays as the order for bringing any
future plugin to the standard.

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
