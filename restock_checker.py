"""
Restock Checker
---------------
Reads a stock CSV file (columns: item_name, current_quantity, reorder_threshold),
flags items running low, and writes a "restock needed" report.

Usage:
    python restock_checker.py stock.csv
    python restock_checker.py stock.csv --output restock_report.csv
"""

import csv
import sys
import argparse
from datetime import datetime


def load_stock_data(file_path):
    """Read the CSV file into a list of dictionaries."""
    stock_items = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                stock_items.append({
                    "item_name": row["item_name"].strip(),
                    "current_quantity": int(row["current_quantity"]),
                    "reorder_threshold": int(row["reorder_threshold"]),
                })
            except (KeyError, ValueError) as e:
                print(f"Skipping malformed row {row}: {e}")
    return stock_items


def find_low_stock(stock_items):
    """Loop through stock items and collect anything at or below threshold."""
    low_stock = []
    for item in stock_items:
        current = item["current_quantity"]
        threshold = item["reorder_threshold"]

        if current <= threshold:
            shortfall = threshold - current
            if current == 0:
                status = "OUT OF STOCK"
            elif current <= threshold * 0.5:
                status = "CRITICAL"
            else:
                status = "LOW"

            low_stock.append({
                "item_name": item["item_name"],
                "current_quantity": current,
                "reorder_threshold": threshold,
                "shortfall": shortfall,
                "status": status,
            })
    return low_stock


def print_report(low_stock):
    """Print a clean restock report to the console."""
    print("=" * 60)
    print("RESTOCK NEEDED REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    if not low_stock:
        print("\nAll items are sufficiently stocked. No restocking needed.\n")
        return

    print(f"\n{len(low_stock)} item(s) need restocking:\n")
    header = f"{'Item':<20}{'Current':<10}{'Threshold':<12}{'Shortfall':<12}{'Status':<12}"
    print(header)
    print("-" * len(header))
    for item in low_stock:
        print(
            f"{item['item_name']:<20}"
            f"{item['current_quantity']:<10}"
            f"{item['reorder_threshold']:<12}"
            f"{item['shortfall']:<12}"
            f"{item['status']:<12}"
        )
    print()


def write_csv_report(low_stock, output_path):
    """Write the restock report out as a CSV file."""
    fieldnames = ["item_name", "current_quantity", "reorder_threshold", "shortfall", "status"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(low_stock)
    print(f"Report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Check stock levels and flag items needing restock.")
    parser.add_argument("input_csv", help="Path to the input stock CSV file")
    parser.add_argument("--output", help="Optional path to write the report as a CSV file")
    args = parser.parse_args()

    stock_items = load_stock_data(args.input_csv)
    if not stock_items:
        print("No valid stock data found. Exiting.")
        sys.exit(1)

    low_stock = find_low_stock(stock_items)
    print_report(low_stock)

    if args.output:
        write_csv_report(low_stock, args.output)


if __name__ == "__main__":
    main()
