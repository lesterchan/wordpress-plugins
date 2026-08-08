#!/bin/bash
#
# Deploy one plugin's working tree to its wordpress.org SVN trunk, and commit.
#
#   bin/plugin_deploy.sh wp-polls
#
# Takes the plugin as an argument rather than reading `git rev-parse
# --show-toplevel`, because it lives in the shared repository now instead of on
# $PATH: there is no "current plugin" when you are standing in the root.
#
# **This commits to wordpress.org.** It is the last step of a release, not a
# thing to run to see what happens. What reaches users is the WORKING TREE of
# the plugin directory, not a clean export and not what is committed to git --
# so anything untracked but present on disk ships unless the exclusion list
# below names it.

# The repository this script lives in, whatever directory it is invoked from.
ROOT=$(cd "$(dirname "$0")/.." && pwd)

DIR_NAME=${1%/}   # tab completion adds a trailing slash; drop it

if [ -z "$DIR_NAME" ]; then
	echo "Usage: bin/plugin_deploy.sh <plugin>" >&2
	echo >&2
	echo "  bin/plugin_deploy.sh wp-polls" >&2
	echo >&2
	echo "Deploys that plugin's working tree to ~/svn/wordpress_plugins/<plugin>/trunk" >&2
	echo "and commits it to wordpress.org." >&2
	exit 1
fi

# paths
SRC_DIR=$ROOT/$DIR_NAME
MSG="Deploying $DIR_NAME from GitHub"
BRANCH="trunk"
DEST_DIR=~/svn/wordpress_plugins/$DIR_NAME/$BRANCH

if [ ! -d "$SRC_DIR" ]; then
	echo "$DIR_NAME is not a directory in $ROOT" >&2
	exit 1
fi

# make sure we're deploying from the right dir
if [ ! -d "$SRC_DIR/.git" ]; then
	echo "$SRC_DIR doesn't seem to be a git repository" >&2
	exit 1
fi

if [ ! -d "$(dirname "$DEST_DIR")" ]; then
	echo "No SVN checkout at $(dirname "$DEST_DIR")" >&2
	echo "Nothing has been copied or committed." >&2
	exit 1
fi

# Build first, and refuse to deploy if the build did not work.
#
# This is checked rather than assumed because the rsync below copies the WORKING
# TREE: build/ is gitignored, so what ships is whatever happens to be on disk. A
# build that failed silently -- no Node, a malformed block.json, a webpack error
# -- would leave the previous build there, or nothing at all, and the deploy
# would carry on and publish it. The failure is invisible to a user until they
# notice the plugin's blocks never appear in the editor.
#
# Not `set -e` for the whole script: svn mkdir on an existing directory and the
# rm -rf loop below both fail harmlessly by design, and aborting on those would
# break every deploy.
if [ -d "$SRC_DIR/src" ] && [ ! -f "$SRC_DIR/bin/build" ]; then
	echo "$DIR_NAME has src/ but no bin/build, so build/ cannot be produced." >&2
	echo "Nothing has been copied or committed." >&2
	exit 1
fi

if [ -f "$SRC_DIR/bin/build" ]; then
	if ! "$SRC_DIR/bin/build"; then
		echo >&2
		echo "Build failed, so the deploy is stopping here." >&2
		echo "Nothing has been copied or committed." >&2
		exit 1
	fi
fi

# make sure the destination dir exists
svn mkdir $DEST_DIR 2> /dev/null
svn add $DEST_DIR 2> /dev/null

# delete everything except .svn dirs
for file in $(find $DEST_DIR/* -not -path "*.svn*")
do
	rm -rf $file 2>/dev/null
done

# copy everything over from git
#
# Everything here is developer tooling or a dependency tree: none of it belongs
# in trunk, and node_modules in particular would ship thousands of files to
# every user if a plugin ever grew a local npm install.
#
# The config entries are globbed rather than named exactly. These tools all take
# a base config plus variants -- a .dist, an .override, a second ruleset or test
# suite -- and an exact-name exclusion silently ships the variant. wp-postratings
# grew a phpunit-multisite config and it would have gone straight to trunk.
RSYNC_EXCLUDES=(
	--exclude='*.git*'
	--exclude='vendor'
	--exclude='.idea'
	--exclude='.travis.yml'
	--exclude='.editorconfig'
	--exclude='phpcs*.xml*'
	--exclude='node_modules'
	--exclude='package.json'
	--exclude='package-lock.json'
	--exclude='.nvmrc'
	--exclude='.eslintrc*'
	--exclude='.eslintignore'
	--exclude='eslint.config.*'
	--exclude='.prettierrc*'
	--exclude='prettier.config.*'
	--exclude='tests'
	--exclude='phpunit*.xml*'
	--exclude='.phpunit.result.cache'
	--exclude='composer.json'
	--exclude='composer.lock'
	--exclude='.wp-env*.json'
	--exclude='playwright.config.*'
	--exclude='vitest.config.*'
	--exclude='vite.config.*'
	# Block sources. Unbuilt JSX is of no use to a site, and this rsyncs the
	# working tree rather than a clean export, so the first plugin to grow a
	# src/ directory would ship its sources without this line. Added while no
	# plugin has one yet, which is the only time this costs nothing.
	#
	# Do NOT add build/ alongside it, however symmetrical the pair looks:
	# build/ is what register_block_type_from_metadata() loads at runtime, so
	# excluding it ships a plugin whose blocks cannot render.
	--exclude='src'
	# bin/build is invoked above, before this rsync, so excluding bin here
	# cannot break it -- it only stops build and test scripts shipping. That
	# ordering is also what makes the src/ exclusion above safe: the build has
	# already turned src/ into build/ by the time anything is copied.
	--exclude='bin'
	# Agent briefings. .claude/ would be skipped anyway -- the rsync source is
	# $SRC_DIR/*, and that glob does not match dotfiles -- but it is named here
	# for the same reason .idea and .editorconfig are: relying on a glob's quirk
	# to keep a directory out of trunk is not obvious to the next person reading
	# this list. CLAUDE.md and AGENTS.md are not dotfiles and genuinely were
	# shipping: both went to wordpress.org with every release and landed in the
	# zip every user downloads.
	--exclude='CLAUDE.md'
	--exclude='AGENTS.md'
	--exclude='.claude'
	# Playwright's output: traces, failure screenshots, and -- the reason this
	# matters -- storage-states/admin.json, a logged-in WordPress session cookie
	# for the local test container.
	#
	# It is in every plugin's .gitignore, which is exactly why it was missed:
	# this script rsyncs the *working tree*, not a clean export, so anything
	# untracked but present on disk ships. Running the browser suite once and
	# deploying afterwards was enough to publish it.
	--exclude='artifacts'
	# The $SRC_DIR/* glob skips dotfiles, but only the ones at the top level:
	# --recursive then copies everything *inside* the directories it matched,
	# dotfiles included. So includes/.DS_Store ships while ./.DS_Store does not.
	# Finder writes those into any folder somebody opens.
	--exclude='.DS_Store'
)
rsync --recursive "${RSYNC_EXCLUDES[@]}" $SRC_DIR/* $DEST_DIR

cd $DEST_DIR

# check .svnignore
for file in $(cat "$SRC_DIR/.svnignore" 2> /dev/null)
do
	rm -rf $DEST_DIR/$file
done

# Transform the readme
if [ -f README.md ]; then
	mv README.md readme.txt
	sed -i '' -e 's/```php/~~~/' -e 's/```javascript/~~~/' -e 's/```/~~~/' readme.txt
	#sed -i '' -e 's///g' readme.txt
fi

# svn addremove
svn stat | awk '/^\?/ {print $2}' | xargs svn add > /dev/null 2>&1
svn stat | awk '/^\!/ {print $2}' | xargs svn rm --force

svn stat

svn ci -m "$MSG"
