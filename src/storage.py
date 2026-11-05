import json
from pathlib import Path

DATA_FILE = Path("servers.json")

# a function that loads data from servers json file
def load_servers():
    """Load server data from the JSON file."""
    if not DATA_FILE.is_file():
       return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

# a function that save data the servers json file
def save_servers(servers):
    """Save server data to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(servers, file, indent=4, ensure_ascii=False)