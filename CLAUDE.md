# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

This repository is the shared tooling above nineteen WordPress plugins. Each
plugin is its own git repository, cloned side by side here and released to
wordpress.org on its own schedule; the plugin directories are deliberately
untracked, which is why `git status` here shows none of their changes. See
`.gitignore`, which lists them by name rather than by pattern and says why.

## Read in this order

1. **[`_standards/STANDARDS.md`](_standards/STANDARDS.md)** — the contract every
   plugin is held to, and the reason this repository exists.
2. **[`_standards/RESUME.md`](_standards/RESUME.md)** — the current state: what
   is finished, what is in flight, what is known broken, and which findings are
   still open. Written for somebody picking the work up cold.
3. The plugin's own **`CLAUDE.md`**, for what that plugin's code cannot tell
   you. Where a plugin's file and the standard disagree, the standard wins.

## Plugin `CLAUDE.md` files are standalone, and must stay that way

**They are read standalone.** The release path excludes `CLAUDE.md` from what
ships to wordpress.org (it once shipped, which is how this rule was learned),
but every plugin is its own public GitHub repository, and whoever clones one
has that plugin directory and nothing else: no `_standards/`, no siblings, no
idea what a section number refers to.

So the test for anything written in one is: **could someone who cloned only that
repository act on this line?** Four things fail it and are not to be
reintroduced:

* a path or section reference to something outside the plugin — `_standards/…`,
  `§7.6.1`, `task #17`. Restate the substance in a clause instead;
* a date, or a claim about what was green when. CI answers that, and a file
  saying "green" is wrong the moment it is not;
* a claim about the collection — "nineteen plugins", "the reference for §4.3",
  "wp-polls gets this wrong". Name another plugin only when it is a public
  plugin whose behaviour matters there, and say what the behaviour is;
* anything a reader cannot check from that directory. The plugin's own commit
  hashes are fine: those resolve in its own history.

Nothing is lost by leaving the pointers out, because anyone working across the
set reads STANDARDS.md and RESUME.md first anyway — that is what the order above
is for. `_standards/` and this file are the campaign's memory; the plugin files
are the plugin's.

## Working here

`bin/verify.py` checks a plugin against the mechanical half of the standard.
The judgement half — voice, comment density, whether a name earns its place —
is not automatable and is not attempted, so a green run is not compliance.

**Eight plugins now compile, and a plugin directory is no longer just what is in
git.** The ones with blocks carry `src/` (committed, never shipped) and generate
`build/` (gitignored, shipped — it is what the block registration loads).
`bin/build` makes one from the other, and `bin/test.sh`, `bin/test-e2e.sh` and
the release skill's deploy all run it before they do anything, so a suite cannot
test a stale build and a release cannot ship one. Two consequences worth knowing
before they bite:

* **`git status` is silent about `build/`, and `build/` ships.** The deploy
  rsyncs the working tree rather than a clean export, so anything untracked but
  present on disk goes to wordpress.org. That is how Playwright's artifacts once
  shipped with a logged-in session cookie in them.
* **You cannot mutation-test a built artefact through the runners**, because they
  rebuild first and your edit is gone before the suite starts. The suite passes
  for a reason unrelated to the code, which looks exactly like a test that cannot
  fail. Mutate the source and rebuild, or call phpunit directly.

Commit these repositories with `--no-gpg-sign`; the global `commit.gpgsign`
setting does not apply to them.

Nothing is pushed or tagged without being asked, and nothing goes near the SVN
checkouts in `~/svn/wordpress_plugins/` unless the task says so explicitly.

## A note on scale

Nineteen copies of anything drift. Most of the work recorded in RESUME.md is
some version of that discovery: five spellings of one skip list, seven
phrasings of one sentence, four implementations of one test file. When
something here looks oddly centralised, that is usually why — and when you add
something per plugin, assume it will diverge unless a test says otherwise.
