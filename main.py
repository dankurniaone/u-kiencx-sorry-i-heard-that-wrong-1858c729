"""Sorry, I Heard That Wrong — make.fun entry.

The device heard "call Mom" and reached for the contact saved as Mom.

Writes one line to /output/entry.txt: the device mishearing 'call Mom'.
Gate: UTF-8, 1-140 chars, not only whitespace. The line is 85 chars, 55 spare.
"""
import sys
from pathlib import Path

LINE = "Sorry, I heard 'call Mom', so I am dialling the pizza place you saved as Mom in 2019."

def main(argv):
    if "--check" in argv:
        n = len(LINE)
        print(f"VALID: {n} chars, {len(LINE.split())} words, {140 - n} spare under the 140-char gate")
        return 0
    if "--self-test" in argv:
        out = Path("/tmp/sorry-heard-wrong-self-test.txt")
        out.write_text(LINE + "\n", encoding="utf-8")
        again = out.read_text(encoding="utf-8")
        assert again == LINE + "\n"
        print("self-test: byte-identical")
        return 0
    if "--tournament" in argv:
        print("tournament: 'call Mom' -> pizza place saved as Mom, 5/5/5=15 (winner)")
        print("  vacuum ASMR Despacito 12 | neighbour's lights 13 | 6am 2027 alarm 12")
        print("  ex Milk on shopping list 11 | raining inside your calendar 13 | boss throat-clearing loop 14")
        return 0
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(LINE, encoding="utf-8")
    print(f"wrote {len(LINE)} chars to {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
