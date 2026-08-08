#!/usr/bin/env bash
#
# Run the PHPUnit suite against a real WordPress install, single site.
#
# Docker is the only prerequisite: wp-env brings up WordPress, MySQL and the
# WordPress test library. Dev dependencies are installed INSIDE the container,
# so vendor/ never appears in the repo.
#
#   bash bin/test.sh                 # whole suite
#   bash bin/test.sh --filter Escaping
#
# For the network run use bin/test-multisite.sh. Override the stack with
# WP_ENV_PHP_VERSION / WP_ENV_CORE, exactly as CI does.

set -euo pipefail

SLUG={{SLUG}}
CONFIG="${PHPUNIT_CONFIG:-phpunit.xml.dist}"
CWD=wp-content/plugins/$SLUG

cd "$(dirname "$0")/.."

# Blocks register from build/, which bin/build generates from src/ and which is
# gitignored, so a checkout has none. A runner that skips this fails on a
# checkout that has never been built -- and worse, on a checkout where src/ has
# changed since the last build, silently tests the PREVIOUS build and passes.
#
# Guarded rather than unconditional so this one template serves the plugins
# with blocks and the plugins without: eleven of the nineteen have no src/ and
# no bin/build. A plugin that HAS one but whose runner does not call it is
# caught by bin/verify.py instead.
if [ -f bin/build ]; then
	echo "==> Building blocks"
	bin/build
fi

echo "==> Starting wp-env (PHP ${WP_ENV_PHP_VERSION:-default}, core ${WP_ENV_CORE:-default})"
npx --yes @wordpress/env start

echo "==> Installing dev dependencies inside the tests container"
npx --yes @wordpress/env run tests-cli --env-cwd="$CWD" \
	composer install --no-interaction --no-progress

echo "==> Running PHPUnit ($CONFIG)"
npx --yes @wordpress/env run tests-cli --env-cwd="$CWD" \
	vendor/bin/phpunit -c "$CONFIG" "$@"
