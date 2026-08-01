#!/usr/bin/env bash
#
# Fill the development site at the root harness with the same fixtures the E2E
# suites create, so the plugins can be clicked through rather than read about.
#
#   bin/seed-demo.sh              # 200 posts, 100 comments
#   bin/seed-demo.sh 500 250      # as much as you like
#
# Safe to run again: everything it creates is marked, and a second run clears
# what the first one made and nothing else.
#
set -euo pipefail

cd "$(dirname "$0")/.."

POSTS="${1:-200}"
COMMENTS="${2:-100}"

# Matches DEMO_PER_PAGE in _standards/demo/seed.php.
PER_PAGE=5

PORT=$(node -p "require('./.wp-env.json').port")

echo "==> Starting the root wp-env (all nineteen plugins)"
npx --yes @wordpress/env start

echo "==> Activating every plugin"
# Activating them one command at a time would cost a couple of seconds each.
npx --yes @wordpress/env run cli wp plugin activate --all

echo "==> Activating a theme"
# A classic theme: the demo shim hooks loop_end and comment_form_before, which
# is where a classic theme's own navigation calls sit.
npx --yes @wordpress/env run cli wp theme activate twentytwentyone

echo "==> Seeding content"
npx --yes @wordpress/env run cli wp eval-file wp-content/demo/seed.php "$POSTS" "$COMMENTS"

echo
echo "Ready: http://localhost:${PORT}"
echo "  Front page          ${POSTS} posts, $(( ( POSTS + PER_PAGE - 1 ) / PER_PAGE )) pages, WP-PageNavi under the loop"
echo "  A much discussed    ${COMMENTS} comments, $(( ( COMMENTS + PER_PAGE - 1 ) / PER_PAGE )) pages, WP-CommentNavi under the list"
echo "  Show and hide       three [showhide] blocks, one open, two side by side"
echo "  Rate this post      the [ratings] control and its read-only twin"
echo "  Relative dates      the shortcodes, and every post date rendered relative"
echo
echo "  wp-admin            http://localhost:${PORT}/wp-admin (admin / password)"
