#!/usr/bin/env bash
#
# Run every plugin's PHPUnit suite inside ONE wp-env stack.
#
# The per-plugin bin/test.sh scripts each bring up their own container pair,
# which is right when you are working on a single plugin but wasteful when you
# want to know whether all nineteen still pass. This uses the .wp-env.json in
# this directory, which mounts all nineteen plugins into a single WordPress
# install on ports 8888/8889, so the whole sweep costs one container start.
#
#   bash bin/test-all.sh                    # every plugin, single site
#   bash bin/test-all.sh --multisite        # every plugin, as a network
#   bash bin/test-all.sh wp-polls wp-ban    # just these
#
# Mounting all nineteen at once is also the only way to catch the thing a
# per-plugin run cannot: two plugins claiming the same option row, the same
# global function, the same class name or the same hook.

set -euo pipefail

cd "$(dirname "$0")/.."

CONFIG=phpunit.xml.dist
PLUGINS=()

for arg in "$@"; do
	case "$arg" in
		--multisite)
			CONFIG=phpunit-multisite.xml.dist
			;;
		-*)
			echo "unknown flag: $arg" >&2
			exit 64
			;;
		*)
			PLUGINS+=( "$arg" )
			;;
	esac
done

if [ ${#PLUGINS[@]} -eq 0 ]; then
	# Slug-alphabetical, matching the port table in _standards/STANDARDS.md.
	PLUGINS=(
		freemyinternet
		wp-ban
		wp-commentnavi
		wp-dbmanager
		wp-downloadmanager
		wp-draftsforfriends
		wp-email
		wp-pagenavi
		wp-pluginsused
		wp-polls
		wp-postratings
		wp-postviews
		wp-print
		wp-relativedate
		wp-serverinfo
		wp-showhide
		wp-stats
		wp-sweep
		wp-useronline
	)
fi

echo "==> Starting the all-plugins wp-env (PHP ${WP_ENV_PHP_VERSION:-default}, core ${WP_ENV_CORE:-default})"
npx --yes @wordpress/env start

FAILED=()

for slug in "${PLUGINS[@]}"; do
	CWD=wp-content/plugins/$slug

	echo
	echo "=============================================================="
	echo "==> $slug ($CONFIG)"
	echo "=============================================================="

	npx --yes @wordpress/env run tests-cli --env-cwd="$CWD" \
		composer install --no-interaction --no-progress

	# Keep going after a failure so one broken plugin does not hide the state
	# of the other eighteen. The exit code below still reports the sweep failed.
	#
	# The exit code alone is not enough to tell a pass from a crash. A test that
	# reaches WordPress's real wp_send_json_*() or wp_die() ends in die(), which
	# terminates the PHP process — and therefore PHPUnit — mid-run with status 0.
	# wp-sweep did exactly that under multisite: it stopped at test 96 of 384,
	# printed no summary, and was recorded as passing. So require PHPUnit to
	# have reached its own verdict, and treat a missing verdict as a failure.
	OUT=$(mktemp)

	if ! npx --yes @wordpress/env run tests-cli --env-cwd="$CWD" \
		vendor/bin/phpunit -c "$CONFIG" 2>&1 | tee "$OUT"; then
		FAILED+=( "$slug" )
	elif ! grep -qE '^(OK \(|OK, but |FAILURES!|ERRORS!|No tests executed)' "$OUT"; then
		echo
		echo "==> $slug: PHPUnit exited without a verdict — the process died mid-run."
		echo "    Last line: $(tail -c 200 "$OUT" | tr -d '\n')"
		FAILED+=( "$slug" )
	fi

	rm -f "$OUT"
done

echo
if [ ${#FAILED[@]} -eq 0 ]; then
	echo "==> All ${#PLUGINS[@]} plugin suites passed."
	exit 0
fi

echo "==> ${#FAILED[@]} of ${#PLUGINS[@]} failed: ${FAILED[*]}"
exit 1
