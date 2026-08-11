# WordPress Plugins — the shared standard

[![Verify](https://github.com/lesterchan/wordpress-plugins/actions/workflows/verify.yml/badge.svg)](https://github.com/lesterchan/wordpress-plugins/actions/workflows/verify.yml)

Nineteen WordPress plugins, held to one written standard so they read as though
one person wrote them on the same afternoon.

The badge above is this repository's own CI: it clones all nineteen plugins and
runs `bin/verify.py` across them on every push and once a night, and a second job
breaks two things on purpose to prove the checker can still fail. Each plugin's
own badge is in the table below.

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

Install counts are wordpress.org's own active-install buckets, which is why they
are round: the API reports the floor of a range, not a figure. They are a
snapshot, taken by hand, and they go stale — re-read them from
`api.wordpress.org/plugins/info/1.2/` rather than trusting the column. Across
the nineteen that is roughly 880,000 active installs and 31.8 million
downloads, spread very unevenly; WP-PageNavi alone is over half of both.

| Plugin | Slug | Installs | CI | What it does |
|---|---|--:|---|---|
| [FreeMyInternet](https://github.com/lesterchan/freemyinternet) | `freemyinternet` | &lt;10 | [![CI](https://github.com/lesterchan/freemyinternet/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/freemyinternet/actions/workflows/ci.yml) | A site-wide protest banner or full-screen blackout, with optional start and end dates. |
| [WP-Ban](https://github.com/lesterchan/wp-ban) | `wp-ban` | 8,000+ | [![CI](https://github.com/lesterchan/wp-ban/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-ban/actions/workflows/ci.yml) | Ban visitors by IP, IP range, host name, user agent or referrer. |
| [WP-CommentNavi](https://github.com/lesterchan/wp-commentnavi) | `wp-commentnavi` | 700+ | [![CI](https://github.com/lesterchan/wp-commentnavi/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-commentnavi/actions/workflows/ci.yml) | Paged navigation for comments. |
| [WP-DBManager](https://github.com/lesterchan/wp-dbmanager) | `wp-dbmanager` | 60,000+ | [![CI](https://github.com/lesterchan/wp-dbmanager/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-dbmanager/actions/workflows/ci.yml) | Optimise, repair, back up and restore the database, on a schedule. |
| [WP-DownloadManager](https://github.com/lesterchan/wp-downloadmanager) | `wp-downloadmanager` | 3,000+ | [![CI](https://github.com/lesterchan/wp-downloadmanager/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-downloadmanager/actions/workflows/ci.yml) | A simple download manager with hit counting. |
| [WP-DraftsForFriends](https://github.com/lesterchan/wp-draftsforfriends) | `wp-draftsforfriends` | 1,000+ | [![CI](https://github.com/lesterchan/wp-draftsforfriends/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-draftsforfriends/actions/workflows/ci.yml) | Share a draft with somebody without giving them an account. |
| [WP-EMail](https://github.com/lesterchan/wp-email) | `wp-email` | 1,000+ | [![CI](https://github.com/lesterchan/wp-email/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-email/actions/workflows/ci.yml) | Let readers send a post or page to a friend. |
| [WP-PageNavi](https://github.com/lesterchan/wp-pagenavi) | `wp-pagenavi` | 500,000+ | [![CI](https://github.com/lesterchan/wp-pagenavi/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-pagenavi/actions/workflows/ci.yml) | Paged navigation for posts. |
| [WP-PluginsUsed](https://github.com/lesterchan/wp-pluginsused) | `wp-pluginsused` | 70+ | [![CI](https://github.com/lesterchan/wp-pluginsused/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-pluginsused/actions/workflows/ci.yml) | List the plugins a site has installed, in a post or page. |
| [WP-Polls](https://github.com/lesterchan/wp-polls) | `wp-polls` | 40,000+ | [![CI](https://github.com/lesterchan/wp-polls/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-polls/actions/workflows/ci.yml) | An AJAX poll system, heavily templatable. |
| [WP-PostRatings](https://github.com/lesterchan/wp-postratings) | `wp-postratings` | 30,000+ | [![CI](https://github.com/lesterchan/wp-postratings/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-postratings/actions/workflows/ci.yml) | An AJAX rating system for any content. |
| [WP-PostViews](https://github.com/lesterchan/wp-postviews) | `wp-postviews` | 100,000+ | [![CI](https://github.com/lesterchan/wp-postviews/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-postviews/actions/workflows/ci.yml) | Count and display how often a post has been viewed. |
| [WP-Print](https://github.com/lesterchan/wp-print) | `wp-print` | 8,000+ | [![CI](https://github.com/lesterchan/wp-print/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-print/actions/workflows/ci.yml) | A printable version of any post or page. |
| [WP-RelativeDate](https://github.com/lesterchan/wp-relativedate) | `wp-relativedate` | 100+ | [![CI](https://github.com/lesterchan/wp-relativedate/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-relativedate/actions/workflows/ci.yml) | Show "Today", "Yesterday", "2 days ago" beside real dates. |
| [WP-ServerInfo](https://github.com/lesterchan/wp-serverinfo) | `wp-serverinfo` | 10,000+ | [![CI](https://github.com/lesterchan/wp-serverinfo/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-serverinfo/actions/workflows/ci.yml) | Report the host's PHP, MySQL, memcached and Redis configuration. |
| [WP-ShowHide](https://github.com/lesterchan/wp-showhide) | `wp-showhide` | 9,000+ | [![CI](https://github.com/lesterchan/wp-showhide/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-showhide/actions/workflows/ci.yml) | Toggle the visibility of content with a shortcode. |
| [WP-Stats](https://github.com/lesterchan/wp-stats) | `wp-stats` | 2,000+ | [![CI](https://github.com/lesterchan/wp-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-stats/actions/workflows/ci.yml) | Site statistics, and the one page the others contribute blocks to. |
| [WP-Sweep](https://github.com/lesterchan/wp-sweep) | `wp-sweep` | 100,000+ | [![CI](https://github.com/lesterchan/wp-sweep/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-sweep/actions/workflows/ci.yml) | Clean up unused, orphaned and duplicated data. |
| [WP-UserOnline](https://github.com/lesterchan/wp-useronline) | `wp-useronline` | 10,000+ | [![CI](https://github.com/lesterchan/wp-useronline/actions/workflows/ci.yml/badge.svg)](https://github.com/lesterchan/wp-useronline/actions/workflows/ci.yml) | Show how many people are on the site right now. |

**All nineteen majors are released.** Each is a rewrite against the standard and
carries breaking changes, documented per plugin under `## Upgrade Notice` in its
own README. wordpress.org serves them now; the commit each plugin shipped from
*before* this work is tagged in its own repository, so the two are comparable.
`Stable tag` in a plugin's README is the authority for what it ships — the table
above is a snapshot like the install counts.

## What is in here

| Path | What it is |
|---|---|
| [`_standards/STANDARDS.md`](_standards/STANDARDS.md) | The contract. 15 numbered sections, 44 including subsections. |
| [`_standards/RESUME.md`](_standards/RESUME.md) | Current state: what is finished, what is open, what is known broken. Written for somebody picking the work up cold. |
| `_standards/templates/` | The files every plugin copies verbatim, with `{{SLUG}}`-style placeholders. |
| `_standards/demo/` | Fixtures for the shared demo harness. |
| `bin/` | The tooling below. |
| `.wp-env.json` | All nineteen plugins in one WordPress, on ports 8888/8889. |

## Getting started

You need Docker (running, not merely installed), Node 24, Python 3 and git.
Docker is what [`wp-env`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/)
runs WordPress in; nothing here installs a web server or a database on your own
machine.

### 1. Clone this repository, then the nineteen inside it

Everything here resolves a plugin as `<this repository>/<slug>` — `verify.py`,
`.wp-env.json`, `bin/test-all.sh`. So the nineteen are cloned *into* this
folder, beside `bin/` and `_standards/`, not somewhere alongside it:

```
wordpress-plugins/          ← this repository
├── _standards/
├── bin/
├── .wp-env.json
├── freemyinternet/         ← each of these is its own repository,
├── wp-ban/                    untracked here, cloned separately
├── …
└── wp-useronline/
```

```sh
git clone https://github.com/lesterchan/wordpress-plugins.git
cd wordpress-plugins
```

The slug list comes out of `verify.py`'s own table rather than being typed
again, which is the same thing CI does and for the same reason — a second copy
of the list is what this repository exists to stop:

```sh
python3 -c "import sys; sys.path.insert(0, 'bin'); import verify; print('\n'.join(p[0] for p in verify.PLUGINS))" |
	xargs -P 6 -I{} git clone --quiet https://github.com/lesterchan/{}.git {}
```

CI adds `--depth 1` because it throws the clones away; leave it off here, since
a plugin's own history is most of what you will want to read. Confirm the layout
before going further — `verify.py` reports a plugin it cannot find as missing
rather than skipping it, so a run that names no missing plugin means all
nineteen are where the tooling expects:

```sh
python3 bin/verify.py
```

### 2. Start WordPress

```sh
npx --yes @wordpress/env start
```

This repository has no `package.json` of its own, so `npx` fetches `wp-env` on
demand; the `--yes` is what stops it asking. The first run downloads WordPress
and a MariaDB image and takes a few minutes, and subsequent runs are seconds.
It reads the `.wp-env.json` here, which mounts **all nineteen plugins into one
WordPress install** — which is also the only way to catch two plugins claiming
the same option row, function name or hook.

### 3. Fill it with something to look at

A bare install has no posts, so the pagination, ratings and comment plugins have
nothing to render:

```sh
bin/seed-demo.sh                      # 200 posts, 100 comments
bin/seed-demo.sh 500 250              # as much as you like
```

It activates all nineteen plugins and a classic theme, then seeds content and
prints where each demo page is. Run it again whenever you like: it clears what
the previous run made and nothing else.

### 4. Open it

| URL | What it is |
|---|---|
| <http://localhost:8888> | The site. Front page, demo pages, everything the plugins render. |
| <http://localhost:8888/wp-admin> | wp-admin. Log in as **`admin`** / **`password`**. |
| <http://localhost:8889> | The tests site. Not for browsing — see below. |

The site on 8889 is the one PHPUnit installs over, so it has no theme and no
active plugins; a browser pointed at it gets a blank front page and "not allowed
to access this page" everywhere else. That is expected. E2E runs go through a
plugin's own `bin/test-e2e.sh`, which activates the plugin and a theme first.

Each plugin also carries its own `.wp-env.json` on its own pair of ports, so you
can bring one plugin up in isolation from inside its directory without
disturbing this one. The port table is in
[`_standards/STANDARDS.md`](_standards/STANDARDS.md) under §10.

### Stopping and starting over

```sh
npx --yes @wordpress/env stop         # containers down, database kept
npx --yes @wordpress/env start --update   # pull newer WordPress and images
npx --yes @wordpress/env destroy      # delete the database and start clean
```

`destroy` is the fix for a site left in a strange state — nothing in it is
worth keeping, and `bin/seed-demo.sh` rebuilds the interesting part.

## Tooling

Nothing here modifies a plugin; every script only reads.

```sh
python3 bin/verify.py                 # check every plugin against the standard
python3 bin/verify.py wp-polls        # or just one
python3 bin/verify.py --quiet         # exit status is the failure count
```

`bin/verify.py` is the mechanical half of the standard — 160 checks at the time
of writing, not all of which apply to every plugin, covering layout, naming,
headers, admin screens, styles, testing, CI, linting and versioning. Re-derive
the count with `grep -c '\.check(' bin/verify.py` rather than trusting that
number; it goes up whenever a defect turns out to be checkable.

```sh
bin/test-all.sh                       # every plugin's PHPUnit suite, one container
bin/test-all.sh --multisite           # the same suites as a network
bin/seed-demo.sh                      # fill the demo harness with fixtures
```

Each plugin additionally carries `bin/test.sh`, `bin/test-multisite.sh` and
`bin/test-e2e.sh` of its own.

```sh
bin/generate-banner                   # every wordpress.org banner, into build/banners/
bin/generate-banner wp-polls          # or just one
bin/generate-banner --proof           # draw wp-admin's overlay on top
bin/generate-banner --install         # also copy into the SVN assets/ working copies
```

Each banner is composed from that plugin's own `assets/icon.svg`, so the set
cannot drift away from the icons wordpress.org already serves; the names,
taglines and accent colours are one table at the top of the script. The run
fails if any copy reaches into the band where wp-admin paints the plugin name
over the banner — a collision invisible on the wordpress.org page itself, which
overlays nothing. `--install` copies but never commits: publishing a banner is
an `svn commit` you make yourself, and it takes effect independently of any
plugin version or release.

**A green run is not compliance.** `verify.py` checks what can be checked
mechanically. The other half — voice, comment density, whether a name earns its
place — is not automatable and is not attempted. `_standards/RESUME.md` tracks
which sections of the standard have a check behind them and which do not,
because the sections with nothing behind them are where the next defect will be.

## Requirements

WordPress 6.8 and PHP 8.2 are the floors, for every plugin. Anything older is
simply not offered the update. Development needs Docker, Node 24, Python 3 and
git — see [Getting started](#getting-started).

## Licence

GPL-2.0-or-later. See [LICENSE](LICENSE). Each plugin is licensed the same way.
