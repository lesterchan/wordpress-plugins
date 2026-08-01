# AGENTS.md

This repository is the shared tooling above nineteen WordPress plugins. Each
plugin is its own git repository, cloned side by side here and released to
wordpress.org on its own schedule; the plugin directories are deliberately
untracked (see `.gitignore`).

Start with **[`_standards/STANDARDS.md`](_standards/STANDARDS.md)** — the
contract every plugin is held to, and the reason this repository exists.

Then **[`_standards/RESUME.md`](_standards/RESUME.md)** for the current state:
what is finished, what is in flight, what is known broken, and which findings
are still open. It is written for somebody picking the work up cold.

Each plugin carries its own `CLAUDE.md` and `AGENTS.md` with the briefing for
that plugin. Read the plugin's file for what the code cannot tell you; read the
standard for what applies to all nineteen. Where they disagree, the standard
wins.

`bin/verify.py` checks a plugin against the mechanical half of the standard.
The judgement half — voice, comment density, whether a name earns its place —
is not automatable and is not attempted.
