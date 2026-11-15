# Server Inventory Tool

A command-line and interactive Python tool for managing, monitoring, and filtering server inventories.

---

## Table of Contents

- [Description](#-description)
- [Overview & Features](#-overview--features)
- [Prerequisites & Setup](#-prerequisites--setup)
  - [System Requirements](#system-requirements)
  - [Installation](#installation)
- [Project Structure](#-project-structure)
- [How to Run the Application](#how-to-run-the-application)
  - [Mode 1: UI Text Menu](#mode-1-ui-text-menu)
  - [Mode 2: Command-Line Interface (CLI)](#mode-2-command-line-interface-cli)
- [Environment Configuration & Filtering](#-environment-configuration--filtering)
- [Data Persistence & Exports](#-data-persistence--exports)
  - [Local JSON Storage (`servers.json`)](#local-json-storage-serversjson)
  - [CSV Reporting (`reports/`)](#csv-reporting-reports)


---

## 🚀&#xFE0E; Description

Server Inventory Tool is a Python program made to help you keep track of your servers and check if they are online. 
You can use it either through an interactive text menu or directly from the command line with CLI flags. 
The tool lets you filter servers by environment (`dev`, `test`, `prod`), run ping checks to see if a server is `up` or `down`, and save everything locally in a JSON file. 
It also prints the server list in a terminal table and lets you export the results to a CSV file.

---

## 🕮 Overview & Features

Keeping track of which servers are running and what roles they have is important in any development or operations workflow. 
**Server Inventory Tool** runs on Windows, Linux, and macOS, giving you both a guided menu and fast terminal commands without needing any external libraries.

### Key Features

- **Server Inventory Tracking:** Saves server details like `name`, `address`, `environment`, `role`, `status`, and `last_checked` timestamps.
- **Persistent JSON Storage:** Reads and updates a local JSON file automatically so your server list and status checks are saved between runs.
- **Cross-Platform Ping Checks:** Uses the system's built-in ping command (`ping -n` on Windows, `ping -c` on Linux/macOS) to check if a server responds and sets the status to `up` or `down`.
- **Terminal Tables:** Prints the server list in readable, aligned columns (`:<15` formatting) directly in the console.
- **CSV Export:** Saves the current server inventory and check results into a `.csv` file so you can open them in Excel or share them easily.
- **Two Ways to Run:** Use either the UI menu or pass quick CLI flags using `argparse`.

---

## ⚙️&#xFE0E; Prerequisites & Setup

### System Requirements

- **Python:** Tested on Python 3.13.
- **Operating System:** Windows, Linux, or macOS.
- **Dependencies:** Built using only Python's standard library (`argparse`, `json`, `csv`, `os`, `sys`, `subprocess`, `platform`, `datetime`). No extra `pip` packages need to be installed.

---

### Installation

1. Clone the repository to your computer:
   ```bash
   git clone <the-repository-url>
   cd server_inventory_tool
   ```
---

## 🌲&#xFE0E; Project Structure

The project is built into separate modules to keep the user interface, logic, and file handling apart:

```text
server_inventory_tool/
├── reports/                    # Generated CSV export files
├── src/
│   ├── utils/                  # Helper functions for UI and input checks
│   │   ├── input_validator.py
│   │   ├── press_enter_to_continue.py
│   │   └── print_server_table.py
│   ├── controller.py           # Main logic and ping checks
│   ├── menu.py                 # Interactive text menu and user prompts
│   └── storage.py              # JSON saving/loading and CSV export
├── .gitignore                  # Files and folders ignored by Git
├── main.py                     # Entry point and CLI argument parser
├── README.md                   # Project documentation
├── REPORT.md                   # Technical report and code explanations
└── servers.json                # Local JSON file storing the server list
```
> [!NOTE]
> Rather than putting every file straight into the root folder, I created a `src` folder 
> for all the UI, logic, and export handling to keep things organized and easy to find. 
> If this was a larger project, I would divide it into more folders to create a clearer structure.

---

## How to Run the Application

Run `main.py` from the root folder using Python. You can either use the UI menu or run commands directly with CLI flags.

### Mode 1: UI Text Menu

Start project without any flags to open the menu:

```bash
python main.py
```

In the menu, choose a number to:
- View all servers in a formatted table.
- Filter servers by environment (`dev`, `test`, `prod`).
- Add a new server or delete an existing one.
- Verify a single server or all servers with a live ping check.
- Export the current server list to a CSV file.

### Mode 2: Command-Line Interface (CLI)

If you want to run a quick check without opening the menu, pass flags directly when running `main.py`. Use `-h` or `--help` to see all available flags:

```bash
python3 main.py --help
```

**Common CLI Examples:**

```bash
# List all servers in the inventory
python3 main.py --list

# Filter servers by environment (dev, test, prod)
python3 main.py --environment <environment name>

# Check reachability (ping) for a specific server by name
python3 main.py --check <server name>

# Run a live ping check on all servers and update their status
python3 main.py --check-all

# Export the inventory directly to a CSV file
python3 main.py --export
```

---

## ⚙️&#xFE0E; Environment Configuration & Filtering

Servers are grouped by environment so you can easily separate test setups from live servers:
- **`dev`**: Development servers used while building and testing new features.
- **`test`**: Staging or QA servers used for testing before release.
- **`prod`**: Production servers running live services.

You can filter by environment either in the interactive menu or by using the `--environment` flag. 
The input validator (`src/utils/input_validator.py`) checks that environment names and server addresses are valid before saving or filtering.

---

## 💾&#xFE0E; Data Persistence & Exports

### Local JSON Storage (`servers.json`)

All servers are loaded from and saved to `servers.json` in the root folder via `src/storage.py`. 
- You can set a custom data filename using the `INVENTORY_DATAFILE` environment variable.
- If `servers.json` doesn't exist yet when you start the program, it creates an empty list automatically.
- Whenever you add a server or run a ping check, the new status (`up` or `down`) and `last_checked` timestamp are saved right away.


```json
[
  {
    "name": "web01",
    "address": "example.com",
    "environment": "prod",
    "role": "webserver",
    "status": "up",
    "last_checked": "2026-11-14 15:10"
  }
]
```

**Field descriptions:**
- `name`: Unique name or hostname for the server.
- `address`: IP address or domain name used for ping checks.
- `environment`: Which environment the server belongs to (`dev`, `test`, or `prod`).
- `role`: What the server is used for (for example `webserver` or `database`).
- `status`: Latest ping result (`up`, `down`, or `unknown`).
- `last_checked`: Date and time of the last ping check (`YYYY-MM-DD HH:MM`).

### CSV Reporting (`reports/`)

When you export the inventory, `src/storage.py` saves a timestamped `.csv` file in the `reports/` folder. This makes it easy to open the server list in Excel or share a quick status report.
