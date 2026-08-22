# Pass-eight convergence canon — the chosen shapes
Every fix agent follows this exactly. "Canonical" = rename/rewrite outliers to this.

## Method names
- Front-end asset pair: `scripts()` / `styles()` (wp-polls renames poll_scripts/poll_styles; wiring + block_editor_styles callers updated).
- CSS-only enqueue callback: `enqueue_styles()` (commentnavi + pagenavi rename `stylesheets()`).
- Asset URLs: always the `WP_X_URL` constant, never plugins_url() (fix wp-pagenavi core :39, wp-stats :131).
- Asset handles: literal 'wp-slug' string (freemyinternet, commentnavi, showhide drop the SLUG-const handle).
- Options: `defaults()` (not get_defaults) · `markers()` (not get_versions) · `update_markers()` no-arg reading the constants (not save_markers($p,$d)) · `flush()` (not flush_cache) · `migrate_legacy_rows()` (not migrate_from_legacy_rows) · `sanitize( $input )`.
- Activation entry: `activate( $network_wide = false )` everywhere (wp-polls `activation`, wp-downloadmanager `on_activation` rename). Per-site verb: `install()` (ban/dbmanager/print rename activate_site; dlm/polls per-site activate()→install()). register_activation_hook registered from the BOOTSTRAP class (postratings shape) pointing at Install where an Install class exists.
- Upgrade hook: `add_action( 'init', …, 5 )` for maybe_upgrade in EVERY plugin that used admin_init (freemyinternet, commentnavi, dff, downloadmanager, email, pagenavi, pluginsused, print) and postviews moves prio 1→5. Carry the canonical comment (below). Plugins calling maybe_upgrade directly in bootstrap (ban, dbmanager, useronline) keep that (direct call runs even earlier) — but add nothing.
- admin_menu callback: `add_page()` (rename: dbmanager/downloadmanager/postratings `menu`, email/postviews `add_menu`, dff/sweep `admin_menu`, polls `poll_menu`).
- Settings API registration: `register()` (freemyinternet, commentnavi, dff, pagenavi, pluginsused, useronline rename register_settings).
- admin_enqueue_scripts callback: `enqueue()` (others rename; polls `poll_scripts_admin`→`enqueue`).
- Widget wiring: bootstrap method `register_widget()` on widgets_init (polls renames widget_polls_init; downloadmanager moves its Widget::init closure into the bootstrap). Widget ctors: inline array arg (polls drops $widget_ops var); `__()` not `esc_html__()` in postratings widget title/desc. id_base strings NEVER change.
- WP-CLI: the 8-plugin majority `register_command()` shape verbatim (negative guard, require_once, add_command, shared docblock). wp-sweep extracts its init() nesting into that exact shape.
- Blocks init docblock: "Hooks block registration." (stats, useronline fix "Hook").
- WPStats bridges: static `init()` (email converts from instance); `most_limit()` (downloadmanager renames limit()).
- REST: instantiate API classes inside the bootstrap (polls moves `new WP_Polls_API()` from file scope).
- capability(): keep per-plugin $context defaults; add `( $context = 'settings' )` to wp-email Settings' no-arg copy; cast `(string) apply_filters(...)` everywhere missing (dbmanager, downloadmanager, dff x2, polls, postviews, stats, sweep); downloadmanager splits its ternary into a second Settings::capability() like email/dff. Filter docblock summary canonical: "Filters the capability required to reach a {Display-Name} screen." (+ existing context lines kept); @param line: "The required capability."; fix "Filter "→"Filters " (stats admin :60, useronline admin :117).
- Singleton constructors: `private function __construct()` (dbmanager, dff, email, sweep, useronline change from public; stats keeps protected? NO — converge stats protected→private too unless a subclass needs it — check first). get_instance() docblock summary: "Get the instance, creating it on first call."
- Component init() docblock summary: "Hook registration." (all component classes' static init()).
- Main file shape: header + constants + requires (using WP_X_DIR ., not __DIR__ .) + ONE entry call; the bootstrap wires everything (component ::init() calls, table registration via private register_table(), WPStats init, API instantiation). Applies to wp-polls, wp-downloadmanager, wp-postviews (fold their file-scope calls into the bootstrap init()); downloadmanager + polls move file-scope $wpdb table registration into bootstrap register_table().
- uninstall.php for Install-owning plugins: full delegate (wp-polls moves its loop into WP_Polls_Install::uninstall() like postratings/useronline, keeping wp_polls source assertions in tests updated).
- Theme-override stylesheet lookup: the navi child→parent→plugin algorithm, applied to polls, downloadmanager, postratings (postratings' stylesheet_url helper adopts it; keep each plugin's documented filename). wp-email's documented removal stays.
- AJAX: front-end action names `polls`/`email` UNCHANGED (cache compat — add a one-line comment "Legacy action name: pages cached with the old script must keep posting somewhere." if absent). wp-sweep admin-only actions rename `sweep_count`/`sweep_totals`→`wp_sweep_count`/`wp_sweep_totals` (php+js+tests). Handler method names: `ajax_*` prefix (polls vote_poll→ajax_vote, manage_poll→ajax_manage; email process/serve→ajax_*; useronline ajax→ajax_refresh) — ACTION strings unchanged, only PHP method names. Nonce consts: `NONCE_ACTION`/`NONCE_FIELD` vocabulary (dff renames NONCE/NONCE_FIELD accordingly, email renames NONCE_NAME→NONCE_FIELD); useronline AJAX_NONCE shape (const + default _ajax_nonce field) adopted by postviews.
- action_links: every plugin with an admin page gets the 7-plugin `action_links` method + `plugin_action_links_` hook (add to: dbmanager, downloadmanager, email, polls, postratings, postviews, serverinfo, stats, sweep, useronline), linking its settings/first screen, docblock copied from wp-ban's.
- serverinfo hook arrays: string class names, not Foo::class.
- freemyinternet: activate() gains ( $network_wide = false ) + the standard get_sites loop + the 4-test test-multisite.php (pagenavi template).
- wp-polls comment modernization: every `// Function: …` banner deleted; every `@param mixed $x Value.` given its real type and sentence; bare `@return mixed` typed from the code. House voice, §2.8 concise.

## Canonical comment sentences (verbatim)
- number=>0: `// 'number' => 0 lifts WP_Site_Query's default cap of 100, which would otherwise skip every site past the hundredth while reporting success.`
- restore in loop: `// Inside the loop: switch_to_blog() pushes onto a stack, so restoring once after the loop unwinds it by exactly one.`
- activation-update (docblock line): `Activation does not fire on a plugin update, which is the single most common reason a migration never runs.`
- file-load registration: `// Must be registered at file-load time, which is when this runs.`
- unminified: `// Shipped unminified: it is small, and the review guidelines prefer readable sources.` (email + useronline converge)
- @param network: `@param bool $network_wide Whether the plugin is being activated network-wide.`

## Process rules
- git mv for renames; grep every old name repo-wide (code, tests, e2e specs, CLAUDE.md, README) and update.
- Behaviour-affecting items (upgrade hook, activation renames, theme-override algorithm, action_links, wiring reshapes) are covered by suites: bin/test.sh + bin/test-multisite.sh green per repo; bin/test-e2e.sh for polls, postratings, downloadmanager, email, sweep, useronline (AJAX/widget/wiring touched). phpcs clean. npm run lint:js + test:js where JS touched. wp-env stop after each repo. python3 ../bin/verify.py <slug> 0 failing (or ../../ from nested).
- Public API frozen: template-tags function names, filter/action HOOK names (except the sweep admin two), widget id_base, shortcode names, AJAX front-end action strings, option row names. If a canon rename collides with frozen API, keep the frozen name and note it.
- Commits per repo per theme (renames / wiring / comments / features), --no-gpg-sign, do NOT push, imperative house voice, body naming the majority joined, trailer exactly:
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CVrFykSreGPwV1hTiRdQBY
- Changelog: repos with staged versions (downloadmanager, dff, pagenavi, pluginsused, polls, postratings, postviews, sweep, useronline) add a bullet ONLY for user-visible changes (action_links line, upgrade-hook timing). Pure renames/comments get no bullet. Unstaged repos: no version changes.
