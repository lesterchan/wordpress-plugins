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

**They ship.** `plugin_deploy.sh` copies `$SRC_DIR/*`, which skips dotfiles —
so `.claude/` and `.github/` never leave — but `CLAUDE.md` is not a dotfile and
is not excluded, so it goes to wordpress.org with every release and lands in the
zip every user downloads. Whoever reads it has one plugin directory and nothing
else: no `_standards/`, no siblings, no idea what a section number refers to.

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
