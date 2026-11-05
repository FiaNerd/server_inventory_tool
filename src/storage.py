import json

# a function that loads data from servers json file
def load_servers():
    """Load server data from the JSON file."""
    with open("servers.json", "r", encoding="utf-8") as file:
        servers = json.load(file)

    return servers

# a function that save data the servers json file
def save_servers(servers):
    """Save server data to the JSON file."""
    with open("servers.json", "w", encoding="utf-8") as file:
        json.dump(servers, file, indent=4, ensure_ascii=False)