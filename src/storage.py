import json

# a function that loads data from servers
def load_servers():
    """Load server data from the JSON file."""
    with open("servers.json", "r", encoding="utf-8") as file:
        servers = json.load(file)

    return servers