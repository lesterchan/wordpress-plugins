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
