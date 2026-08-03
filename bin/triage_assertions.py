"""Split the message-less assertions into 'a message is owed' and 'it is not'.

PHPUnit prints a diff of expected against actual for the comparing assertions,
so `assertSame( 'Today', relative_comment_date( 'DATE' ) )` already fails
legibly. It prints nothing useful for the predicate ones -- "Failed asserting
that false is true" names neither the subject nor the expectation -- and it
cannot say which pass of a loop failed. Those are where a message is owed.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from measure_assertions import ARITY, CALL, split_args
from collections import Counter

# Assertions whose failure output carries no expected-vs-actual diff.
OPAQUE = {n for n, a in ARITY.items() if a == 1} | {
    "assertCount", "assertNotCount", "assertArrayHasKey", "assertArrayNotHasKey",
    "assertInstanceOf", "assertNotInstanceOf", "assertObjectHasProperty",
    "assertObjectNotHasProperty", "assertMatchesRegularExpression",
    "assertDoesNotMatchRegularExpression", "assertGreaterThan", "assertLessThan",
    "assertGreaterThanOrEqual", "assertLessThanOrEqual", "assertSameSize",
}
LOOP = re.compile(r"\b(foreach|for|while)\s*\(")

owed_opaque = Counter()
owed_loop = Counter()
not_owed = Counter()

for root in sys.argv[1:]:
    plugin = Path(root).name
    for php in sorted(Path(root).glob("tests/**/*.php")):
        src = php.read_text(encoding="utf-8", errors="replace")
        lines = src.split("\n")
        for m in CALL.finditer(src):
            name = m.group(1)
            if name not in ARITY:
                continue
            args, _ = split_args(src, m.end() - 1)
            if args is None or len(args) > ARITY[name]:
                continue
            line_no = src.count("\n", 0, m.start())
            indent = len(lines[line_no]) - len(lines[line_no].lstrip("\t"))
            in_loop = False
            for i in range(line_no - 1, max(0, line_no - 40), -1):
                l = lines[i]
                if not l.strip():
                    continue
                ind = len(l) - len(l.lstrip("\t"))
                if ind < indent and LOOP.search(l):
                    in_loop = True
                    break
                if ind < indent and re.search(r"function\s+\w+", l):
                    break
            if in_loop:
                owed_loop[plugin] += 1
            elif name in OPAQUE:
                owed_opaque[plugin] += 1
            else:
                not_owed[plugin] += 1

plugins = sorted(set(owed_opaque) | set(owed_loop) | set(not_owed))
print(f"{'plugin':22} {'opaque':>7} {'in loop':>8} {'OWED':>6} {'diffs ok':>9}")
to = tl = tn = 0
for p in sorted(plugins, key=lambda p: -(owed_opaque[p] + owed_loop[p])):
    o, l, n = owed_opaque[p], owed_loop[p], not_owed[p]
    to += o; tl += l; tn += n
    print(f"{p:22} {o:7} {l:8} {o + l:6} {n:9}")
print(f"{'TOTAL':22} {to:7} {tl:8} {to + tl:6} {tn:9}")
