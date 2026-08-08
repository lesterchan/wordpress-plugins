# WordPress Plugins — the shared standard

Nineteen WordPress plugins, held to one written standard so they read as though
one person wrote them on the same afternoon.

This repository is not a plugin. It is the tooling and the contract that sit
*above* nineteen plugins, each of which is its own repository, released to
wordpress.org on its own schedule. The plugin directories are cloned side by
side here and are deliberately untracked — see [`.gitignore`](.gitignore), which
lists them by name rather than by pattern and explains why.

## Why it exists

Nineteen copies of anything drift. Five spellings of one skip list. Seven
phrasings of one sentence. Four implementations of one test file. Each is
individually harmless and collectively means nineteen plugins that behave
almost, but not quite, alike.

The fix is to write the contract down once and check it mechanically. So the
only permitted differences between any two of these plugins are **name, features
and capability** — everything else is specified.

**The corollary is the part worth stealing:** anything copied into nineteen
repositories diverges unless something compares the copies. A rule the spec
states and nothing enforces is a rule that has already drifted; you just cannot
see it yet.

## The plugins

Each links to its own repository. All are on
[wordpress.org/plugins](https://wordpress.org/plugins/search/lesterchan/).

| Plugin | Slug | CI | What it does |
|---|---|---|---|
| [FreeMyInternet](https://github.com/lesterchan/freemyinternet) | `freemyinternet` | [![CI](https://github.com/lesterchan/freemyinternet/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/freemyinternet/actions/workflows/ci.yml) | A site-wide protest banner or full-screen blackout, with optional start and end dates. |
| [WP-Ban](https://github.com/lesterchan/wp-ban) | `wp-ban` | [![CI](https://github.com/lesterchan/wp-ban/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-ban/actions/workflows/ci.yml) | Ban visitors by IP, IP range, host name, user agent or referrer. |
| [WP-CommentNavi](https://github.com/lesterchan/wp-commentnavi) | `wp-commentnavi` | [![CI](https://github.com/lesterchan/wp-commentnavi/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-commentnavi/actions/workflows/ci.yml) | Paged navigation for comments. |
| [WP-DBManager](https://github.com/lesterchan/wp-dbmanager) | `wp-dbmanager` | [![CI](https://github.com/lesterchan/wp-dbmanager/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-dbmanager/actions/workflows/ci.yml) | Optimise, repair, back up and restore the database, on a schedule. |
| [WP-DownloadManager](https://github.com/lesterchan/wp-downloadmanager) | `wp-downloadmanager` | [![CI](https://github.com/lesterchan/wp-downloadmanager/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-downloadmanager/actions/workflows/ci.yml) | A simple download manager with hit counting. |
| [WP-DraftsForFriends](https://github.com/lesterchan/wp-draftsforfriends) | `wp-draftsforfriends` | [![CI](https://github.com/lesterchan/wp-draftsforfriends/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-draftsforfriends/actions/workflows/ci.yml) | Share a draft with somebody without giving them an account. |
| [WP-EMail](https://github.com/lesterchan/wp-email) | `wp-email` | [![CI](https://github.com/lesterchan/wp-email/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-email/actions/workflows/ci.yml) | Let readers send a post or page to a friend. |
| [WP-PageNavi](https://github.com/lesterchan/wp-pagenavi) | `wp-pagenavi` | [![CI](https://github.com/lesterchan/wp-pagenavi/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-pagenavi/actions/workflows/ci.yml) | Paged navigation for posts. |
| [WP-PluginsUsed](https://github.com/lesterchan/wp-pluginsused) | `wp-pluginsused` | [![CI](https://github.com/lesterchan/wp-pluginsused/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-pluginsused/actions/workflows/ci.yml) | List the plugins a site has installed, in a post or page. |
| [WP-Polls](https://github.com/lesterchan/wp-polls) | `wp-polls` | [![CI](https://github.com/lesterchan/wp-polls/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-polls/actions/workflows/ci.yml) | An AJAX poll system, heavily templatable. |
| [WP-PostRatings](https://github.com/lesterchan/wp-postratings) | `wp-postratings` | [![CI](https://github.com/lesterchan/wp-postratings/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-postratings/actions/workflows/ci.yml) | An AJAX rating system for any content. |
| [WP-PostViews](https://github.com/lesterchan/wp-postviews) | `wp-postviews` | [![CI](https://github.com/lesterchan/wp-postviews/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-postviews/actions/workflows/ci.yml) | Count and display how often a post has been viewed. |
| [WP-Print](https://github.com/lesterchan/wp-print) | `wp-print` | [![CI](https://github.com/lesterchan/wp-print/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-print/actions/workflows/ci.yml) | A printable version of any post or page. |
| [WP-RelativeDate](https://github.com/lesterchan/wp-relativedate) | `wp-relativedate` | [![CI](https://github.com/lesterchan/wp-relativedate/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-relativedate/actions/workflows/ci.yml) | Show "Today", "Yesterday", "2 days ago" beside real dates. |
| [WP-ServerInfo](https://github.com/lesterchan/wp-serverinfo) | `wp-serverinfo` | [![CI](https://github.com/lesterchan/wp-serverinfo/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-serverinfo/actions/workflows/ci.yml) | Report the host's PHP, MySQL, memcached and Redis configuration. |
| [WP-ShowHide](https://github.com/lesterchan/wp-showhide) | `wp-showhide` | [![CI](https://github.com/lesterchan/wp-showhide/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-showhide/actions/workflows/ci.yml) | Toggle the visibility of content with a shortcode. |
| [WP-Stats](https://github.com/lesterchan/wp-stats) | `wp-stats` | [![CI](https://github.com/lesterchan/wp-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-stats/actions/workflows/ci.yml) | Site statistics, and the one page the others contribute blocks to. |
| [WP-Sweep](https://github.com/lesterchan/wp-sweep) | `wp-sweep` | [![CI](https://github.com/lesterchan/wp-sweep/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-sweep/actions/workflows/ci.yml) | Clean up unused, orphaned and duplicated data. |
| [WP-UserOnline](https://github.com/lesterchan/wp-useronline) | `wp-useronline` | [![CI](https://github.com/lesterchan/wp-useronline/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-useronline/actions/workflows/ci.yml) | Show how many people are on the site right now. |

**The majors currently in these repositories are unreleased.** Each is a rewrite
against the standard and carries breaking changes, documented per plugin under
`## Upgrade Notice` in its README. What wordpress.org serves today is the
previous release; the commit each plugin shipped from before this work is
tagged in its own repository.

## What is in here

| Path | What it is |
|---|---|
| [`_standards/STANDARDS.md`](_standards/STANDARDS.md) | The contract. 15 numbered sections, 44 including subsections. |
| [`_standards/RESUME.md`](_standards/RESUME.md) | Current state: what is finished, what is open, what is known broken. Written for somebody picking the work up cold. |
| [`_standards/RELEASE.md`](_standards/RELEASE.md) | The release sequence, for the human doing it. The exhaustive pre-flight is the `release-wp-plugin` skill's; this covers what that skill does not — CI, the block build, and `assets/`. |
| `_standards/templates/` | The files every plugin copies verbatim, with `{{SLUG}}`-style placeholders. |
| `_standards/demo/` | Fixtures for the shared demo harness. |
| `bin/` | The tooling below. |
| `.wp-env.json` | All nineteen plugins in one WordPress, on ports 8888/8889. |

## Tooling

```sh
python3 bin/verify.py                 # check every plugin against the standard
python3 bin/verify.py wp-polls        # or just one
python3 bin/verify.py --quiet         # exit status is the failure count
```

`bin/verify.py` is the mechanical half of the standard — 153 checks, not all
of which apply to every plugin, covering layout, naming, headers, admin
screens, styles, testing, CI, linting and versioning.

```sh
bin/test-all.sh                       # every plugin's PHPUnit suite, one container
bin/test-all.sh --multisite           # the same suites as a network
bin/seed-demo.sh                      # fill the demo harness with fixtures
```

Each plugin additionally carries `bin/test.sh`, `bin/test-multisite.sh` and
`bin/test-e2e.sh` of its own.

**A green run is not compliance.** `verify.py` checks what can be checked
mechanically. The other half — voice, comment density, whether a name earns its
place — is not automatable and is not attempted. `_standards/RESUME.md` tracks
which sections of the standard have a check behind them and which do not,
because the sections with nothing behind them are where the next defect will be.

## Requirements

WordPress 6.8 and PHP 8.2 are the floors, for every plugin. Anything older is
simply not offered the update. Development needs Docker (for
[`wp-env`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/))
and Node 24.

## Licence

GPL-2.0-or-later. See [LICENSE](LICENSE). Each plugin is licensed the same way.
