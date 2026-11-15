import json
import os
from pathlib import Path
import csv
from datetime import datetime

# Reading from environment variable with standard value
CONFIG_DATAFILE = Path(os.getenv("INVENTORY_DATAFILE", "servers.json"))

# A function that loads data from servers json file
def load_servers():
    """Load server data from the JSON file."""
    if not CONFIG_DATAFILE.is_file():
        print("\n[i] No existing server file found. Starting with an empty list.")
        return []

    try:
        with CONFIG_DATAFILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

            if not data:
                print("\n[i] The server file is empty.")

            return data

    except FileNotFoundError:
        print(f"\n[!] Error: The file '{CONFIG_DATAFILE}' could not be found.")
        return []
    except json.JSONDecodeError:
        print(f"\n[!] Error: The server file is corrupted or contains invalid JSON.")
        return []

# A function that save data the servers json file
def save_servers(servers):
    """Save server data to the JSON file."""
    try:
        with CONFIG_DATAFILE.open("w", encoding="utf-8") as file:
            json.dump(servers, file, indent=4, ensure_ascii=False)
    except (PermissionError, OSError) as e:
        print(f"\n[!] Error: Could not save to file. Check permissions. ({e})")


# A function for exporting the serve list into a report folder
def export_to_csv(servers):
    """Export all servers to a timestamped CSV file in the 'reports' directory"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    now = datetime.now()
    current_filename = f"inventory_{now.strftime('%Y-%m-%d_%H%M')}.csv"
    report_path = report_dir / current_filename

    fieldnames = ["name", "address", "environment", "role", "status", "last_checked"]

    # Open file on the right path (report_path)
    try:
        with open(report_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(servers)

        print(f"Report has been exported to {report_path}")
    except (PermissionError, OSError) as e:
        print(f"\n[!] Error: Could not export CSV report. ({e})")