#!/usr/bin/env python3
"""Sorry, I Heard That Wrong.

The smart speaker mishears its human and dials the wrong "Mom".

Gate: /output/entry.txt holds UTF-8 text, 1 to 140 characters, not only
whitespace. The chosen line runs 85 characters, so 55 characters sit spare.
Judge order: humour first, freshness second, then how much the line sounds
like the device itself. One tight line, every word earning its place.
"""

import sys
from pathlib import Path

ENTRY = "Sorry, I heard 'call Mom', so I am dialling the pizza place you saved as Mom in 2019."
LIMIT = 140
OUT = Path("/output/entry.txt")

CANDIDATES = [
    # (line, specificity, surprise, freshness)
    ("Sorry, I heard 'call Mom', so I am dialling the pizza place you saved as Mom in 2019.", 5, 5, 5),
    ("I heard 'turn off the lights' and now the whole street is dark. Sorry, neighbour.", 4, 4, 5),
    ("Your 6am alarm is set for 2027. I did not want to assume you meant today.", 4, 4, 4),
    ("I heard 'play Despacito' as 'vacuum ASMR'. The floor has never been cleaner.", 4, 4, 4),
    ("It is raining inside your calendar. I have booked you an umbrella for Tuesday.", 4, 5, 4),
    ("You said 'call my ex'. I added milk to the shopping list instead. You are welcome.", 4, 3, 4),
    ("I heard your boss clear his throat and now I am stuck in a meeting loop. Send help.", 4, 4, 3),
]


def pick():
    ranked = sorted(CANDIDATES, key=lambda c: (c[1] + c[2] + c[3], c[1], c[2]), reverse=True)
    return ranked[0][0]


def check():
    text = pick()
    chars = len(text)
    words = len(text.split())
    status = "VALID" if 1 <= chars <= LIMIT and text.strip() else "INVALID"
    print(f"{status}: {chars} chars, {words} words, {LIMIT - chars} spare under the {LIMIT}-char gate")
    return 0 if status == "VALID" else 1


def self_test():
    probe = Path("/tmp/sorry-heard-wrong-self-test.txt")
    text = pick()
    probe.write_text(text + "\n", encoding="utf-8")
    again = probe.read_text(encoding="utf-8")
    assert again == text + "\n", "round-trip mismatch"
    print("self-test: byte-identical")
    return 0


def show_tournament():
    print("tournament (specificity / surprise / freshness):")
    ranked = sorted(CANDIDATES, key=lambda c: c[1] + c[2] + c[3], reverse=True)
    for i, (line, spec, surp, fresh) in enumerate(ranked):
        mark = "  <-- winner" if i == 0 else ""
        print(f"  {spec}/{surp}/{fresh} = {spec + surp + fresh:2d}  {line}{mark}")
    return 0


def write_entry():
    text = pick()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {len(text)} chars to {OUT}")
    return 0


def main(argv):
    if "--check" in argv:
        return check()
    if "--self-test" in argv:
        return self_test()
    if "--tournament" in argv:
        return show_tournament()
    return write_entry()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
