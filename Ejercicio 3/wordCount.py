#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
wordCount.py

Read a file containing words (presumably between spaces) and compute:
- All distinct words
- Frequency of each word

Outputs:
WordCountResults_<inputFileName>.txt

Uses only basic algorithms (no external libraries).
"""

import sys
import time
import os


# ---------------------------------------------------------
# Basic string helpers
# ---------------------------------------------------------
def is_letter_or_digit(ch: str) -> bool:
    """Return True if character is alphanumeric."""
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ("0" <= ch <= "9")


def normalize_word(raw: str) -> str:
    """
    Normalize a word:
    - remove punctuation at edges
    - convert to lowercase
    - return empty string if invalid
    """
    s = raw.strip()

    if not s:
        return ""

    left = 0
    right = len(s) - 1

    while left <= right and not is_letter_or_digit(s[left]):
        left += 1

    while right >= left and not is_letter_or_digit(s[right]):
        right -= 1

    if left > right:
        return ""

    return s[left : right + 1].lower()


# ---------------------------------------------------------
# File reading
# ---------------------------------------------------------
def read_tokens(path: str) -> list[str]:
    """Read whitespace-separated tokens from file."""
    tokens: list[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            tokens.extend(line.split())

    return tokens


# ---------------------------------------------------------
# Sorting (selection sort)
# ---------------------------------------------------------
def selection_sort_strings(values: list[str]) -> list[str]:
    """Sort list of strings using selection sort."""
    arr = values[:]
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


# ---------------------------------------------------------
# Word counting
# ---------------------------------------------------------
def count_words(tokens: list[str]) -> tuple[dict[str, int], int, int]:
    """
    Count words and return:
    counts dictionary,
    number of valid words,
    number of invalid tokens.
    """
    counts: dict[str, int] = {}
    valid = 0
    invalid = 0

    for token in tokens:
        word = normalize_word(token)

        if not word:
            invalid += 1
            print(f"Invalid token skipped: {token}")
            continue

        valid += 1

        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts, valid, invalid


# ---------------------------------------------------------
# Build output report
# ---------------------------------------------------------
def build_report(
    input_file: str,
    counts: dict[str, int],
    valid: int,
    invalid: int,
    elapsed: float,
) -> list[str]:
    """Create report lines for console and file."""
    words_sorted = selection_sort_strings(list(counts.keys()))

    lines: list[str] = []

    lines.append("Word Count Results")
    lines.append(f"Input file: {input_file}")
    lines.append("")
    lines.append(f"Valid words: {valid}")
    lines.append(f"Invalid tokens: {invalid}")
    lines.append(f"Distinct words: {len(words_sorted)}")
    lines.append("")
    lines.append(f"{'WORD':<25} {'COUNT':>10}")
    lines.append("-" * 36)

    for w in words_sorted:
        lines.append(f"{w:<25} {counts[w]:>10}")

    lines.append("")
    lines.append(f"Elapsed time: {elapsed:.6f} seconds")

    return lines


# ---------------------------------------------------------
# Write report
# ---------------------------------------------------------
def write_report(path: str, lines: list[str]) -> None:
    """Write lines to output file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main() -> int:
    """Program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        return 2

    start = time.perf_counter()

    input_file = sys.argv[1]

    # 🔥 NEW FEATURE → dynamic output name
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"WordCountResults_{base_name}.txt"

    try:
        tokens = read_tokens(input_file)
    except OSError as exc:
        print(f"ERROR: Could not read file '{input_file}': {exc}")
        return 1

    counts, valid, invalid = count_words(tokens)

    elapsed = time.perf_counter() - start

    lines = build_report(input_file, counts, valid, invalid, elapsed)

    print("\n".join(lines))

    try:
        write_report(output_file, lines)
        print(f"\nResults saved to: {output_file}")
    except OSError as exc:
        print(f"ERROR: Could not write file: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
