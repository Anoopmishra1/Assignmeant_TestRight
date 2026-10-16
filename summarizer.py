"""
Section 2: Device Telemetry Summarizer
========================================
Reads device_telemetry.csv, groups by device_id, computes aggregate
statistics, filters out overheating devices, and exports results to JSON.
"""

import csv
import json
import sys
import os


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INPUT_CSV = "device_telemetry.csv"
OUTPUT_JSON = "output.json"
TEMPERATURE_THRESHOLD = 80.0  # Devices above this avg temp are filtered out


# ---------------------------------------------------------------------------
# Data Ingestion
# ---------------------------------------------------------------------------

def read_telemetry(filepath):
    """
    Read and validate the telemetry CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        list[dict]: A list of validated row dictionaries with keys
                    'device_id', 'status', and 'temperature'.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty or has no valid rows.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: '{filepath}'")

    valid_statuses = {"ACTIVE", "WARNING", "ERROR"}
    rows = []
    skipped = 0

    with open(filepath, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Validate that the CSV has the required columns
        required_columns = {"device_id", "status", "temperature"}
        if reader.fieldnames is None:
            raise ValueError(f"CSV file '{filepath}' is empty.")

        missing_cols = required_columns - set(reader.fieldnames)
        if missing_cols:
            raise ValueError(
                f"CSV is missing required columns: {missing_cols}"
            )

        for line_num, row in enumerate(reader, start=2):
            device_id = row.get("device_id", "").strip()
            status = row.get("status", "").strip().upper()
            temp_raw = row.get("temperature", "").strip()

            # Validate device_id
            if not device_id:
                skipped += 1
                continue

            # Validate status
            if status not in valid_statuses:
                print(f"  [WARN] Line {line_num}: Invalid status "
                      f"'{row.get('status')}' — skipping.")
                skipped += 1
                continue

            # Validate temperature
            try:
                temperature = float(temp_raw)
            except (ValueError, TypeError):
                print(f"  [WARN] Line {line_num}: Invalid temperature "
                      f"'{temp_raw}' — skipping.")
                skipped += 1
                continue

            rows.append({
                "device_id": device_id,
                "status": status,
                "temperature": temperature,
            })

    if not rows:
        raise ValueError("CSV file contains no valid data rows.")

    if skipped > 0:
        print(f"  [INFO] Skipped {skipped} invalid row(s) during ingestion.\n")

    return rows


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_by_device(rows):
    """
    Group rows by device_id and compute summary statistics.

    Args:
        rows (list[dict]): Validated telemetry rows.

    Returns:
        dict: Mapping of device_id → {
            'total_records': int,
            'avg_temperature': float,
            'error_count': int
        }
    """
    device_groups = {}

    for row in rows:
        did = row["device_id"]

        if did not in device_groups:
            device_groups[did] = {
                "total_records": 0,
                "temperature_sum": 0.0,
                "error_count": 0,
            }

        group = device_groups[did]
        group["total_records"] += 1
        group["temperature_sum"] += row["temperature"]

        if row["status"] == "ERROR":
            group["error_count"] += 1

    # Compute averages and build the final summary
    summary = {}
    for did, group in device_groups.items():
        avg_temp = group["temperature_sum"] / group["total_records"]
        summary[did] = {
            "total_records": group["total_records"],
            "avg_temperature": round(avg_temp, 2),
            "error_count": group["error_count"],
        }

    return summary


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_overheating_devices(summary, threshold=TEMPERATURE_THRESHOLD):
    """
    Remove devices whose average temperature exceeds the threshold.

    Args:
        summary (dict): Aggregated device summary.
        threshold (float): Maximum allowed average temperature.

    Returns:
        dict: Filtered summary with overheating devices removed.
    """
    filtered = {}
    removed = []

    for did, stats in summary.items():
        if stats["avg_temperature"] > threshold:
            removed.append(did)
        else:
            filtered[did] = stats

    if removed:
        print(f"  [INFO] Filtered out {len(removed)} overheating device(s): "
              f"{', '.join(removed)}\n")

    return filtered


# ---------------------------------------------------------------------------
# Export & Display
# ---------------------------------------------------------------------------

def export_to_json(data, filepath):
    """
    Save aggregated data to a JSON file.

    Args:
        data (dict): The aggregated device data.
        filepath (str): Output JSON file path.
    """
    with open(filepath, mode="w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=2)

    print(f"  [OK] Results exported to '{filepath}'\n")


def print_summary_table(summary):
    """
    Print a formatted summary table to the terminal.

    Args:
        summary (dict): Aggregated and filtered device data.
    """
    if not summary:
        print("  No devices remaining after filtering.")
        return

    # Table header
    header = f"{'Device':<12} | {'Records':>8} | {'Avg Temp (°C)':>14} | {'Errors':>7}"
    separator = "-" * len(header)

    print(separator)
    print(header)
    print(separator)

    for did in sorted(summary.keys()):
        stats = summary[did]
        print(
            f"{did:<12} | "
            f"{stats['total_records']:>8} | "
            f"{stats['avg_temperature']:>14.2f} | "
            f"{stats['error_count']:>7}"
        )

    print(separator)
    print(f"  Total devices: {len(summary)}\n")


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    """Run the full telemetry summarization pipeline."""

    print("\n" + "=" * 50)
    print("  Device Telemetry Summarizer")
    print("=" * 50 + "\n")

    # --- Step 1: Ingest ---
    print("[1/4] Reading telemetry data...")
    try:
        rows = read_telemetry(INPUT_CSV)
    except FileNotFoundError as err:
        print(f"  [ERROR] {err}")
        sys.exit(1)
    except ValueError as err:
        print(f"  [ERROR] {err}")
        sys.exit(1)

    print(f"  [OK] Loaded {len(rows)} valid record(s).\n")

    # --- Step 2: Aggregate ---
    print("[2/4] Aggregating by device...")
    summary = aggregate_by_device(rows)
    print(f"  [OK] Found {len(summary)} unique device(s).\n")

    # --- Step 3: Filter ---
    print(f"[3/4] Filtering devices with avg temp > {TEMPERATURE_THRESHOLD}°C...")
    filtered = filter_overheating_devices(summary)

    # --- Step 4: Export ---
    print("[4/4] Exporting results...")
    export_to_json(filtered, OUTPUT_JSON)

    # --- Display ---
    print_summary_table(filtered)


if __name__ == "__main__":
    main()
