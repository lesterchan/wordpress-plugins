"""
Count PHPUnit assertions that carry a failure message, per assertion name.

The naive regex the earlier counts used cannot do this: PHPUnit's $message
argument sits at a different position for every assertion, so "has more than N
arguments" is only meaningful once you know N for that specific name. This
walks each call, splits its arguments at the top level -- respecting nesting,
strings and escapes -- and compares the count against the arity table below.

Anything not in the table is reported separately rather than guessed at.
"""

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Required arguments BEFORE $message, by assertion name.
ARITY = {}

for name in """assertTrue assertFalse assertNull assertNotNull assertEmpty
assertNotEmpty assertIsArray assertIsString assertIsInt assertIsBool
assertIsFloat assertIsObject assertIsCallable assertIsNumeric assertIsIterable
assertIsNotArray assertIsNotString assertIsNotInt assertIsNotBool
assertFileExists assertFileDoesNotExist assertFileNotExists
assertDirectoryExists assertDirectoryDoesNotExist assertIsReadable
assertIsWritable assertNan assertFinite assertInfinite assertWPError
assertNotWPError assertQueryTrue assertJson assertNotFalse assertIsResource""".split():
    ARITY[name] = 1

for name in """assertSame assertNotSame assertEquals assertNotEquals
assertContains assertNotContains assertStringContainsString
assertStringNotContainsString assertStringContainsStringIgnoringCase
assertArrayHasKey assertArrayNotHasKey assertInstanceOf assertNotInstanceOf
assertGreaterThan assertLessThan assertGreaterThanOrEqual
assertLessThanOrEqual assertCount assertNotCount assertStringStartsWith
assertStringEndsWith assertStringStartsNotWith assertStringEndsNotWith
assertMatchesRegularExpression assertDoesNotMatchRegularExpression
assertRegExp assertNotRegExp assertObjectHasProperty
assertObjectNotHasProperty assertObjectHasAttribute assertSameSize
assertEqualsCanonicalizing assertEqualsIgnoringCase assertJsonStringEqualsJsonString
assertFileEquals assertStringEqualsFile assertEqualSets assertEqualSetsWithIndex
assertSameSets assertSameSetsWithIndex assertContainsOnlyInstancesOf
assertDiscardWhitespace assertStringNotContainsStringIgnoringCase""".split():
    ARITY[name] = 2

for name in "assertEqualsWithDelta assertNotEqualsWithDelta".split():
    ARITY[name] = 3

CALL = re.compile(r"\$this->(assert[A-Za-z]+)\s*\(")


def split_args(src, start):
    """Split the argument list opening at src[start] == '('.

    Returns (list_of_arg_strings, index_after_closing_paren) or (None, None)
    if the call never closes -- which would mean the file does not parse.
    """
    depth = 0
    args = []
    current = []
    i = start
    quote = None

    while i < len(src):
        ch = src[i]

        if quote:
            if ch == "\\":
                current.append(src[i:i + 2])
                i += 2
                continue
            if ch == quote:
                quote = None
            current.append(ch)
            i += 1
            continue

        if ch in "'\"":
            quote = ch
            current.append(ch)
            i += 1
            continue

        if ch in "([{":
            depth += 1
            if depth == 1:
                i += 1
                continue
            current.append(ch)
            i += 1
            continue

        if ch in ")]}":
            depth -= 1
            if depth == 0:
                args.append("".join(current).strip())
                return [a for a in args if a != ""], i + 1
            current.append(ch)
            i += 1
            continue

        if ch == "," and depth == 1:
            args.append("".join(current).strip())
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    return None, None


def main(roots):
    per_name = defaultdict(lambda: [0, 0])   # name -> [total, with_message]
    per_plugin = defaultdict(lambda: [0, 0])
    unknown = Counter()

    for root in roots:
        plugin = Path(root).name
        for php in sorted(Path(root).glob("tests/**/*.php")):
            src = php.read_text(encoding="utf-8", errors="replace")
            for m in CALL.finditer(src):
                name = m.group(1)
                args, _ = split_args(src, m.end() - 1)
                if args is None:
                    continue
                if name not in ARITY:
                    unknown[name] += 1
                    continue
                has_message = len(args) > ARITY[name]
                per_name[name][0] += 1
                per_plugin[plugin][0] += 1
                if has_message:
                    per_name[name][1] += 1
                    per_plugin[plugin][1] += 1

    total = sum(v[0] for v in per_name.values())
    withmsg = sum(v[1] for v in per_name.values())

    print(f"TOTAL {total} assertions, {withmsg} carry a message "
          f"({100 * withmsg / total:.1f} %), {total - withmsg} do not\n")

    print("--- by plugin: missing / total (percent missing) ---")
    for plugin, (t, w) in sorted(per_plugin.items(),
                                 key=lambda kv: -(kv[1][0] - kv[1][1])):
        print(f"{plugin:22} {t - w:5} / {t:5}  ({100 * (t - w) / t:5.1f} %)")

    print("\n--- by assertion: missing / total, top 25 ---")
    for name, (t, w) in sorted(per_name.items(),
                               key=lambda kv: -(kv[1][0] - kv[1][1]))[:25]:
        print(f"{name:38} {t - w:5} / {t:5}")

    if unknown:
        print("\n--- NOT IN THE ARITY TABLE (excluded from every number above) ---")
        for name, count in unknown.most_common():
            print(f"{name:38} {count:5}")


if __name__ == "__main__":
    main(sys.argv[1:])
