# scripts/pattern_hist_leap_split.py
"""
Compute histogram of Hebrew year patterns (4000–6000) using Months.year_pattern(),
split into leap/non-leap groups, sort each group by frequency, and plot with percentages.

Notes:
- Comments are in English (per request).
- Hebrew strings for title/labels/legend are reversed with [::-1] for RTL rendering.
"""

from collections import Counter
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.patches import Patch

# Import your project modules (adjust if your package path differs)
from hdate.molad import Months
from hdate.leap_years import leapYear


def compute_counts(start: int, end: int) -> Tuple[Counter, Counter, int]:
    """Return (leap_counts, nonleap_counts, total_years) for the given inclusive range."""
    leap_counts = Counter()
    nonleap_counts = Counter()
    total = end - start + 1

    for y in range(start, end + 1):
        pat = Months.year_pattern(y)[::-1]
        if leapYear.is_leap(y):
            leap_counts[pat] += 1
        else:
            nonleap_counts[pat] += 1

    return leap_counts, nonleap_counts, total


def sort_counts_desc(c: Counter) -> List[Tuple[str, int]]:
    """Return list of (pattern, count) sorted by descending count, then by pattern for stability."""
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))


def main():
    # Range selection
    start, end = 4000, 6000

    # Compute counts
    leap_counts, nonleap_counts, total_years = compute_counts(start, end)

    # Sort each group by frequency (descending)
    leap_items = sort_counts_desc(leap_counts)
    nonleap_items = sort_counts_desc(nonleap_counts)

    # Build plotting lists: we concatenate leap group first, then nonleap group.
    labels: List[str] = [k for k, _ in leap_items] + [k for k, _ in nonleap_items]
    values_abs: List[int] = [v for _, v in leap_items] + [v for _, v in nonleap_items]

    # Convert counts to percentages of the entire range
    values_pct: List[float] = [100.0 * v / total_years for v in values_abs]

    # Colors per bar: one color for leap, another for non-leap.
    leap_color = "#1f77b4"      # blue-ish
    nonleap_color = "#ff7f0e"   # orange-ish
    colors: List[str] = [leap_color] * len(leap_items) + [nonleap_color] * len(nonleap_items)

    # Create bar plot
    plt.figure(figsize=(14, 6))
    bars = plt.bar(labels, values_pct, color=colors)

    # Title and axis labels in Hebrew, reversed for RTL display
    title_he = "התפלגות דפוסי השנים"
    xlabel_he = "דפוס שנה"
    ylabel_he = "אחוז מהשנים"

    plt.title(title_he[::-1])
    plt.xlabel(xlabel_he[::-1])
    plt.ylabel(ylabel_he[::-1])

    # Y axis as percent
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=100.0, decimals=1))

    # X tick labels: keep as-is (patterns are short glyphs)
    plt.xticks(rotation=0)

    # Legend in Hebrew (reversed)
    # "Leap years" = "שנים מעוברות"; "Non-leap years" = "שנים פשוטות"
    legend_handles = [
        Patch(color=leap_color, label="שנים מעוברות"[::-1]),
        Patch(color=nonleap_color, label="שנים פשוטות"[::-1]),
    ]
    plt.legend(handles=legend_handles, loc="upper right")
    plt.grid()

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
