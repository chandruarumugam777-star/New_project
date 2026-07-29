# Restock Checker

A small Python command-line tool that reads inventory data from a CSV file, flags items that need restocking, and generates a restock report.

## Description

`restock_checker.py` takes a stock CSV file with each item's current quantity and reorder threshold, then:

- Loads and validates the stock data
- Identifies items at or below their reorder threshold
- Classifies each low item as **LOW**, **CRITICAL**, or **OUT OF STOCK**
- Prints a formatted report to the console
- Optionally writes the results to a CSV report file

## Requirements

- Python 3.6+
- No external dependencies (uses only the standard library: `csv`, `sys`, `argparse`, `datetime`)

## Input Format

The input CSV must contain the following columns:

| Column              | Type | Description                          |
|----------------------|------|---------------------------------------|
| `item_name`          | str  | Name of the inventory item             |
| `current_quantity`   | int  | Quantity currently in stock            |
| `reorder_threshold`  | int  | Minimum quantity before restocking     |

**Example (`stock.csv`):**
```csv
item_name,current_quantity,reorder_threshold
Widget A,12,20
Widget B,45,30
Widget C,5,15
Widget D,100,50
Widget E,8,8
```

Rows that are missing required fields or contain non-numeric quantities are skipped, with a message printed to the console.

## Usage

Print a report to the console:
```bash
python restock_checker.py stock.csv
```

Print a report and save it to a CSV file:
```bash
python restock_checker.py stock.csv --output restock_report.csv
```

## Status Classification

For each item where `current_quantity <= reorder_threshold`:

| Status         | Condition                                      |
|----------------|-------------------------------------------------|
| `OUT OF STOCK` | `current_quantity == 0`                          |
| `CRITICAL`     | `current_quantity <= reorder_threshold * 0.5`    |
| `LOW`          | Otherwise (below threshold but above 50% of it)  |

`shortfall` is calculated as `reorder_threshold - current_quantity`.

## Output

**Console output** — a formatted table plus a summary header with a timestamp.

**CSV output** (`--output`) — a file with columns:
```
item_name,current_quantity,reorder_threshold,shortfall,status
```

**Example (`restock_report.csv`):**
```csv
item_name,current_quantity,reorder_threshold,shortfall,status
Widget A,12,20,8,LOW
Widget C,5,15,10,CRITICAL
Widget E,8,8,0,LOW
```

## Project Structure

```
.
├── restock_checker.py   # Main script
├── stock.csv            # Sample input data
├── restock_report.csv   # Sample generated report
└── README.md            # This file
```

## Notes

- If no items need restocking, the tool prints a message stating all items are sufficiently stocked and skips writing a CSV report is not automatic — `--output` will still write a file with just the header row.
- Malformed rows are skipped rather than causing the script to fail.
