#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
computeStatistics.py

Compute descriptive statistics (mean, median, mode, variance,
standard deviation) from a file using only basic algorithms.

Outputs results to console and StatisticsResults_<inputFileName>.txt.
"""

import os
import sys
import time


# ---------------------------------------------------------
# Parse number WITHOUT using int() or float()
# ---------------------------------------------------------
def parse_number(token: str) -> float:
    """Convert string token to float manually. Raise ValueError if invalid."""
    s = token.strip()

    if not s:
        raise ValueError("Empty token")

    sign = 1.0
    i = 0

    if s[0] == "-":
        sign = -1.0
        i = 1
    elif s[0] == "+":
        i = 1

    int_part = 0
    has_digit = False

    while i < len(s) and "0" <= s[i] <= "9":
        has_digit = True
        int_part = int_part * 10 + (ord(s[i]) - ord("0"))
        i += 1

    frac_part = 0
    frac_div = 1

    if i < len(s) and s[i] == ".":
        i += 1
        while i < len(s) and "0" <= s[i] <= "9":
            has_digit = True
            frac_part = frac_part * 10 + (ord(s[i]) - ord("0"))
            frac_div *= 10
            i += 1

    if not has_digit or i != len(s):
        raise ValueError("Invalid number")

    return sign * (int_part + frac_part / frac_div)


# ---------------------------------------------------------
# Square root using Newton method
# ---------------------------------------------------------
def sqrt_newton(x: float) -> float:
    """Compute square root without math.sqrt using Newton iteration."""
    if x == 0.0:
        return 0.0

    guess = x if x >= 1.0 else 1.0
    for _ in range(25):
        guess = 0.5 * (guess + x / guess)

    return guess


# ---------------------------------------------------------
# Read tokens from file
# ---------------------------------------------------------
def read_tokens(path: str) -> list[str]:
    """Read whitespace-separated tokens from file."""
    tokens: list[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            tokens.extend(line.split())

    return tokens


# ---------------------------------------------------------
# Basic selection sort
# ---------------------------------------------------------
def selection_sort(values: list[float]) -> list[float]:
    """Return sorted copy using selection sort."""
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
# Mean
# ---------------------------------------------------------
def mean(values: list[float]) -> float:
    """Compute arithmetic mean."""
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


# ---------------------------------------------------------
# Median
# ---------------------------------------------------------
def median(sorted_vals: list[float]) -> float:
    """Compute median from sorted values."""
    n = len(sorted_vals)
    mid = n // 2

    if n % 2 == 1:
        return sorted_vals[mid]

    return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


# ---------------------------------------------------------
# Mode
# ---------------------------------------------------------
def mode(values: list[float]) -> list[float]:
    """Compute mode(s). Return empty list if no repeats."""
    counts: dict[float, int] = {}

    for v in values:
        counts[v] = counts.get(v, 0) + 1

    max_count = 0

    # pylint: disable=consider-using-max-builtin
    for c in counts.values():
        if c > max_count:
            max_count = c

    if max_count <= 1:
        return []

    modes: list[float] = []
    for k, c in counts.items():
        if c == max_count:
            modes.append(k)

    return modes


# ---------------------------------------------------------
# Variance
# ---------------------------------------------------------
def variance(values: list[float], avg: float) -> float:
    """Compute population variance."""
    total = 0.0

    for v in values:
        diff = v - avg
        total += diff * diff

    return total / len(values)


# ---------------------------------------------------------
# Build output file name based on input file
# ---------------------------------------------------------
def build_output_filename(input_file: str) -> str:
    """Create output filename: StatisticsResults_<inputBaseName>.txt."""
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    return f"StatisticsResults_{base_name}.txt"


# ---------------------------------------------------------
# Build report lines
# ---------------------------------------------------------
def build_report(
    input_file: str,
    values: list[float],
    invalid_count: int,
    elapsed: float,
) -> list[str]:
    """Build output report lines for console and file."""
    sorted_vals = selection_sort(values)

    avg = mean(values)
    med = median(sorted_vals)
    modes = mode(values)
    var = variance(values, avg)
    std = sqrt_newton(var)

    lines = [
        "Statistics Results",
        f"Input file: {input_file}",
        f"Count: {len(values)}",
        f"Invalid: {invalid_count}",
        "",
        f"Mean: {avg:.6f}",
        f"Median: {med:.6f}",
        f"Mode: {modes if modes else 'None'}",
        f"Variance: {var:.6f}",
        f"Std Dev: {std:.6f}",
        "",
        f"Elapsed time: {elapsed:.6f} seconds",
    ]

    return lines


# ---------------------------------------------------------
# Write report to file
# ---------------------------------------------------------
def write_report(path: str, lines: list[str]) -> None:
    """Write report lines to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main() -> int:
    """Program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return 2

    start = time.perf_counter()
    input_file = sys.argv[1]
    output_file = build_output_filename(input_file)

    try:
        tokens = read_tokens(input_file)
    except OSError as exc:
        print(f"ERROR: Could not read file '{input_file}': {exc}")
        return 1

    values: list[float] = []
    invalid = 0

    for t in tokens:
        try:
            values.append(parse_number(t))
        except ValueError:
            print(f"Invalid token skipped: {t}")
            invalid += 1

    if not values:
        elapsed = time.perf_counter() - start
        lines = [
            "Statistics Results",
            f"Input file: {input_file}",
            "",
            "ERROR: No valid numbers found.",
            f"Invalid: {invalid}",
            f"Elapsed time: {elapsed:.6f} seconds",
        ]
        print("\n".join(lines))
        try:
            write_report(output_file, lines)
            print(f"\nResults saved to: {output_file}")
        except OSError as exc:
            print(f"ERROR: Could not write '{output_file}': {exc}")
            return 1
        return 0

    elapsed = time.perf_counter() - start
    lines = build_report(input_file, values, invalid, elapsed)

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
