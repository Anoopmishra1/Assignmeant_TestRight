"""
Section 3: Device Temperature Bar Chart
=========================================
Loads the aggregated JSON output from summarizer.py and generates
a bar chart comparing average temperature per device using matplotlib.
"""

import json
import sys
import os

import matplotlib.pyplot as plt
import matplotlib


# Use non-interactive backend so it works in headless environments
matplotlib.use("Agg")


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INPUT_JSON = "output.json"
OUTPUT_CHART = "chart.png"


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_summary(filepath):
    """
    Load the aggregated device summary from a JSON file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: The parsed device summary data.
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] JSON file not found: '{filepath}'")
        print("  → Run summarizer.py first to generate the output.")
        sys.exit(1)

    with open(filepath, mode="r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as err:
            print(f"[ERROR] Failed to parse JSON: {err}")
            sys.exit(1)

    if not data:
        print("[ERROR] JSON file is empty — no devices to chart.")
        sys.exit(1)

    return data


# ---------------------------------------------------------------------------
# Chart Generation
# ---------------------------------------------------------------------------

def generate_bar_chart(data, output_path):
    """
    Generate and save a bar chart of average temperatures per device.

    Args:
        data (dict): Device summary with 'avg_temperature' per device.
        output_path (str): File path to save the chart image.
    """
    # Extract device names and temperatures
    devices = sorted(data.keys())
    temperatures = [data[d]["avg_temperature"] for d in devices]
    error_counts = [data[d]["error_count"] for d in devices]

    # Color bars based on temperature ranges
    colors = []
    for temp in temperatures:
        if temp < 50:
            colors.append("#2ecc71")   # Green — cool
        elif temp < 70:
            colors.append("#f39c12")   # Orange — warm
        else:
            colors.append("#e74c3c")   # Red — hot

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(devices, temperatures, color=colors, width=0.5,
                  edgecolor="white", linewidth=1.2)

    # Add value labels on top of each bar
    for bar, temp, errors in zip(bars, temperatures, error_counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.0,
            f"{temp}°C",
            ha="center", va="bottom",
            fontsize=11, fontweight="bold", color="#2c3e50"
        )
        # Show error count inside the bar
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() / 2,
            f"{errors} err",
            ha="center", va="center",
            fontsize=9, color="white", fontweight="bold"
        )

    # Chart styling
    ax.set_title(
        "Average Temperature per Device",
        fontsize=16, fontweight="bold", pad=15, color="#2c3e50"
    )
    ax.set_xlabel("Device ID", fontsize=12, labelpad=10, color="#555")
    ax.set_ylabel("Temperature (°C)", fontsize=12, labelpad=10, color="#555")

    # Set y-axis limits with padding for labels
    max_temp = max(temperatures) if temperatures else 100
    ax.set_ylim(0, max_temp + 15)

    # Grid and spine styling
    ax.yaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color("#ccc")

    ax.tick_params(axis="both", colors="#666", labelsize=10)

    # Rotate x-labels to prevent overlap
    plt.xticks(rotation=0, ha="center")

    # Tight layout to prevent clipping
    plt.tight_layout()

    # Save chart
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"[OK] Chart saved to '{output_path}'")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Load JSON data and generate the bar chart."""

    print("\n" + "=" * 50)
    print("  Device Temperature Chart Generator")
    print("=" * 50 + "\n")

    data = load_summary(INPUT_JSON)
    print(f"[INFO] Loaded {len(data)} device(s) from '{INPUT_JSON}'.\n")

    generate_bar_chart(data, OUTPUT_CHART)

    print("\nDone!\n")


if __name__ == "__main__":
    main()
