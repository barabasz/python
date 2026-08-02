"""Script to calculate Euler's number (ℯ) with custom precision and compare with reference constant."""

import argparse
import sys
from mpmath import mp, mpf, nstr


def calculate_eulers_number(max_n: int, precision: int) -> mpf:
    """Calculates Euler's number (ℯ) using Taylor series expansion: ∑ (1 / k!).

    Uses an iterative approach keeping track of the running term to maintain
    O(N) computational complexity.

    Args:
        max_n: The maximum integer n to iterate up to (from 0 to max_n).
        precision: The required decimal places of precision.

    Returns:
        mpf: High-precision floating point representation of Euler's number.

    Raises:
        ValueError: If max_n is negative or precision is less than 1.
    """
    if max_n < 0:
        raise ValueError("n must be a non-negative integer.")
    if precision < 1:
        raise ValueError("precision must be at least 1.")

    # Working precision higher than target to avoid guard-digit rounding issues
    mp.dps = precision + 10

    e_sum = mpf(1)  # Represents k = 0 (1 / 0! = 1)
    current_term = mpf(1)

    # Iterative calculation for k from 1 to max_n
    for k in range(1, max_n + 1):
        current_term /= k
        e_sum += current_term

    return e_sum


def format_fixed_decimals(val: mpf, decimals: int) -> str:
    """Formats an mpf float to an exact number of decimal places."""
    # Set dps to decimals + 1 to account for 1 digit before decimal point
    mp.dps = decimals + 10
    
    # Format to string without scientific notation
    s = nstr(val, n=decimals + 5, min_fixed=-sys.maxsize, max_fixed=sys.maxsize)
    
    if "." in s:
        integer_part, decimal_part = s.split(".")
        return f"{integer_part}.{decimal_part[:decimals]}"
    return f"{s}.{'0' * decimals}"


def main() -> None:
    """Main execution function with CLI argument handling."""
    parser = argparse.ArgumentParser(
        description="Calculate Euler's number (ℯ) with arbitrary precision using series expansion."
    )
    parser.add_argument(
        "n",
        type=int,
        nargs="?",
        default=25,
        help="Maximum iteration count n (default: 25)",
    )
    parser.add_argument(
        "p",
        type=int,
        nargs="?",
        default=50,
        help="Decimal digits after decimal point p (default: 50)",
    )

    args = parser.parse_args()

    try:
        # Calculate e
        e_calculated = calculate_eulers_number(max_n=args.n, precision=args.p)

        # Reference e from mpmath
        e_reference = mp.e

        # Absolute difference
        delta = abs(e_reference - e_calculated)

        # Format both outputs to exactly 'p' places after decimal
        e_formatted = format_fixed_decimals(e_calculated, args.p)
        delta_formatted = format_fixed_decimals(delta, args.p)

        # Output symbols
        euler_symbol = "\u2147"  # Unicode U+2147 for Euler's constant (ℯ)
        delta_symbol = "\u0394"  # Unicode U+0394 for Greek capital Delta (Δ)

        print(
            f"Euler's number calculation for n = {args.n} ({args.p}-digits precision)"
        )
        print(f"{euler_symbol} = {e_formatted}")
        print(f"{delta_symbol} = {delta_formatted}")

    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()