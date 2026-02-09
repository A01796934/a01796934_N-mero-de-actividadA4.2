#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
convertNumbers.py

Read a file containing items (presumably numbers) and convert each valid
decimal integer to binary and hexadecimal using basic algorithms
(no bin(), hex(), format()).

Outputs to console and ConversionResults_<inputFileName>.txt, including elapsed time.
"""

import os
import sys
import time

HEX_DIGITS = "0123456789ABCDEF"


# ---------------------------------------------------------
# Parse integer WITHOUT using int()
# ---------------------------------------------------------
def parse_int(token: str) -> int:
    """Parse a base-10 integer from token without using int()."""
    s = token.strip()

    if not s:
        raise ValueError("Empty token")

    sign = 1
    i = 0

    if s[0] == "-":
        sign = -1
        i = 1
    elif s[0] == "+":
        i = 1

    if i >= len(s):
        raise ValueError("Sign without digits")

    value = 0
    while i < len(s):
        ch = s[i]
        if ch < "0" or ch > "9":
            raise ValueError("Invalid integer")
        value = value * 10 + (ord(ch) - ord("0"))
        i += 1

    return sign * value


# ---------------------------------------------------------
# Convert to binary (base 2) using repeated division
# ---------------------------------------------------------
def to_binary(n: int) -> str:
    """Convert integer n to binary string using basic algorithm."""
    if n == 0:
        return "0"

    sign = ""
    if n < 0:
        sign = "-"
        n = -n

    digits: list[str] = []
    while n > 0:
        digits.append("1" if (n % 2) == 1 else "0")
        n //= 2

    digits.reverse()
    return sign + "".join(digits)


# ---------------------------------------------------------
# Convert to hexadecimal (base 16) using repeated division
# ---------------------------------------------------------
def to_hex(n: int) -> str:
    """Convert integer n to hexadecimal string using basic algorithm."""
    if n == 0:
        return "0"

    sign = ""
    if n < 0:
        sign = "-"
        n = -n

    digits: list[str] = []
    while n > 0:
        digits.append(HEX_DIGITS[n % 16])
        n //= 16

    digits.reverse()
    return sign + "".join(digits)


# ---------------------------------------------------------
# Read tokens from file
# ---------------------------------------------------------
def read_tokens(path: str) -> list[str]:
    """Read whitespace-separated tokens from a text file."""
    tokens: list[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            tokens.extend(line.split())
    return tokens


# ---------------------------------------------------------
# Build output file name based on input file
# ---------------------------------------------------------
def build_output_filename(input_file: str) -> str:
    """Create output filename: ConversionResults_<inputBaseName>.txt."""
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    return f"ConversionResults_{base_name}.txt"


# ---------------------------------------------------------
# Build report lines (console + file)
# ---------------------------------------------------------
def build_report(
    input_file: str,
    tokens: list[str],
) -> tuple[list[str], int, int]:
    """
    Convert tokens and build report lines.

    Returns:
    - lines: report lines
    - valid_count
    - invalid_count
    """
    valid_count = 0
    invalid_count = 0

    lines: list[str] = []
    lines.append("Conversion Results")
    lines.append(f"Input file: {input_file}")
    lines.append("")
    lines.append(f"{'DECIMAL':>12}  {'BINARY':>32}  {'HEXADECIMAL':>12}")
    lines.append(f"{'-' * 12}  {'-' * 32}  {'-' * 12}")

    for t in tokens:
        try:
            n = parse_int(t)
            b = to_binary(n)
            h = to_hex(n)

            lines.append(f"{n:>12}  {b:>32}  {h:>12}")
            valid_count += 1
        except ValueError:
            invalid_count += 1
            msg = f"Invalid token skipped: {t}"
            print(msg)
            lines.append(f"ERROR: {msg}")

    return lines, valid_count, invalid_count


# ---------------------------------------------------------
# Write report to file
# ---------------------------------------------------------
def write_report(path: str, lines: list[str]) -> None:
    """Write report lines to output file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main() -> int:
    """Entry point for the converter program."""
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        return 2

    start = time.perf_counter()
    input_file = sys.argv[1]
    output_file = build_output_filename(input_file)

    try:
        tokens = read_tokens(input_file)
    except OSError as exc:
        print(f"ERROR: Could not read file '{input_file}': {exc}")
        return 1

    lines, valid_count, invalid_count = build_report(input_file, tokens)

    elapsed = time.perf_counter() - start

    lines.append("")
    lines.append(f"Valid items: {valid_count}")
    lines.append(f"Invalid items: {invalid_count}")
    lines.append(f"Elapsed time: {elapsed:.6f} seconds")

    print("\n".join(lines))

    try:
        write_report(output_file, lines)
        print(f"\nResults saved to: {output_file}")
    except OSError as exc:
        print(f"ERROR: Could not write '{output_file}': {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
