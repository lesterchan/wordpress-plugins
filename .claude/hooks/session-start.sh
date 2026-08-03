#!/bin/bash
#
# Install the toolchain that gates these repositories.
#
# CI runs three families of check and this session can reproduce two of them.
# Getting that wrong is expensive: `php -l` and `bin/verify.py` both pass on
# code phpcs rejects, and treating them as the gate put four red commits on
# master in one afternoon. So the point of this hook is to make the real
# checks runnable before any work starts.
#
#   phpcs + WPCS  -> the "PHP coding standards" job, and the one most often
#                    tripped: a docblock description must start with a capital
#                    letter, and a string with nothing to interpolate must use
#                    single quotes.
#   Node 24       -> what CI pins. The npm that ships with Node 22 resolves
#                    vite's optional `yaml` peer differently and calls every
#                    lockfile here out of sync, which is a false alarm that has
#                    already cost a debugging session.
#   Docker        -> installed but not running by default. wp-env needs it.
#
# PHPUnit and Playwright still will not run: wp-env downloads WordPress from
# *.wordpress.org, and this session's egress policy blocks that host. Docker
# itself is fine. See the note at the end of the run.

set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
	exit 0
fi

log() { printf '==> %s\n' "$1"; }

# --- Node 24, to match ci.yml -----------------------------------------------
# nvm ships as a shell function rather than a binary, so it has to be sourced.
export NVM_DIR="${NVM_DIR:-/opt/nvm}"

if [ -s "$NVM_DIR/nvm.sh" ]; then
	# shellcheck disable=SC1091
	. "$NVM_DIR/nvm.sh"

	if ! nvm which 24 >/dev/null 2>&1; then
		log "Installing Node 24 (CI pins it; npm 10 misreads these lockfiles)"
		nvm install 24 >/dev/null
	fi

	nvm use 24 >/dev/null
	NODE_BIN="$(dirname "$(nvm which 24)")"

	if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
		echo "export NVM_DIR=\"$NVM_DIR\"" >> "$CLAUDE_ENV_FILE"
		echo "export PATH=\"$NODE_BIN:\$PATH\"" >> "$CLAUDE_ENV_FILE"
	fi

	log "Node $(node --version), npm $(npm --version)"
else
	log "nvm not found at $NVM_DIR; leaving Node as it is"
fi

# --- phpcs and WPCS, exactly as ci.yml installs them ------------------------
export COMPOSER_ALLOW_SUPERUSER=1

PHPCS_BIN="$(composer global config bin-dir --absolute 2>/dev/null || true)"

if [ -z "$PHPCS_BIN" ] || [ ! -x "$PHPCS_BIN/phpcs" ]; then
	log "Installing phpcs + WPCS"
	composer global config --no-plugins allow-plugins.dealerdirect/phpcodesniffer-composer-installer true >/dev/null 2>&1
	composer global require --no-interaction --no-progress \
		squizlabs/php_codesniffer wp-coding-standards/wpcs >/dev/null 2>&1
	PHPCS_BIN="$(composer global config bin-dir --absolute 2>/dev/null)"
fi

if [ -x "$PHPCS_BIN/phpcs" ]; then
	if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
		echo "export PATH=\"$PHPCS_BIN:\$PATH\"" >> "$CLAUDE_ENV_FILE"
		echo "export COMPOSER_ALLOW_SUPERUSER=1" >> "$CLAUDE_ENV_FILE"
	fi

	log "$("$PHPCS_BIN/phpcs" --version)"
	log "Run it from INSIDE a plugin directory, or it misses that plugin's phpcs.xml"
	log "and reports tens of thousands of issues out of vendor/:  cd <plugin> && phpcs -q ."
else
	log "phpcs did not install; the PHP coding standards job cannot be reproduced here"
fi

# --- Docker, for wp-env -----------------------------------------------------
if command -v docker >/dev/null 2>&1; then
	if ! docker info >/dev/null 2>&1; then
		log "Starting the Docker daemon"
		( sudo -n dockerd >/tmp/dockerd.log 2>&1 & ) || true

		for _ in $(seq 1 15); do
			docker info >/dev/null 2>&1 && break
			sleep 1
		done
	fi

	if docker info >/dev/null 2>&1; then
		log "Docker is up"
	else
		log "Docker would not start; see /tmp/dockerd.log"
	fi
fi

# --- What still will not work, said plainly ---------------------------------
log "PHPUnit and Playwright need wp-env, which downloads WordPress from"
log "*.wordpress.org. That host is blocked by this session's egress policy, so"
log "those two suites can only be run by CI. phpcs and bin/verify.py cover the rest."
