#!/usr/bin/env python3
"""
Check all nineteen plugins against _standards/STANDARDS.md.

This is the mechanical half of verification: everything that can be decided by
reading files rather than by judgement. It does not start Docker and does not
run PHPUnit -- bin/test-all.sh does that.

    python3 bin/verify.py              # every plugin
    python3 bin/verify.py wp-polls     # just one
    python3 bin/verify.py --quiet      # only failures

Exit status is the number of failing checks, capped at 250.
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# slug -> (display name, class prefix, port). Slug-alphabetical; ports two apart
# so port and testsPort can never collide. 8888/8889 are the all-plugins env.
PLUGINS = [
    ("freemyinternet", "FreeMyInternet", "FreeMyInternet", 8890),
    ("wp-ban", "WP-Ban", "WP_Ban", 8892),
    ("wp-commentnavi", "WP-CommentNavi", "WP_CommentNavi", 8894),
    ("wp-dbmanager", "WP-DBManager", "WP_DBManager", 8896),
    ("wp-downloadmanager", "WP-DownloadManager", "WP_DownloadManager", 8898),
    ("wp-draftsforfriends", "WP-DraftsForFriends", "WP_DraftsForFriends", 8900),
    ("wp-email", "WP-EMail", "WP_Email", 8902),
    ("wp-pagenavi", "WP-PageNavi", "WP_PageNavi", 8904),
    ("wp-pluginsused", "WP-PluginsUsed", "WP_PluginsUsed", 8906),
    ("wp-polls", "WP-Polls", "WP_Polls", 8908),
    ("wp-postratings", "WP-PostRatings", "WP_PostRatings", 8910),
    ("wp-postviews", "WP-PostViews", "WP_PostViews", 8912),
    ("wp-print", "WP-Print", "WP_Print", 8914),
    ("wp-relativedate", "WP-RelativeDate", "WP_RelativeDate", 8916),
    ("wp-serverinfo", "WP-ServerInfo", "WP_ServerInfo", 8918),
    ("wp-showhide", "WP-ShowHide", "WP_ShowHide", 8920),
    ("wp-stats", "WP-Stats", "WP_Stats", 8922),
    ("wp-sweep", "WP-Sweep", "WP_Sweep", 8924),
    ("wp-useronline", "WP-UserOnline", "WP_UserOnline", 8926),
]

# Version each plugin ships as, per STANDARDS.md §14. wp-dbmanager and
# wp-useronline differ from what the repo carried before this pass because
# their previous number is already live on wordpress.org.
# §2.1 plugins with no settings and no tables, which therefore store no option
# row at all -- not even the version markers. freemyinternet is deliberately not
# here: it has a settings screen, so it keeps both rows.
STORES_NOTHING = {"wp-relativedate", "wp-showhide", "wp-serverinfo", "wp-sweep"}

SHIPS_AS = {
    "freemyinternet": "1.0.0",
    "wp-ban": "2.0.0",
    "wp-commentnavi": "2.0.0",
    "wp-dbmanager": "4.0.0",
    "wp-downloadmanager": "2.0.0",
    "wp-draftsforfriends": "2.0.0",
    "wp-email": "3.0.0",
    "wp-pagenavi": "3.0.0",
    "wp-pluginsused": "2.0.0",
    "wp-polls": "3.0.0",
    "wp-postratings": "2.0.0",
    "wp-postviews": "2.0.0",
    "wp-print": "3.0.0",
    "wp-relativedate": "2.0.0",
    "wp-serverinfo": "3.0.0",
    "wp-showhide": "3.0.0",
    "wp-stats": "3.0.0",
    "wp-sweep": "2.0.0",
    "wp-useronline": "4.0.0",
}

README_FIELDS = [
    "Contributors:",
    "Donate link:",
    "Tags:",
    "Requires at least:",
    "Tested up to:",
    "Stable tag:",
    "Requires PHP:",
    "License:",
    "License URI:",
]

CANONICAL_SECTIONS = [
    "## Description",
    "## Usage",
    "## Frequently Asked Questions",
    "## Screenshots",
    "## Changelog",
    "## Upgrade Notice",
]

CHANGELOG_PREFIXES = ("BREAKING:", "NEW:", "CHANGED:", "FIXED:", "NOTE:")

# The year in the copyright line, kept apart from the block so that rolling it
# over is one edit rather than nineteen.
COPYRIGHT_YEAR = "2026"

# §3.1's GPL comment block, verbatim, tabs and all. Two spaces after the year,
# around "email :", and either side of the postal code -- those are the spacing
# the standard pins, and normalising them is why this is compared rather than
# pattern-matched.
#
# The address is the FSF's current one. Sixteen plugins carried
# "59 Temple Place, Suite 330, Boston, MA  02111-1307", which the FSF left in
# 2005 and which survives across the whole WordPress plugin directory purely by
# copy-and-paste; three carried "51 Franklin St", the right building with the
# street name abbreviated. This is the wording the FSF actually publishes with
# GPL-2.0 today. It is a postal address the block tells a reader to write to, so
# of the two ways to make nineteen files agree, only one of them is also true.
GPL_BLOCK = """/*
\tCopyright %s  Lester Chan  (email : lesterchan@gmail.com)

\tThis program is free software; you can redistribute it and/or modify
\tit under the terms of the GNU General Public License as published by
\tthe Free Software Foundation; either version 2 of the License, or
\t(at your option) any later version.

\tThis program is distributed in the hope that it will be useful,
\tbut WITHOUT ANY WARRANTY; without even the implied warranty of
\tMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
\tGNU General Public License for more details.

\tYou should have received a copy of the GNU General Public License
\talong with this program; if not, write to the Free Software
\tFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/"""


def gpl_block(source):
    """The /* ... */ licence block that follows the plugin header docblock."""
    m = re.search(r"^/\*\n\tCopyright .*?^\*/", source, re.M | re.S)

    return m.group(0) if m else None


def first_difference(got, want):
    """Where two blocks diverge, as a line number and both spellings.

    A byte-for-byte comparison that reports only "does not match" sends the
    reader to diff nineteen files by eye. Trailing whitespace and tab-versus-
    space are the likeliest causes and the hardest to see, so the differing
    line is quoted with its whitespace made visible.
    """
    def visible(text):
        return text.replace("\t", "\\t").replace(" ", "·")

    got_lines = got.split("\n")
    want_lines = want.split("\n")

    for i in range(max(len(got_lines), len(want_lines))):
        mine = got_lines[i] if i < len(got_lines) else "<end of block>"
        theirs = want_lines[i] if i < len(want_lines) else "<end of block>"

        if mine != theirs:
            return "line %d: %s != %s" % (i + 1, visible(mine), visible(theirs))

    return ""

# Files in includes/ whose names a theme copies verbatim to override them. The
# filename is public API, so it cannot be bent to the class-*.php convention.
THEME_TEMPLATES = {
    "wp-print": ("print-posts.php", "print-comments.php"),
}

SKIP_DIRS = {"vendor", "node_modules", ".git", ".idea", "tests", "artifacts"}

# §2.2's retired spellings. Every one of these was in use somewhere in the
# collection before the canonicalisation pass, and the section retires them by
# name in favour of OPTION / VERSION / GROUP / PAGE / CAPABILITY plus SECTION_*.
#
# DB_VERSION, SLUG and SECTION are on the list as *class* constants only --
# {{UPPER}}_DB_VERSION and {{UPPER}}_SLUG are §2.3 PHP defines and are required,
# and SECTION_<NAME> is what SECTION was retired in favour of. So this is
# matched against `const NAME =` and never against a bare identifier.
RETIRED_CONSTS = {
    "OPTION_NAME", "OPTION_GROUP", "PAGE_SLUG", "DB_VERSION_OPTION",
    "VERSION_OPTION", "DB_VERSION_NAME", "DB_VERSION", "SLUG", "SECTION",
    "VERSIONS_KEY", "HANDLE",
}


# §2.7's custom capabilities, one per plugin. Everything not named here gates on
# manage_options, and a plugin may never reach for a sibling's capability.
#
# §2.7 listed five of these and omitted two that ship -- wp-polls' manage_polls
# and wp-sweep's activate_plugins. Both were added to the section on 2026-08-04,
# so this map and §2.7 now agree; check them against each other before changing
# either.
#
# The name is a shade loose and worth reading carefully: only four of the seven
# are *custom*, in the sense that the plugin must add_cap() them into existence
# -- manage_downloads, manage_email, manage_polls and manage_ratings.
# install_plugins, activate_plugins and publish_posts are core's, held by every
# administrator already and nobody's to grant. §2.7 draws that line, and the
# add_cap() rule below depends on it.
CUSTOM_CAPABILITIES = {
    "wp-dbmanager": "install_plugins",
    "wp-downloadmanager": "manage_downloads",
    "wp-draftsforfriends": "publish_posts",
    "wp-email": "manage_email",
    "wp-polls": "manage_polls",
    "wp-postratings": "manage_ratings",
    "wp-sweep": "activate_plugins",
}


# §4.2.1 / §4.2.2: the tab strip of every plugin that has one, in order.
#
# §4.2.2 pins two of these labels by name -- they are `Settings` and `Templates`
# and nothing else -- and §4.2.1's table pins the data-screen tab of three
# plugins. The rest are pinned here for the same reason SHIPS_AS is: five of the
# six tabbed plugins disagreed with each other before §4.2.2 was written
# (`Poll Options`, `Poll Templates`, `General`), the renames were done by hand in
# six repositories, and a rename that stops at the tab strip sends the README and
# the e2e suite to a screen name that no longer exists.
#
# wp-serverinfo is in the table although its tabs are panels of one read-only
# report rather than §4.2.1 screens-turned-tabs. The section does not govern it;
# the drift it prevents is the same.
TAB_LABELS = {
    "wp-ban": ["Stats", "Settings", "Templates"],
    "wp-downloadmanager": ["Settings", "Templates"],
    "wp-draftsforfriends": ["Shared Drafts", "Settings"],
    "wp-email": ["Settings", "Templates"],
    "wp-polls": ["Settings", "Templates"],
    "wp-postratings": ["Settings", "Templates"],
    "wp-postviews": ["Settings", "Templates"],
    "wp-print": ["Settings", "Templates"],
    "wp-serverinfo": ["General", "PHP", "MySQL", "memcached", "Redis"],
    "wp-stats": ["Statistics", "Settings"],
    "wp-useronline": ["Users Online", "Settings", "Templates"],
}


# §13's seven: six contributors to the wp_stats_sections filter, plus wp-stats
# which owns it and reads none of their option rows.
WPSTATS_CONTRIBUTORS = {
    "wp-downloadmanager", "wp-email", "wp-polls", "wp-postratings",
    "wp-postviews", "wp-useronline",
}


def class_constants(root, includes):
    """Every `const NAME = '<literal>';` in shipped PHP, as (name, value, file).

    Shipped code only, by allow list -- the root entry points plus includes/ --
    for the same reason the §7.6.1 check uses one: a test may legitimately
    define a constant of its own, and a deny list acquires a new member every
    time somebody installs something.

    Only string literals are collected. A constant whose value is an array or an
    expression (PROXY_HEADERS, COLORS_BUILTIN) has no single spelling to compare
    and is not what §2.2 is about.
    """
    found = []
    files = [os.path.join(root, e) for e in sorted(os.listdir(root))
             if e.endswith(".php")]
    if os.path.isdir(includes):
        files += [os.path.join(includes, e)
                  for e in sorted(os.listdir(includes)) if e.endswith(".php")]

    for path in files:
        body = read(path) or ""
        # Strip comments first, as the §4.2 and §7.6.1 checks do: §2.2's own
        # retired names are quoted in the docblocks explaining the rename.
        body = re.sub(r"/\*.*?\*/|//[^\n]*|^\s*\*[^\n]*$", "", body,
                      flags=re.S | re.M)
        for m in re.finditer(
                r"\bconst\s+([A-Z][A-Z0-9_]*)\s*=\s*'([^']*)'\s*;", body):
            found.append((m.group(1), m.group(2), os.path.relpath(path, root)))
        # A constant with a non-string value still has a name to check.
        for m in re.finditer(r"\bconst\s+([A-Z][A-Z0-9_]*)\s*=\s*(?!')", body):
            found.append((m.group(1), None, os.path.relpath(path, root)))

    return [(n, v, w) for n, v, w in found if v is not None or n in RETIRED_CONSTS]


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return None


def walk(base):
    """Every file under base, skipping dependency and VCS trees."""
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield os.path.join(dirpath, name)


class Report:
    def __init__(self, slug):
        self.slug = slug
        self.failures = []

    def check(self, ok, label, detail=""):
        if not ok:
            self.failures.append((label, detail))


def verify(slug, name, prefix, port, root):
    r = Report(slug)
    under = slug.replace("-", "_")
    upper = under.upper()
    main = os.path.join(root, slug + ".php")

    # --- §3.2 README header -------------------------------------------------
    readme = read(os.path.join(root, "README.md"))
    if readme is None:
        r.check(False, "README.md missing")
    else:
        lines = readme.split("\n")
        header = []
        for line in lines[1:]:
            if line.strip() == "":
                break
            header.append(line)

        r.check(len(header) == 9, "README header field count",
                "expected 9, found %d" % len(header))

        for i, line in enumerate(header[:-1]):
            r.check(line.endswith("  "), "README header line break",
                    "%r needs two trailing spaces" % line.strip())
        if header:
            last = header[-1]
            r.check(last == last.rstrip(), "README last header line",
                    "%r must not have trailing spaces" % last.strip())

        for i, field in enumerate(README_FIELDS):
            if i < len(header):
                r.check(header[i].strip().startswith(field),
                        "README field order",
                        "line %d should start %r, got %r"
                        % (i + 2, field, header[i].strip()[:40]))

        contributors = re.search(r"^Contributors:\s*(.+?)\s*$", readme, re.M)
        r.check(contributors is not None
                and contributors.group(1).strip() == "GamerZ",
                "README Contributors is GamerZ only",
                contributors.group(1).strip() if contributors else "missing")

        stable = re.search(r"^Stable tag:\s*(\S+)", readme, re.M)
        r.check(stable is not None and stable.group(1) == SHIPS_AS[slug],
                "README Stable tag matches §14",
                "%s (want %s)" % (stable.group(1) if stable else "?",
                                  SHIPS_AS[slug]))

        # §3.3: the h2 set is closed and ordered. h3s are free.
        found_h2 = [ln.rstrip() for ln in lines if ln.startswith("## ")]
        for section in ("## Description", "## Changelog", "## Upgrade Notice"):
            r.check(section in found_h2, "README section present", section)

        unexpected = [h for h in found_h2 if h not in CANONICAL_SECTIONS]
        for h in unexpected:
            r.check(False, "README has a non-canonical h2", h)

        ordered = [h for h in found_h2 if h in CANONICAL_SECTIONS]
        expected_order = [h for h in CANONICAL_SECTIONS if h in ordered]
        r.check(ordered == expected_order, "README h2 order matches §3.3",
                " / ".join(ordered))

        # Changelog bullets use the five allowed prefixes.
        in_changelog = False
        for line in lines:
            if line.startswith("## Changelog"):
                in_changelog = True
                continue
            if in_changelog and line.startswith("## "):
                break
            if in_changelog and line.startswith("* "):
                body = line[2:]
                r.check(body.startswith(CHANGELOG_PREFIXES),
                        "changelog bullet prefix", body[:60])

    # --- §3.1 plugin header -------------------------------------------------
    head = read(main)
    if head is None:
        r.check(False, "main plugin file missing", slug + ".php")
    else:
        def header_field(field):
            m = re.search(r"^\s*\*\s*%s\s*(.+?)\s*$" % re.escape(field),
                          head, re.M)
            return m.group(1) if m else None

        r.check(header_field("Plugin Name:") == name, "header Plugin Name",
                str(header_field("Plugin Name:")))
        r.check(header_field("Version:") == SHIPS_AS[slug], "header Version",
                "%s (want %s)" % (header_field("Version:"), SHIPS_AS[slug]))
        r.check(header_field("Text Domain:") == slug, "header Text Domain",
                str(header_field("Text Domain:")))
        r.check(header_field("Domain Path:") == "/languages",
                "header Domain Path", str(header_field("Domain Path:")))
        r.check(header_field("Requires at least:") == "6.8",
                "header Requires at least")
        r.check(header_field("Requires PHP:") == "8.2", "header Requires PHP")
        r.check(header_field("License:") == "GPLv2 or later", "header License")
        r.check(header_field("License URI:")
                == "https://www.gnu.org/licenses/gpl-2.0.html",
                "header License URI")

        # §3.1 the GPL block itself, byte for byte. Checking only the header
        # field above is what let one plugin ship the v2-ONLY wording under a
        # "GPLv2 or later" header for as long as it did, and let the FSF's
        # postal address drift into two spellings across the nineteen. Neither
        # was visible to phpcs, to the header check, or to reading one file.
        block = gpl_block(head)

        if block is None:
            r.check(False, "GPL comment block missing (§3.1)")
        else:
            r.check("either version 2 of the License, or" in block
                    and "(at your option) any later version." in block,
                    "GPL block is the 'or later' variant (§3.1)")
            r.check(block == GPL_BLOCK % COPYRIGHT_YEAR,
                    "GPL block matches §3.1 verbatim",
                    first_difference(block, GPL_BLOCK % COPYRIGHT_YEAR))

        # §2.3 the constants. DB_VERSION only where there is a schema to count:
        # a plugin with no settings and no tables stores nothing at all (§2.1),
        # so it has no row for a schema counter to describe.
        consts = ["VERSION", "SLUG", "MAIN_FILE", "DIR", "URL"]

        if slug not in STORES_NOTHING:
            consts.insert(1, "DB_VERSION")

        for const in consts:
            r.check("%s_%s" % (upper, const) in head,
                    "constant defined", "%s_%s" % (upper, const))

        if slug in STORES_NOTHING:
            r.check("%s_DB_VERSION" % upper not in head,
                    "no DB_VERSION for a plugin that stores nothing (§2.1)")

        m = re.search(r"define\(\s*'%s_VERSION',\s*'([^']+)'" % upper, head)
        r.check(m is not None and m.group(1) == SHIPS_AS[slug],
                "%s_VERSION matches §14" % upper,
                m.group(1) if m else "not found")

    # --- §10 wp-env ---------------------------------------------------------
    env = read(os.path.join(root, ".wp-env.json"))
    if env is None:
        r.check(False, ".wp-env.json missing")
    else:
        r.check('"port": %d' % port in env, "wp-env port", "want %d" % port)
        r.check('"testsPort": %d' % (port + 1) in env, "wp-env testsPort",
                "want %d" % (port + 1))
        r.check("schemas.wp.org" in env, "wp-env $schema present")
        r.check('"WP_DEBUG": true' in env, "wp-env WP_DEBUG")

    r.check(not os.path.exists(os.path.join(root, ".wp-env.override.json")),
            ".wp-env.override.json deleted")
    r.check(not os.path.isdir(os.path.join(root, ".idea")), ".idea deleted")

    gitignore = read(os.path.join(root, ".gitignore")) or ""
    for entry in ("vendor/", "node_modules/", ".idea/",
                  ".wp-env.override.json", ".phpunit.result.cache"):
        r.check(entry in gitignore, ".gitignore entry", entry)

    # --- §1 layout ----------------------------------------------------------
    for required in ("index.php", "uninstall.php", "LICENSE", "phpcs.xml",
                     "phpunit.xml.dist", "phpunit-multisite.xml.dist",
                     ".editorconfig", "composer.json", "README.md"):
        r.check(os.path.exists(os.path.join(root, required)),
                "required file", required)

    allowed_root_php = {slug + ".php", "index.php", "uninstall.php"}
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if not os.path.isfile(full):
            continue
        if entry.endswith(".php") and entry not in allowed_root_php:
            r.check(False, "loose root PHP file", entry)
        # A tool's own config file belongs beside the tool's config files, not
        # in js/ -- that directory ships to users, and eslint and Playwright
        # both look for theirs at the project root by convention.
        if (entry.endswith(".js")
                and not entry.endswith(".config.mjs")
                and not entry.endswith(".config.js")):
            r.check(False, "loose root JS file", entry)
        if entry.endswith(".css"):
            r.check(False, "loose root CSS file", entry)

    # index.php in every shipped directory. tests/ is in SKIP_DIRS for the
    # content scans but §1 still requires an index.php there, so it is walked
    # explicitly rather than skipped.
    # artifacts/ is a Playwright output directory: gitignored, never shipped,
    # and recreated on every failing run, so an index.php in it would be a file
    # nobody wrote asking to be kept.
    walk_skip = (SKIP_DIRS - {"tests"}) | {"artifacts"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in walk_skip and not d.startswith(".")]
        rel = os.path.relpath(dirpath, root)
        if rel == ".":
            continue
        r.check("index.php" in filenames, "index.php in directory", rel)

    # --- §5.1 no RTL sheet --------------------------------------------------
    for path in walk(root):
        if path.endswith("-rtl.css"):
            r.check(False, "RTL stylesheet must be folded in",
                    os.path.relpath(path, root))

    # --- §6 no jQuery -------------------------------------------------------
    for path in walk(root):
        if not path.endswith((".php", ".js")):
            continue
        body = read(path) or ""
        # Strip comments first: four plugins had to reword prose that merely
        # mentioned the old library. Match code, not English.
        code = re.sub(r"/\*.*?\*/|//[^\n]*|^\s*\*[^\n]*$", "", body,
                      flags=re.S | re.M)
        if re.search(r"\bjQuery\b|['\"]jquery['\"]", code):
            r.check(False, "jQuery reference",
                    os.path.relpath(path, root))

    # --- §2.4 classes and file names ---------------------------------------
    includes = os.path.join(root, "includes")
    if os.path.isdir(includes):
        for entry in sorted(os.listdir(includes)):
            if not entry.endswith(".php") or entry == "index.php":
                continue
            if entry in ("deprecated.php", "template-tags.php", "bots.php"):
                continue
            # §1 sanctions screen-*.php partials alongside class-*.php.
            if entry.startswith("screen-"):
                continue
            # Theme-overridable templates keep the exact filename a theme must
            # use to override them -- the name is public API, so renaming it to
            # class-* or screen-* would break every existing override.
            if entry in THEME_TEMPLATES.get(slug, ()):
                continue
            r.check(entry.startswith("class-"), "includes file naming", entry)

            body = read(os.path.join(includes, entry)) or ""
            for cls in re.findall(r"^\s*(?:final\s+|abstract\s+)?class\s+(\w+)",
                                  body, re.M):
                r.check(cls.startswith(prefix), "class prefix",
                        "%s in %s (want %s_*)" % (cls, entry, prefix))
                expect = "class-" + cls.lower().replace("_", "-") + ".php"
                r.check(entry == expect, "class file name",
                        "%s declares %s, expected %s" % (entry, cls, expect))

    # --- §2.6 hook prefixes -------------------------------------------------
    hook_prefix = under + "_"
    # Hooks the plugin CONSUMES from core, which it does not own and must not
    # rename. 'the_views' was wrongly here: it is wp-postviews' own filter, and
    # §2.6 requires renaming it, so allowlisting it made the check blind to the
    # one case it was written for.
    core_hooks = {
        "the_content", "comment_text", "widget_title", "rss2_head",
        "rss_update_period", "rss_update_frequency",
    }
    for path in walk(root):
        if not path.endswith(".php"):
            continue
        body = read(path) or ""
        for hook in re.findall(
                r"(?:apply_filters|do_action)(?:_ref_array)?\(\s*'([a-z0-9_]+)'",
                body):
            if hook in core_hooks:
                continue
            # A hook may also be named exactly after the plugin -- wp_pagenavi
            # and wp_commentnavi are each their plugin's oldest documented
            # filter, and neither can carry a trailing underscore.
            ok = hook.startswith(hook_prefix) or hook == under
            r.check(ok, "hook prefix",
                    "%s in %s (want %s* or %s)"
                    % (hook, os.path.relpath(path, root), hook_prefix, under))

    # --- §2.1 option rows ---------------------------------------------------
    all_php = "\n".join(read(p) or "" for p in walk(root) if p.endswith(".php"))
    # A row the plugin also deletes is one it is migrating away from, and §2.1
    # *requires* the migration to read it before folding it in. So collect the
    # deleted names first and exempt them: only an unprefixed row that is read
    # or written WITHOUT being cleaned up is a violation. Without this, every
    # correct migration fails the check.
    migrated = set(re.findall(r"delete_option\(\s*'([a-z0-9_]+)'", all_php))
    legacy = [
        opt for opt in re.findall(
            r"(?:get_option|update_option|add_option)\(\s*'([a-z0-9_]+)'",
            all_php)
        if opt not in migrated
    ]
    core_options = {
        "home", "siteurl", "blogname", "blog_charset", "date_format",
        "time_format", "gmt_offset", "admin_email", "permalink_structure",
        "page_on_front", "show_on_front", "active_plugins", "users_can_register",
    }
    for opt in sorted(set(legacy)):
        if opt in core_options or opt.startswith(under + "_"):
            continue
        r.check(False, "unprefixed option row", opt)

    # --- §4.2 the Settings class owns the fields ----------------------------
    # Admin owns the menu and the screens; Settings owns register_setting(), the
    # sections, the field_<name>() callbacks and the sanitiser. wp-print and
    # wp-pagenavi both drifted to putting fields on Admin, which nothing caught.
    if os.path.isdir(includes):
        for entry in sorted(os.listdir(includes)):
            if not entry.endswith(".php"):
                continue
            body = read(os.path.join(includes, entry)) or ""
            # Strip comments first, or a docblock explaining why the Settings
            # API calls were removed reads as the calls themselves. Same reason
            # the jQuery check does it: match code, not English.
            body = re.sub(r"/\*.*?\*/|//[^\n]*|^\s*\*[^\n]*$", "", body,
                          flags=re.S | re.M)
            if "add_settings_field(" not in body:
                continue
            r.check(entry.endswith("-settings.php"),
                    "add_settings_field() belongs on the Settings class",
                    "%s (§4.2)" % entry)

    # --- §7 tests -----------------------------------------------------------
    tests = os.path.join(root, "tests")
    if not os.path.isdir(tests):
        r.check(False, "tests/ missing")
    else:
        # §7.1: every PHP file under tests/ is a test-, a helper-, or one of the
        # two named files. Walked rather than listed, because tests/e2e/ and
        # tests/js/ each carry an index.php and a suite that predates this rule
        # could put a testcase in a subdirectory where nothing would look.
        # tests/e2e/mu-plugins is out of scope: WordPress loads whatever is in
        # a mu-plugins directory by filename, and §7.5's theme shims live there
        # because that is where the wp-env mapping points. Requiring them to be
        # test-*.php would be the §7.2.1 mistake -- a rule written before e2e
        # existed firing on e2e scaffolding -- with the file moved rather than
        # the rule widened.
        for dirpath, dirnames, filenames in os.walk(tests):
            dirnames[:] = [d for d in dirnames
                           if d not in SKIP_DIRS and d != "mu-plugins"]
            for entry in sorted(filenames):
                if not entry.endswith(".php"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, entry), root)
                ok = (entry.startswith("test-") or entry.startswith("helper-")
                      or entry in ("bootstrap.php", "index.php"))
                r.check(ok, "tests file naming", rel)
        r.check(os.path.exists(os.path.join(tests, "test-metadata.php")),
                "tests/test-metadata.php present")
        r.check(not os.path.exists(os.path.join(tests, "phpunit-multisite.xml")),
                "stray tests/phpunit-multisite.xml removed")

        # §7.1: one class per file, named {{CLASS}}_<Area>_Test, extending
        # {{CLASS}}_TestCase. Both halves matter and both had drifted in one
        # file: wp-polls' schema migration tests were `Test_Migration_Schema
        # extends WP_UnitTestCase`, which is the naming of no other file in the
        # collection and skips the plugin's own fixture reset.
        #
        # The base is checked as "a {{CLASS}}_*TestCase" rather than literally
        # {{CLASS}}_TestCase, because an AJAX suite cannot inherit from it --
        # only WP_Ajax_UnitTestCase installs the handler that turns the
        # endpoint's wp_send_json_*() into a catchable exception. wp-email and
        # wp-sweep both answer that with a second plugin-owned base beside the
        # first, which is the shape §7.1 wants and does not currently mention.
        r.check(os.path.exists(os.path.join(tests, "helper-testcase.php")),
                "§7.1 tests/helper-testcase.php present")

        for entry in sorted(os.listdir(tests)):
            if not entry.startswith("test-") or not entry.endswith(".php"):
                continue
            body = read(os.path.join(tests, entry)) or ""
            declared = re.findall(
                r"^\s*(?:final\s+|abstract\s+)?class\s+(\w+)"
                r"(?:\s+extends\s+(\w+))?", body, re.M)

            r.check(len(declared) == 1, "§7.1 one class per test file",
                    "tests/%s declares %d" % (entry, len(declared)))

            for cls, parent in declared:
                r.check(re.match(r"^%s_\w+_Test$" % re.escape(prefix), cls),
                        "§7.1 test class name",
                        "%s in tests/%s, want %s_<Area>_Test"
                        % (cls, entry, prefix))
                # Plugin_Metadata_TestCase is the shared metadata fixture,
                # byte-identical in all nineteen and deliberately naming no
                # plugin -- it reaches the plugin's own base through a
                # class_alias set in bootstrap.php. Its own check is the
                # template comparison above.
                r.check(parent == "Plugin_Metadata_TestCase"
                        or (parent is not None
                            and parent.startswith(prefix + "_")
                            and parent.endswith("TestCase")),
                        "§7.1 test class extends the plugin's own test case",
                        "%s in tests/%s extends %s, want %s_TestCase"
                        % (cls, entry, parent or "nothing", prefix))

    # --- §8 CI --------------------------------------------------------------
    ci = read(os.path.join(root, ".github", "workflows", "ci.yml"))
    if ci is None:
        r.check(False, ".github/workflows/ci.yml missing")
    else:
        r.check("actions/checkout@v7" in ci, "CI checkout@v7")
        r.check("shivammathur/setup-php@v2" in ci, "CI setup-php@v2")
        r.check("concurrency:" in ci, "CI concurrency block")
        r.check("permissions:" in ci, "CI permissions block")
        r.check(ci.count("- php:") == 6, "CI matrix has 6 rows",
                "found %d" % ci.count("- php:"))
        r.check("'8.5'" in ci, "CI tests PHP 8.5")
        r.check(ci.count("multisite: true") == 3, "CI has 3 multisite rows",
                "found %d" % ci.count("multisite: true"))
        r.check("wp-content/plugins/%s" % slug in ci, "CI env-cwd slug")

    # --- §8 ci.yml matches the template ------------------------------------
    # Same reasoning as phpcs.xml: the workflow is meant to be identical in all
    # nineteen. A no-JS plugin legitimately drops the whole eslint job, so the
    # comparison ignores that block.
    tpl_ci = read(os.path.join(ROOT, "_standards", "templates",
                               ".github", "workflows", "ci.yml"))
    if ci and tpl_ci:
        # A job whose subject a plugin does not have is dropped from both sides
        # rather than required of it: there is no eslint job without js/, and no
        # Playwright job without tests/e2e. Everything else has to match.
        # Anchored on whichever job comes next rather than on one name: the
        # template gained a job between eslint and phpunit, and an anchor naming
        # phpunit stopped matching the plugins whose eslint job still runs
        # straight into it.
        jobs = "phpcs|eslint|e2e|phpunit"

        def _drop(name, text):
            return re.sub(r"\n  %s:.*?(?=\n  (?:%s):)" % (name, jobs), "",
                          text, flags=re.S)

        # Lintable JavaScript is not only js/. The Playwright specs are
        # JavaScript too, and a plugin whose only scripts are those still needs
        # the linting job -- assuming otherwise is how five repositories shipped
        # e2e specs that nothing had ever linted, and how three others carried a
        # job that died at setup-node because they have no package.json at all.
        has_js = (os.path.isdir(os.path.join(root, "js"))
                  or os.path.isdir(os.path.join(root, "tests", "e2e")))

        def _norm(text):
            text = text.replace("{{SLUG}}", slug)
            if not has_js:
                text = _drop("eslint", text)
            if not os.path.isdir(os.path.join(root, "tests", "e2e")):
                text = _drop("e2e", text)
            return re.sub(r"\s+", " ", text).strip()

        r.check(_norm(ci) == _norm(tpl_ci),
                "ci.yml matches the shared template",
                "differs from _standards/templates (§8)")

    # --- §2.7 the capability granted is the capability checked --------------
    # Four plugins create a capability of their own -- wp-downloadmanager,
    # wp-email, wp-polls, wp-postratings -- and every screen gates on the
    # FILTERED value, {{UNDER}}_capability applied to the constant. Granting the
    # constant, or its literal string, while checking the filtered one means a
    # site that uses the filter hands its administrator a capability nothing
    # looks at and gates every screen on one nobody holds. The owner is locked
    # out of their own plugin and no log says why. Three of the four had it on
    # 2026-08-04; only wp-postratings did not.
    #
    # A literal that is NOT the plugin's current capability is deliberately
    # allowed: wp-dbmanager removes 'manage_database', the capability it retired
    # in 2.80.6, and there is no accessor for a capability that no longer
    # exists. Only the current one has to go through the filter.
    cap_files = [os.path.join(root, e) for e in sorted(os.listdir(root))
                 if e.endswith(".php")]
    if os.path.isdir(includes):
        cap_files += [os.path.join(includes, e)
                      for e in sorted(os.listdir(includes))
                      if e.endswith(".php")]
    current_caps = set(
        re.findall(r"const CAPABILITY\s*=\s*'([a-z_]+)'",
                   "\n".join(read(p) or "" for p in cap_files)))
    for path in cap_files:
        body = re.sub(r"/\*.*?\*/|//[^\n]*|^\s*\*[^\n]*$", "", read(path) or "",
                      flags=re.S | re.M)
        for m in re.finditer(r"(?:add_cap|remove_cap)\(\s*([^;)]+?)\s*\)", body):
            arg = m.group(1).strip()
            literal = re.fullmatch(r"'([a-z_]+)'", arg)
            # The filtered accessor is the only correct spelling; a constant is
            # the bug, and a literal is the bug only when it names the
            # capability this plugin currently checks.
            bad = arg.endswith("::CAPABILITY") or (
                literal is not None and literal.group(1) in current_caps)
            if bad:
                r.check(False,
                        "§2.7 the granted capability goes through the filter",
                        "%s at %s:%d, want %s::capability()"
                        % (arg, os.path.relpath(path, root),
                           body.count("\n", 0, m.start()) + 1, prefix + "_Admin"))

    # --- the metadata fixture is one file, not nineteen --------------------
    # This started as four different implementations of the same walk, so
    # excluding one directory took four edits and the hardcoded-list variant
    # silently passed for any directory nobody had added to it. They were
    # collapsed onto the template, and this is what keeps them there: the file
    # is deliberately identical in all nineteen -- it reaches the plugin's own
    # fixture base class through the Plugin_TestCase alias precisely so that it
    # never has to name a plugin -- so any difference at all is drift.
    tpl_meta = read(os.path.join(ROOT, "_standards", "templates",
                                 "helper-metadata-testcase.php"))
    meta = read(os.path.join(root, "tests", "helper-metadata-testcase.php"))
    if tpl_meta and meta:
        r.check(meta == tpl_meta,
                "helper-metadata-testcase.php matches the shared template",
                "differs from _standards/templates; this file carries no "
                "per-plugin text, so edit the template and copy it out")

    # --- @package is the display name, everywhere ---------------------------
    # Voice, and the sort verify.py can actually see. Two plugins had drifted:
    # wp-useronline and wp-postratings carried the lowercase slug through
    # includes/ while every newer file -- tests, bin, js, css -- used the
    # display name, so the older half of each plugin was tagged one way and the
    # newer half another. Nothing compared them, so it survived the whole
    # canonicalisation pass.
    #
    # `lesterchan` is exempt: it is the shared metadata fixture, which is
    # byte-identical in all nineteen and therefore names no plugin.
    wrong = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS or d == "tests"]
        for fn in filenames:
            if not fn.endswith(".php"):
                continue
            body = read(os.path.join(dirpath, fn)) or ""
            for tag in re.findall(r"@package\s+(\S+)", body):
                if tag not in (name, "lesterchan"):
                    rel = os.path.relpath(os.path.join(dirpath, fn), root)
                    wrong.append("%s: @package %s" % (rel, tag))
    r.check(not wrong, "@package is the plugin display name everywhere",
            "; ".join(wrong[:3]) + (" (+%d more)" % (len(wrong) - 3) if len(wrong) > 3 else ""))

    # --- §12 the package.json script set ------------------------------------
    # Derived from what the plugin has rather than listed, which is the whole
    # point: §12 named five scripts and no E2E entry until 2026-08-03, because
    # the Playwright work added two and nothing compared the result. All
    # nineteen diverged from the spec identically and in silence.
    pkg_raw = read(os.path.join(root, "package.json"))
    if pkg_raw:
        try:
            scripts = set(json.loads(pkg_raw).get("scripts", {}))
        except ValueError:
            scripts = None
            r.check(False, "package.json parses")

        if scripts is not None:
            expected = {"lint:js", "lint:js:fix", "test"}

            if os.path.isdir(os.path.join(root, "tests", "e2e")):
                expected |= {"test:e2e", "test:e2e:headed"}

            # A test:js pointing at a runner with nothing to run is a green
            # result that means nothing, so it is owed only with a suite.
            if os.path.isdir(os.path.join(root, "tests", "js")):
                expected |= {"test:js", "test:js:watch"}

            missing = sorted(expected - scripts)
            extra = sorted(scripts - expected)
            detail = []
            if missing:
                detail.append("missing " + ", ".join(missing))
            if extra:
                detail.append("unexpected " + ", ".join(extra))

            r.check(not missing and not extra,
                    "§12 package.json scripts match what the plugin has",
                    "; ".join(detail))

    # --- §3.3 one spelling for an admin path --------------------------------
    # A menu path is prose the reader retypes, so it is worth having exactly
    # one shape for it. Two drifted independently and nothing compared them:
    # four plugins wrote the separator as a Unicode arrow while fourteen wrote
    # "->" (wp-serverinfo used the arrow throughout, wp-polls, wp-postviews and
    # wp-sweep mixed both inside one file), and wp-print left four paths
    # unmarked while every other plugin sets them in code or bold. Neither is a
    # judgement call about voice; both are one spelling of one thing.
    readme = read(os.path.join(root, "README.md")) or ""
    arrows = [n for n, line in enumerate(readme.split("\n"), 1) if "→" in line]
    r.check(not arrows, "§3.3 admin paths use -> rather than a Unicode arrow",
            ", ".join("README.md:%d" % n for n in arrows[:3])
            + (" (+%d more)" % (len(arrows) - 3) if len(arrows) > 3 else ""))

    # Backticks or bold, so the path is not mistaken for prose. Anything inside
    # a fenced block is already marked up and is skipped.
    bare, fenced = [], False
    for n, line in enumerate(readme.split("\n"), 1):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if re.search(r"(?:^|[^`*])WP-Admin\s*->", line):
            bare.append(n)
    r.check(not bare, "§3.3 admin paths are in backticks or bold",
            ", ".join("README.md:%d" % n for n in bare[:3])
            + (" (+%d more)" % (len(bare) - 3) if len(bare) > 3 else ""))

    # --- §7.2.2 administrators come from the helper -------------------------
    # §7.2.2 asks that every administrator a suite creates go through one
    # helper, so the question "what does this capability mean on a network"
    # is answered once per plugin rather than once per call site. Nothing
    # checked it, and the section's own count of who complied was wrong for a
    # fortnight -- it named eleven plugins and 55 call sites when the truth was
    # eleven and 52, and called a plugin non-compliant that had a helper. A
    # figure nothing measures is a figure that rots.
    #
    # helper-*.php is where the helper lives, so it is the one place the
    # factory may be reached for an administrator directly. Subscriber and
    # editor fixtures are untouched: those assert the unprivileged path and
    # §7.2.2 says explicitly they must not be routed through the helper.
    inline = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(root, "tests")):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if not fn.endswith(".php") or fn.startswith("helper-"):
                continue
            body = read(os.path.join(dirpath, fn)) or ""
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            for m in re.finditer(r"->user->create(?:_and_get)?\s*\(", body):
                # The statement, not a fixed window: an administrator created
                # across three lines is the same finding as one on a single
                # line, and a `role` on the *next* statement is not.
                if "administrator" in body[m.end():].split(";")[0]:
                    inline.append("%s:%d"
                                  % (rel, body.count("\n", 0, m.start()) + 1))
    r.check(not inline,
            "§7.2.2 administrators are created through create_admin()",
            ", ".join(inline[:3])
            + (" (+%d more)" % (len(inline) - 3) if len(inline) > 3 else ""))

    # --- §7.6.1 the settings row is never read bare -------------------------
    # register_setting() is passed a `default` in most of the collection, and
    # that installs a default_option_{$option} filter which answers get_option()
    # with the shipped defaults for a row that does not exist. So a one-argument
    # read cannot tell an absent row from a defaulted one -- and a migration
    # that guards its fold-in on `is_array()` therefore skips it, on the one
    # path a real update takes, while deleting the legacy row it read anyway.
    #
    # Latent or live depends only on hook order, which is not a thing to rely
    # on: wp-dbmanager avoided the data loss purely because maybe_upgrade() ran
    # on plugins_loaded and register_setting() on admin_init, and moving the
    # call to where five siblings put theirs would have armed it.
    #
    # The legacy row is deliberately not covered. register_setting() names the
    # *current* row, so no default_option filter exists for the old one and a
    # bare read of it is correct -- which is what five plugins do.
    #
    # Shipped code only, by allow list rather than deny list: tests read the row
    # bare on purpose, to assert what is actually in the database.
    bare = []
    shipped = [os.path.join(root, e) for e in sorted(os.listdir(root))
               if e.endswith(".php")]
    if os.path.isdir(includes):
        shipped += [os.path.join(includes, e)
                    for e in sorted(os.listdir(includes)) if e.endswith(".php")]
    for path in shipped:
        body = read(path) or ""
        # Strip comments first, exactly as the §4.2 check does: this section is
        # explained at length in the very docblocks that sit above the code it
        # is about, and prose describing the trap must not read as the trap.
        body = re.sub(r"/\*.*?\*/|//[^\n]*|^\s*\*[^\n]*$", "", body,
                      flags=re.S | re.M)
        for m in re.finditer(
                r"get_option\(\s*(?:self|[A-Za-z_][A-Za-z0-9_]*)::OPTION\s*\)",
                body):
            bare.append("%s:%d" % (os.path.relpath(path, root),
                                   body.count("\n", 0, m.start()) + 1))
    r.check(not bare,
            "§7.6.1 the settings row is read with an explicit default",
            ", ".join(bare))

    # --- §11 ships no raster image -----------------------------------------
    # Satisfied everywhere and enforced nowhere until 2026-08-03: §11 replaced
    # every GIF and PNG in the collection with inline SVG, and nothing compared
    # the result, so the next one added would have shipped. The rule is about
    # what reaches a user, so tests/ and the E2E fixtures are out of scope --
    # only what the deploy would carry.
    rasters = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.lower().endswith((".png", ".gif", ".jpg", ".jpeg", ".bmp", ".ico")):
                rasters.append(os.path.relpath(os.path.join(dirpath, fn), root))

    r.check(not rasters, "§11 ships no raster image",
            "; ".join(rasters[:3]) + (" (+%d more)" % (len(rasters) - 3) if len(rasters) > 3 else ""))

    # --- the session-start hook is one file, not twenty --------------------
    # It installs the toolchain CI gates on -- Node 24, phpcs, npm ci -- and
    # names no plugin, branching on what it finds instead. Same reasoning as
    # the metadata fixture above: anything copied into twenty repositories
    # diverges unless something compares it.
    for rel in (os.path.join(".claude", "hooks", "session-start.sh"),
                os.path.join(".claude", "settings.json")):
        tpl_hook = read(os.path.join(ROOT, "_standards", "templates", rel))
        hook = read(os.path.join(root, rel))

        if tpl_hook is None:
            continue

        r.check(hook is not None, "%s exists" % rel,
                "copy it out of _standards/templates")

        if hook is not None:
            r.check(hook == tpl_hook, "%s matches the shared template" % rel,
                    "differs from _standards/templates; this file carries no "
                    "per-plugin text, so edit the template and copy it out")

    # --- §7.4 phpunit configs ----------------------------------------------
    for cfg, marker in (("phpunit.xml.dist", None),
                        ("phpunit-multisite.xml.dist", 'name="WP_MULTISITE"')):
        body = read(os.path.join(root, cfg))
        if body is None:
            continue
        r.check('prefix="test-"' in body, "%s discovers by test- prefix" % cfg)
        # Strip XML comments first: the template's own comment explains that no
        # <exclude> entries are needed, and matching that text flagged every
        # correct config as broken.
        uncommented = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        r.check("<exclude>" not in uncommented,
                "%s has no <exclude> entries" % cfg)
        r.check("<coverage>" in body, "%s has coverage block" % cfg)
        if marker:
            r.check(marker in body, "%s sets WP_MULTISITE" % cfg)

    # --- XML configs must actually parse ------------------------------------
    # A '--' inside an XML comment is illegal, and phpcs responds by refusing to
    # run at all rather than warning. That shipped in the shared template once
    # and would have broken every agent that copied it, so it is checked here.
    import xml.dom.minidom
    for cfg in ("phpcs.xml", "phpunit.xml.dist", "phpunit-multisite.xml.dist"):
        full = os.path.join(root, cfg)
        if not os.path.exists(full):
            continue
        try:
            xml.dom.minidom.parse(full)
        except Exception as exc:  # noqa: BLE001 - any parse failure is fatal
            r.check(False, "%s is not valid XML" % cfg, str(exc))

    # --- §9 phpcs -----------------------------------------------------------
    phpcs = read(os.path.join(root, "phpcs.xml")) or ""
    # The value may be a comma-separated list: a plugin that deliberately reuses
    # core's translated strings sets "<slug>,default", which does not weaken the
    # sniff -- it still rejects any third domain.
    tpl_phpcs = read(os.path.join(ROOT, "_standards", "templates", "phpcs.xml"))
    if tpl_phpcs and phpcs:
        def _norm(t):
            t = t.replace(name, "{{NAME}}").replace(slug, "{{SLUG}}")
            # a deliberately widened text_domain list is allowed to differ
            t = t.replace('value="{{SLUG}},default"', 'value="{{SLUG}}"')
            return re.sub(r"\s+", " ", t).strip()
        r.check(_norm(phpcs) == _norm(tpl_phpcs),
                "phpcs.xml matches the shared template",
                "local rules drift; §9 puts collection-wide sniffs in the "
                "template and the residue in inline ignores with reasons")

    td = re.search(r'name="text_domain"\s+value="([^"]+)"', phpcs)
    domains = [d.strip() for d in td.group(1).split(",")] if td else []
    r.check(slug in domains, "phpcs text_domain includes the slug",
            td.group(1) if td else "not set")
    r.check('value="6.8"' in phpcs, "phpcs minimum_wp_version 6.8")

    # --- §1.1 the floors, in all six places --------------------------------
    # Header and phpcs are checked above; these are the other four. The floors
    # only work if every one of them agrees.
    composer = read(os.path.join(root, "composer.json")) or ""
    r.check('">=8.2"' in composer, "composer require.php is >=8.2")

    # composer.lock must agree with composer.json. Composer treats a mismatch as
    # an error, not a warning, so CI's `composer install` fails before PHPUnit
    # runs at all. Raising the PHP floor in composer.json without re-locking put
    # ten plugins in that state at once.
    lock = read(os.path.join(root, "composer.lock"))
    if lock:
        try:
            import json as _json
            data = _json.loads(lock)
            plat = (data.get("platform-overrides") or data.get("platform")
                    or {}).get("php")
            r.check(plat in (None, ">=8.2"),
                    "composer.lock platform matches composer.json",
                    "%s (run: composer update --lock)" % plat)
        except ValueError as exc:
            r.check(False, "composer.lock is not valid JSON", str(exc))

    if env:
        r.check('"phpVersion": "8.2"' in env, "wp-env phpVersion 8.2")

    if readme:
        req_wp = re.search(r"^Requires at least:\s*(\S+)", readme, re.M)
        req_php = re.search(r"^Requires PHP:\s*(\S+)", readme, re.M)
        tested = re.search(r"^Tested up to:\s*(\S+)", readme, re.M)
        r.check(req_wp is not None and req_wp.group(1) == "6.8",
                "README Requires at least 6.8",
                req_wp.group(1) if req_wp else "missing")
        r.check(req_php is not None and req_php.group(1) == "8.2",
                "README Requires PHP 8.2",
                req_php.group(1) if req_php else "missing")
        r.check(tested is not None and tested.group(1) == "7.0",
                "README Tested up to 7.0",
                tested.group(1) if tested else "missing")

    if ci:
        r.check("'8.2'" in ci, "CI tests PHP 8.2")
        r.check("wordpress: '6.8'" in ci, "CI floor row is WP 6.8")
        r.check("'7.4'" not in ci and "'8.4'" not in ci,
                "CI references neither PHP 7.4 nor 8.4")

    # §9: a suppression is allowed in includes/ only when it carries a reason on
    # the same line. Anywhere else, or without a reason, it fails. Banning them
    # outright proved unsatisfiable -- DirectDatabaseQuery has no code-level
    # answer for a plugin that owns a table -- so the collection-wide sniffs
    # live in the shared phpcs.xml and the residue must justify itself.
    for path in walk(root):
        if not path.endswith(".php"):
            continue
        rel = os.path.relpath(path, root)
        body = read(path) or ""
        for line in body.split("\n"):
            m = re.search(r"phpcs:(disable|ignore)\b(.*)$", line)
            if not m:
                continue
            if not rel.startswith("includes" + os.sep):
                r.check(False, "phpcs suppression outside includes/", rel)
            elif "--" not in m.group(2):
                r.check(False, "phpcs suppression with no reason",
                        "%s: %s" % (rel, line.strip()[:60]))

    # §4.1 admin hook suffixes are derived, never spelled out.
    #
    # WordPress builds a submenu's hook as
    # sanitize_title( $menu_title ) . '_page_' . $slug, so a hardcoded one moves
    # the moment the menu is renamed -- silently, because nothing errors: the
    # screen still loads, its assets just stop being enqueued. Renaming
    # wp-postratings' menu did exactly that and turned its shape picker into a
    # list of labels.
    #
    # toplevel_page_ and settings_page_ are exempt: neither depends on the title.
    for path in sorted(glob.glob(os.path.join(root, "includes", "*.php"))):
        rel = os.path.relpath(path, root)
        for n, line in enumerate((read(path) or "").split("\n"), 1):
            if line.lstrip().startswith("*") or line.lstrip().startswith("//"):
                continue
            # Two fragile shapes: a prefix awaiting concatenation
            # ('ratings_page_' . $slug), and a fully spelled suffix naming one
            # of this plugin's own pages ('ratings_page_wp-postratings'). A
            # complete literal that is not about this plugin -- a shortcode
            # called poll_page_shortcode, say -- is neither.
            for m in re.finditer(r"'([a-z0-9-]+)_page_([a-z0-9-]*)'", line):
                if m.group(1) in ("toplevel", "settings"):
                    continue
                if m.group(2) and slug not in m.group(2):
                    continue
                r.check(False, "admin hook suffix hardcoded, derive it (§4.1)",
                        "%s:%d: %s" % (rel, n, m.group(0)))

    # --- §2.2 class constants have one spelling each ------------------------
    # The five names are fixed and so are four of their five values, which makes
    # this the cheapest section in the standard to check and one of the last to
    # get a check. §2.2 exists because eleven different spellings were in use --
    # OPTION_NAME, OPTION_GROUP, PAGE_SLUG, DB_VERSION_OPTION and friends -- and
    # nothing has compared the nineteen since they were renamed.
    #
    # Values, not just names: a GROUP that stops matching OPTION splits the
    # settings group from the row it saves into, which options.php answers with
    # a redirect to a page that saves nothing, and no tool here would have seen
    # it. §2.2 pins them equal for that reason.
    consts = class_constants(root, includes)

    for cname, value, where in consts:
        if cname in RETIRED_CONSTS:
            r.check(False, "§2.2 retired class constant",
                    "%s in %s (see §2.2 for the replacement)" % (cname, where))
            continue

        want = {
            "VERSION": under + "_version",
            "GROUP": under + "_options",
        }.get(cname)

        if want is not None:
            r.check(value == want, "§2.2 class constant value",
                    "%s = %r in %s, want %r" % (cname, value, where, want))

        # OPTION is the settings row on the class that owns the settings, and
        # the volatile-data row (§2.1's `{{UNDER}}_<noun>`) on a class that owns
        # one -- wp-ban's WP_Ban_Stats. Both are the plugin's own prefix.
        if cname == "OPTION":
            r.check(value.startswith(under + "_"), "§2.2 OPTION is a §2.1 row",
                    "%s = %r in %s, want %s_*" % (cname, value, where, under))

        if cname == "PAGE":
            r.check(value == slug or value.startswith(slug + "-"),
                    "§2.2 PAGE is the page slug",
                    "%s = %r in %s, want %s or %s-*"
                    % (cname, value, where, slug, slug))

        # §4.2: SECTION_<NAME> = '{{UNDER}}_<name>'. Nineteen plugins agree
        # today; nothing compared them, and a section id is what
        # add_settings_section() and do_settings_sections() have to agree on.
        if cname.startswith("SECTION_"):
            expect = under + "_" + cname[len("SECTION_"):].lower()
            r.check(value == expect, "§4.2 SECTION_ constant value",
                    "%s = %r in %s, want %r" % (cname, value, where, expect))

    names = {cname for cname, _, _ in consts}

    # A plugin that stores nothing at all (§2.1) has no row for OPTION or
    # VERSION to name, which is why four of the nineteen define neither. §2.2
    # says "every plugin defines OPTION and VERSION" and is wrong about those
    # four -- the rule that survives contact with §2.1 is this one.
    if slug in STORES_NOTHING:
        for cname in ("OPTION", "VERSION"):
            r.check(cname not in names,
                    "§2.1 a plugin that stores nothing names no row",
                    "%s is defined but the plugin writes no option row" % cname)
    else:
        for cname in ("OPTION", "VERSION"):
            r.check(cname in names, "§2.2 class constant defined", cname)

        r.check(any(cname == "OPTION" and value == under + "_options"
                    for cname, value, _ in consts),
                "§2.2 OPTION names the settings row",
                "no class defines OPTION = '%s_options'" % under)

    # --- §2.7 capabilities --------------------------------------------------
    # Two halves, both closed sets.
    #
    # The value: manage_options, or the one custom capability §2.7 names for
    # this plugin and no other. A plugin quietly gating a screen on a sibling's
    # capability, or inventing a new one, is a permission change nobody asked
    # for, and it is invisible until a site notices a role can no longer reach a
    # screen. wp-downloadmanager's `activate_plugins`-as-"level 10" (§7.2.2) is
    # the shape: a capability standing in for something it does not mean.
    #
    # The route: §2.7 requires every check of the plugin's *own* capability to
    # go through one apply_filters( '{{UNDER}}_capability', … ) so a site has a
    # single place to move it. Core meta-capabilities, unfiltered_html and the
    # editor-integration gates are explicitly NOT behind it -- five plugins were
    # right to be ignoring the earlier absolute wording -- so this checks that
    # the filter exists and wraps the constant, not that no other
    # current_user_can() appears anywhere.
    allowed_caps = {"manage_options"}
    if slug in CUSTOM_CAPABILITIES:
        allowed_caps.add(CUSTOM_CAPABILITIES[slug])

    for cname, value, where in consts:
        if cname != "CAPABILITY":
            continue
        r.check(value in allowed_caps, "§2.7 capability is the one §2.7 names",
                "%s in %s, allowed here: %s"
                % (value, where, ", ".join(sorted(allowed_caps))))

        # §2.7: a plugin gating on anything other than manage_options is taking
        # an exception, and "the reason goes in a docblock at the gate". The
        # reason cannot be judged mechanically, but its absence can: a constant
        # carrying nothing but a one-line summary and its @var has not argued
        # anything. wp-dbmanager is the model -- it says why install_plugins is
        # right and why that is not drift -- and wp-polls had four bare lines
        # until 2026-08-04, which is how a deliberate decision becomes something
        # the next reader "tidies up".
        if "manage_options" == value:
            continue

        block = ""
        for path in [main] + sorted(glob.glob(os.path.join(includes, "*.php"))):
            body = read(path) or ""
            m = re.search(
                r"(/\*\*(?:(?!\*/).)*?\*/)\s*const CAPABILITY\s*=\s*'%s'"
                % re.escape(value), body, re.S)
            if m:
                block = m.group(1)
                break

        # Lines of actual prose: not the delimiters, not the @var, not blanks.
        prose = [ln for ln in block.split("\n")
                 if re.match(r"^\s*\*\s+\S", ln) and "@" not in ln]

        r.check(len(prose) >= 3,
                "§2.7 a capability that is not manage_options argues for itself",
                "%s in %s has %d line(s) of reasoning on its constant; §2.7 "
                "asks why this gate is not manage_options"
                % (value, where, len(prose)))

    if any(cname == "CAPABILITY" for cname, _, _ in consts):
        # The default passed to the filter need not be the bare constant:
        # wp-downloadmanager picks between manage_options and its own capability
        # on the context before filtering, which is exactly what §2.7 asks for.
        # So this looks for the constant anywhere in the call's arguments rather
        # than immediately after the hook name.
        shipped_php = "\n".join(read(p) or "" for p in sorted(
            glob.glob(os.path.join(includes, "*.php"))) + [main])
        filtered = None
        for m in re.finditer(
                r"apply_filters(?:_ref_array)?\(\s*'%s_capability'"
                % re.escape(under), shipped_php):
            if "::CAPABILITY" in shipped_php[m.end():m.end() + 300]:
                filtered = m
                break
        r.check(filtered is not None,
                "§2.7 the capability is read through one filter",
                "no apply_filters( '%s_capability', self::CAPABILITY, … )"
                % under)

        # A plugin that ships a custom capability must actually name it. This is
        # the half that goes stale: §2.7's list is prose, and a plugin dropping
        # its custom capability for manage_options would leave the list saying
        # something no code does.
        if slug in CUSTOM_CAPABILITIES:
            r.check(any(cname == "CAPABILITY"
                        and value == CUSTOM_CAPABILITIES[slug]
                        for cname, value, _ in consts),
                    "§2.7 the custom capability is still defined",
                    "no class defines CAPABILITY = '%s'"
                    % CUSTOM_CAPABILITIES[slug])

    # --- §4.2.1 / §4.2.2 the tab strip --------------------------------------
    # Every tabbed screen builds its strip from one tabs() returning slug =>
    # label, so the labels are readable without running anything. Two things are
    # checked: the strip is exactly what the standard says it is, in order, and
    # -- separately, because it needs no table and so survives a plugin the
    # table has not heard of -- no label is one of the spellings §4.2.2 retires.
    #
    # `Options` is banned outright: the page is already Settings, so a tab
    # called `Poll Options` says the same thing twice and is what five of the
    # six tabbed plugins were doing.
    #
    # §4.2.2's other half -- a label must not repeat a word the surrounding
    # context already supplies -- is deliberately NOT checked. The section says
    # in as many words that the obvious mechanical reading ("drop the plugin
    # name") is wrong and leads somewhere silly, and that the test is whether
    # the word is doing work where it stands. A check for it would fire on
    # `Users Online` and miss `E-Mail Templates`, which is worse than none.
    labels = []
    tabs_file = None
    for path in sorted(glob.glob(os.path.join(includes, "*.php"))):
        body = read(path) or ""
        m = re.search(r"function\s+tabs\s*\([^)]*\)\s*\{(.*?)\n\t\}", body,
                      re.S)
        if not m:
            continue
        tabs_file = os.path.relpath(path, root)
        labels = re.findall(r"__\(\s*'([^']+)'", m.group(1))
        break

    if slug in TAB_LABELS:
        r.check(labels == TAB_LABELS[slug], "§4.2.1 the tab strip, in order",
                "%s has %s, want %s"
                % (tabs_file or "no tabs() found", labels, TAB_LABELS[slug]))
    else:
        r.check(not labels, "§4.2.1 a tab strip the standard does not know",
                "%s builds tabs %s; add them to TAB_LABELS and to §4.2.1"
                % (tabs_file, labels))

    for label in labels:
        r.check("Options" not in label,
                "§4.2.2 a tab is never named Options",
                "%r in %s -- the page is already Settings" % (label, tabs_file))

    # --- §13.1 the wp_stats_sections entry ----------------------------------
    # The one cross-plugin contract, and the one place where changing a plugin
    # in isolation breaks a sibling. §13.1 pins the array shape precisely
    # because seven plugins implemented it in seven separate sessions; the
    # shared metadata fixture pins §13.2's shared-row hazard, and this is the
    # half of §13 nothing had compared.
    #
    # A key that drifts is silent in both directions: wp-stats skips a
    # malformed entry rather than fatalling (§13.2), so a contributor keyed
    # 'polls' instead of 'wp_polls' simply renders nothing, and the theme hook
    # wp_stats_section_{key} a site had written moves out from under it.
    if slug in WPSTATS_CONTRIBUTORS:
        path = os.path.join(includes, "class-%s-wpstats.php" % slug)
        body = read(path) or ""
        rel = os.path.relpath(path, root)

        r.check(body != "", "§13 the WPStats component exists", rel)

        if body:
            r.check("add_filter( 'wp_stats_sections'" in body,
                    "§13 contributes through wp_stats_sections", rel)

            m = re.search(
                r"\$sections\['([a-z0-9_]+)'\]\s*=\s*array\((.*?)\n\t\t\);",
                body, re.S)
            r.check(m is not None, "§13.1 the entry is one array literal",
                    "%s: no $sections['…'] = array( … ); found" % rel)

            if m:
                r.check(m.group(1) == under,
                        "§13.1 the entry is keyed by {{UNDER}}",
                        "%s keys it %r, want %r" % (rel, m.group(1), under))
                for key in ("title", "priority", "render"):
                    r.check("'%s'" % key in m.group(2),
                            "§13.1 the entry names every key",
                            "%s: no %r in the entry" % (rel, key))

            # §13.1: a contributor that is opted out returns $sections
            # untouched, and reads only its own row to decide.
            r.check("stats_display" in body,
                    "§13.1 the contributor honours its own stats_display",
                    rel)

    if slug == "wp-stats":
        body = "\n".join(read(p) or "" for p in sorted(
            glob.glob(os.path.join(includes, "*.php"))))
        r.check("apply_filters( 'wp_stats_sections', array() )" in body,
                "§13 wp-stats fires wp_stats_sections with an empty array")
        r.check("'wp_stats_section_' . $key" in body,
                "§13.1 wp-stats dispatches wp_stats_section_{key}")

    # --- §4.3 list tables, the half that is checkable -----------------------
    # "Every tabular data screen is a WP_List_Table subclass" splits into a half
    # a reader can decide and a half only a reader can: which screens are
    # tabular data screens is judgement -- wp-serverinfo's five key/value report
    # tables are not, and §4.3's own deviations for wp-dbmanager are argued
    # rather than derived -- but a class that calls itself a Table and is not
    # one is mechanical. §2.4 makes `_Table` the suffix for exactly this thing,
    # so the name is the claim and this checks the claim.
    #
    # no_items() and get_columns() are the two §4.3 asks for unconditionally.
    # The rest of its list -- pagination at 20, sortable columns, hover row
    # actions, bulk actions -- is prefaced "normally" and has two documented
    # exceptions in wp-dbmanager alone, so it is not checked.
    if os.path.isdir(includes):
        for entry in sorted(os.listdir(includes)):
            if not entry.endswith(".php"):
                continue
            body = read(os.path.join(includes, entry)) or ""
            for m in re.finditer(
                    # \b after _Table, or WP_DBManager_Tables -- the ops
                    # component, not a list table -- matches on its own prefix.
                    r"^\s*(?:final\s+|abstract\s+)?class\s+(\w+_Table)\b"
                    r"(?:\s+extends\s+(\w+))?", body, re.M):
                cls, parent = m.group(1), m.group(2)
                r.check(parent == "WP_List_Table",
                        "§4.3 a _Table class is a WP_List_Table",
                        "%s in %s extends %s" % (cls, entry, parent or "nothing"))
                r.check(entry.endswith("-table.php"),
                        "§2.4 a list table lives in class-*-table.php",
                        "%s declares %s" % (entry, cls))
                for method in ("no_items", "get_columns"):
                    r.check(re.search(r"function\s+%s\s*\(" % method, body),
                            "§4.3 a list table defines %s()" % method,
                            "%s in %s" % (cls, entry))

    # --- §7.2.4 an escaping regression test exists, in the shape §7.2.4 asks --
    # The coarse half, and it is worth saying plainly what it does not do:
    # nothing here can enumerate the values a plugin echoes from the database,
    # so this cannot tell a suite that covers every output surface from one that
    # covers a single column. What it can do is fail the day the escaping test
    # is deleted or watered down, which is the failure mode §7.2.4 was written
    # against -- the guard is not "we escape carefully" but a test that goes red
    # when an output stops escaping.
    #
    # The shape is checked because §7.2.4 insists on both halves and the reason
    # is not obvious: escaping that dropped the value entirely passes the
    # negative assertion while corrupting the data, and a poll answer that
    # silently vanishes is its own bug. So one file must carry a canonical
    # payload, an assertion that something is absent, and an assertion that
    # something is present.
    #
    # Scoped to the plugins that store something. §7.2.4 opens "every plugin
    # that echoes a value it read from the database"; the four §2.1 plugins that
    # write no row at all have none to echo, and wp-relativedate's kses test
    # deliberately asserts only the negative half because there is no stored
    # value to preserve.
    if slug not in STORES_NOTHING:
        payloads = re.compile(r"<script>|onerror\s*=|onmouseover\s*=")
        proof = None
        for entry in sorted(os.listdir(tests) if os.path.isdir(tests) else []):
            if not entry.startswith("test-") or not entry.endswith(".php"):
                continue
            body = read(os.path.join(tests, entry)) or ""
            if (payloads.search(body)
                    and "assertStringNotContainsString" in body
                    and "assertStringContainsString" in body):
                proof = entry
                break

        r.check(proof is not None,
                "§7.2.4 an escaping regression test with a canonical payload",
                "no tests/test-*.php holds one of §7.2.4's three payloads "
                "together with both an absent- and a present- assertion")

    # --- §2.5 global functions ----------------------------------------------
    # Same shape as §2.4, which has been checked since the fan-out: a name that
    # reaches global scope is prefixed, and where it may live is a closed set.
    #
    # Two checks, because §2.5's two sentences say different things and only one
    # of them survives contact with the collection. "Global functions exist only
    # in template-tags.php and deprecated.php" is false in all nineteen --
    # uninstall.php necessarily declares one, and §7.2.1 relies on it doing so
    # -- so the enforceable rule is the second sentence: any other global
    # function is prefixed {{UNDER}}_. template-tags.php and deprecated.php are
    # exempt from the prefix because §2.5 requires the opposite of them: those
    # names shipped in the last SVN release and are the documented public API.
    #
    # A global function inside a class-*.php file is a violation whichever way
    # it is spelled -- that file declares a class, and "everything else is a
    # class method" is unambiguous there.
    #
    # Column-anchored deliberately: every method in the collection is indented,
    # so this cannot mistake one for a global function. A global function nested
    # inside a conditional would slip through, which is a miss rather than a
    # false alarm.
    for path in shipped:
        rel = os.path.relpath(path, root)
        body = read(path) or ""
        base = os.path.basename(path)

        for m in re.finditer(r"^function\s+(\w+)\s*\(", body, re.M):
            fn = m.group(1)
            line = body.count("\n", 0, m.start()) + 1

            if base.startswith("class-"):
                r.check(False, "§2.5 a class file declares a global function",
                        "%s() at %s:%d -- everything but a template tag or a "
                        "deprecated shim is a class method" % (fn, rel, line))
                continue

            if base in ("template-tags.php", "deprecated.php"):
                continue

            r.check(fn.startswith(under + "_"), "§2.5 global function prefix",
                    "%s() at %s:%d, want %s_*" % (fn, rel, line, under))

    # --- a widget fills its instance out against defaults -------------------
    #
    # WP_Widget::widget() is handed whatever array the caller passed. the_widget()
    # passes only what its caller wrote, and a sidebar can still hold an instance
    # stored before a setting existed -- so a key read straight out of it prints
    # "Undefined array key" into the middle of the rendered page.
    #
    # Seven plugins ship a widget. Six were already right, five by parsing
    # against a defaults() method and one by guarding every read; wp-polls was
    # the one that did neither, and it was found by *looking at a screenshot of
    # the widget*, not by any suite. Nothing mechanical asked until this rule.
    #
    # Either shape passes: wp_parse_args() over the instance, or a guard on
    # every read. The check is deliberately loose about which, because
    # wp-useronline's guards are correct and rewriting them to satisfy a checker
    # would be the tail wagging the dog.
    for path in shipped:
        body = read(path) or ""

        if "extends WP_Widget" not in body:
            continue

        rel = os.path.relpath(path, root)
        m = re.search(r"function\s+widget\s*\(\s*\$\w+\s*,\s*\$(\w+)\s*\)", body)

        if not m:
            continue

        instance = m.group(1)
        # Bounded to widget()'s own body, and that bound is the whole rule.
        #
        # Scanning to the end of the file instead looks harmless -- it can only
        # be more lenient -- but form() parses the same $instance a few methods
        # later in every one of these classes, so the leniency is total: the
        # rule passed on the plugin it was written for. Caught by reverting
        # wp-polls' fix and watching the check stay green.
        tail = body[m.end():]
        nxt = re.search(r"\n\t(?:public |protected |private )?function\s", tail)
        if nxt:
            tail = tail[:nxt.start()]
        parsed = re.search(r"wp_parse_args\s*\(\s*\(array\)\s*\$" + instance, tail)
        reads = re.findall(r"\$" + instance + r"\[\s*'(\w+)'\s*\]", tail)
        guarded = re.findall(
            r"(?:!\s*empty|isset)\s*\(\s*\$" + instance + r"\[\s*'(\w+)'\s*\]",
            tail,
        )

        unguarded = [k for k in reads if k not in guarded]

        r.check(bool(parsed) or not unguarded,
                "a widget() fills its instance out against defaults",
                "%s reads %s from $%s without wp_parse_args() or a guard -- an "
                "instance missing a key prints a PHP warning into the page"
                % (rel, ", ".join(sorted(set(unguarded))[:4]), instance))

    # --- §13.4.7 what the WP-CLI and REST files are called ------------------
    #
    # The shipped class is named for the thing it is and the test for the
    # surface it exercises, which is why WP_Sweep_Command is tested by
    # test-cli.php. Both halves are copied per plugin, and anything copied into
    # nineteen repositories diverges unless something compares it.
    command_file = os.path.join(root, "includes", "class-%s-command.php" % slug)

    if os.path.exists(command_file):
        body = read(command_file) or ""
        want_class = prefix + "_Command"

        r.check("class %s extends WP_CLI_Command" % want_class in body,
                "§13.4.7 command class name",
                "%s should declare `class %s extends WP_CLI_Command`"
                % (os.path.relpath(command_file, root), want_class))

        # The registered name is the slug without the wp- prefix (§13.3): a
        # directory convention is not a command-naming one, and `wp wp-polls`
        # spells wp twice.
        bare = slug[3:] if slug.startswith("wp-") else slug
        registered = re.search(r"WP_CLI::add_command\(\s*'([^']+)'", "\n".join(
            read(p) or "" for p in shipped))

        r.check(registered is not None and registered.group(1) == bare,
                "§13.3 command registers under the bare noun",
                "want '%s', found %s" % (
                    bare,
                    "'%s'" % registered.group(1) if registered else "no add_command() call"))

        # A command offering --format=ids has to reduce its rows to that column.
        #
        # WP_CLI\Utils\format_items() hands `ids` straight to implode(), so rows
        # that are associative arrays print as the word `Array`, once per row,
        # with a PHP warning. Six commands advertised the format and six got
        # this wrong, including one whose README documented a `| xargs` pipe
        # built on it -- and every suite was green, because the WP_CLI stand-in
        # records what it is handed instead of formatting it. Two agents
        # inferred the bug from WP-CLI's source; running `wp polls list
        # --format=ids` against a real WP-CLI is what settled it.
        offers_ids = re.search(r"^\s*\*\s*-\s*ids\s*$", body, re.M)

        r.check(not offers_ids or "wp_list_pluck( $rows" in body,
                "a command offering --format=ids reduces rows to the id",
                "%s advertises --format=ids; without wp_list_pluck() over the "
                "rows it prints `Array` per row"
                % os.path.relpath(command_file, root))

        test_cli = os.path.join(root, "tests", "test-cli.php")
        r.check(os.path.exists(test_cli), "§13.4.7 a command has tests/test-cli.php")

        if os.path.exists(test_cli):
            r.check("class %s_CLI_Test" % prefix in (read(test_cli) or ""),
                    "§13.4.7 CLI test class name",
                    "tests/test-cli.php should declare class %s_CLI_Test" % prefix)

        # §13.4.7 again: a command nobody is told about is a command nobody
        # runs, and README.md ships to wordpress.org as readme.txt. Caught by
        # Lester on the first three plugins rather than by any check.
        r.check(readme is not None and "### WP-CLI" in readme,
                "§13.4.7 a command is documented in the README",
                "README.md needs a `### WP-CLI` block under `## Usage`")

    api_file = os.path.join(root, "includes", "class-%s-api.php" % slug)

    if os.path.exists(api_file):
        body = read(api_file) or ""
        want_class = prefix + "_API"
        bare = slug[3:] if slug.startswith("wp-") else slug

        r.check("class %s" % want_class in body, "§13.4.7 API class name",
                "%s should declare `class %s`"
                % (os.path.relpath(api_file, root), want_class))

        r.check("const REST_NAMESPACE = '%s/v1'" % bare in body,
                "§13.3 REST namespace is the bare noun",
                "%s should carry const REST_NAMESPACE = '%s/v1'"
                % (os.path.relpath(api_file, root), bare))

        test_rest = os.path.join(root, "tests", "test-rest-api.php")
        r.check(os.path.exists(test_rest), "§13.4.7 a namespace has tests/test-rest-api.php")

        if os.path.exists(test_rest):
            r.check("class %s_REST_API_Test" % prefix in (read(test_rest) or ""),
                    "§13.4.7 REST test class name",
                    "tests/test-rest-api.php should declare class %s_REST_API_Test" % prefix)

        r.check(os.path.exists(os.path.join(root, "tests", "e2e", "rest.spec.js")),
                "§13.4.7 a namespace has tests/e2e/rest.spec.js")

        r.check(readme is not None and "### REST API" in readme,
                "§13.4.7 a namespace is documented in the README",
                "README.md needs a `### REST API` block under `## Usage`")

    return r


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    quiet = "--quiet" in sys.argv

    selected = [p for p in PLUGINS if not args or p[0] in args]
    if not selected:
        print("no matching plugin; known: %s"
              % ", ".join(p[0] for p in PLUGINS))
        return 1

    total = 0
    for slug, name, prefix, port in selected:
        root = os.path.join(ROOT, slug)
        if not os.path.isdir(root):
            print("MISSING  %s" % slug)
            total += 1
            continue

        report = verify(slug, name, prefix, port, root)
        total += len(report.failures)

        if report.failures:
            print("\n%s  %d failing" % (slug, len(report.failures)))
            seen = set()
            for label, detail in report.failures:
                key = (label, detail)
                if key in seen:
                    continue
                seen.add(key)
                print("   - %s%s" % (label, ": " + detail if detail else ""))
        elif not quiet:
            print("%s  ok" % slug)

    print("\n%d failing checks across %d plugins" % (total, len(selected)))
    return min(total, 250)


if __name__ == "__main__":
    sys.exit(main())
