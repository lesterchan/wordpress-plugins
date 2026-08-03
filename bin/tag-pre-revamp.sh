#!/usr/bin/env bash
# Tag each plugin's last release before the 2026 rewrite, and push it.
#
# The commits are fixed, so this runs from any clone. Clones made with
# --depth may not contain them: run `git fetch --unshallow origin` first.
#
#   ./tag-pre-revamp.sh [directory holding the 19 plugin repos]   (default: .)
#
# Re-running is safe: a tag that already exists is left alone.
set -u
BASE="${1:-.}"
fail=0

tag() {
  slug=$1; ver=$2; sha=$3; date=$4; subject=$5; extra=${6:-}
  repo="$BASE/$slug"
  if [ ! -d "$repo/.git" ]; then echo "SKIP $slug: no repo at $repo"; fail=1; return; fi
  if git -C "$repo" rev-parse -q --verify "refs/tags/$ver" >/dev/null; then
    echo "have $slug $ver"
  elif ! git -C "$repo" cat-file -e "$sha^{commit}" 2>/dev/null; then
    echo "SKIP $slug: $sha not in this clone -- git -C $repo fetch --unshallow origin"; fail=1; return
  else
    git -C "$repo" tag -a "$ver" "$sha" -m "$ver - the last release before the 2026 rewrite

Marks $slug as it shipped before the consistency programme began:

    $sha $date
    $subject

Everything after this commit is the rewrite to the shared standard in
github.com/lesterchan/wordpress-plugins, _standards/STANDARDS.md.$extra" || { fail=1; return; }
    echo "tagged $slug $ver"
  fi
  git -C "$repo" push origin "refs/tags/$ver" || fail=1
}

tag freemyinternet         0.01      8a7a7a59cc9aae05585a0c24b528f0693cce683a 2020-05-20 Bump\ \'Tested\ up\ to\'\ to\ 5.4 ''
tag wp-ban                 1.69.2    8f5452ac3ad2581ef0b951e674c8741d1e5bc01d 2025-03-09 Don\'t\ allow\ to\ access\ ban-options\ directly ''
tag wp-commentnavi         1.12.2    45b51b7d09cafb6c00af5c0bfcfd50687d9cad87 2023-08-09 Bump\ \'Tested\ up\ to\'\ to\ 6.3 ''
tag wp-dbmanager           2.80.10   b7ad9070db5015da01ddf4312c783ded4b0cef44 2024-11-24 Don\'t\ throw\ fatal\ error\ if\ unknown\ .sql\ files\ are\ inside\ the\ database\ backup\ folder. ''
tag wp-downloadmanager     1.69.1    416b9f5459496166c0395f9e055d4c4cf872404a 2026-02-13 Don\'t\ allow\ Path\ Traversal ''
tag wp-draftsforfriends    1.0.2     952592aa8de8fbe3126b46941d04107222a43fbe 2023-08-09 Bump\ \'Tested\ up\ to\'\ to\ 6.3 ''
tag wp-email               2.69.3    066014a931c4726d5d265a2bfad3f8a75bd5f9d6 2024-12-18 Remove\ email_text_domain\(\) $'\n\nThe plugin header at this commit reads Version: 2.69.2. The Stable tag is\nthe authority for what wordpress.org served, and it reads 2.69.3, so this\ntree shipped as 2.69.3 with the header left behind.'
tag wp-pagenavi            2.94.5    3a010444c30935ad4817d47cee6db3d9eb0a04ea 2024-12-19 Fix\ readme\ typo ''
tag wp-pluginsused         1.50.2    7cff1208433487127ba52368434db20f2714bd47 2023-08-09 Bump\ \'Tested\ up\ to\'\ to\ 6.3 ''
tag wp-polls               2.77.4    50adb772515258de5a094d4d1f91ffe6ac297dc1 2025-12-26 Remove\ duplicated\ shortcode\ #162 ''
tag wp-postratings         1.91.2    75e54f4f3876980a7bec6056117ab65fea213579 2024-07-16 Fixed\ XSS\ in\ Google\ Rich\ Text\ Snippets ''
tag wp-postviews           1.78      9b1c2c848cda67e996756adb498debf2a7f5ec25 2026-01-16 Bump\ Copyright\ and\ Tested\ To ''
tag wp-print               2.58.2    dde8f97cabc5571426dde431fe82293bc45aeed6 2023-09-08 Merge\ pull\ request\ #16\ from\ zoheirkabuli/rtl ''
tag wp-relativedate        1.51      b7fa2f8dbb978076929835739325025557ae90db 2023-08-09 Bump\ \'Tested\ up\ to\'\ to\ 6.3 ''
tag wp-serverinfo          1.66      a7dc3cfea95f690761befaf10dede7ae95b78957 2026-06-16 Merge\ pull\ request\ #15\ from\ lesterchan/claude/issue-10-20260616-1447 ''
tag wp-showhide            1.06      a1a0ee216ab49507a92657c4474e4f656bbde3fb 2025-11-28 Use\ esc_html\(\)\ to\ fix\ XSS ''
tag wp-stats               2.56.1    22839ce3084e3e372784e7e0d6930d035c9cb416 2026-06-22 Escape\ all\ inputs ''
tag wp-sweep               1.2.0     cff61a76242206573141d110683b01aa5cd20016 2026-06-19 Bump\ to\ 1.2.0\ and\ document\ available\ filters\ in\ README ''
tag wp-useronline          2.88.9    14d4edc203dcdd591efee9c58d3e8e5a6574401c 2025-07-15 Merge\ pull\ request\ #65\ from\ portalvasco/patch-33 ''

exit $fail
