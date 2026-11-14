import subprocess
from datetime import datetime
from src import storage
from src.storage import save_servers
import platform


def add_new_server(servers, server_name, address, environment, role, storage):

    new_server = {
        "name": server_name,
        "address": address,
        "environment": environment,
        "role": role,
        "status": "unknown",
        "last_checked": ""
    }

    servers.append(new_server)
    storage.save_servers(servers)

    return new_server


def delete_server_by_name(servers, server_name):

    for server in servers:
        if server.get("name", "").lower() == server_name.lower():
            servers.remove(server)
            storage.save_servers(servers)
            return True, f"Server '{server_name}' has been deleted."

    return False, f"\n[!] Server '{server_name}' was not found."


def verify_server_by_name(servers, server_name, storage ):
    # Find server by name (case-insensitive), returns None if not found
    find_server = next(
        (server for server in servers if server.get("name", "").lower() == server_name.lower()),
        None
    )

    if not find_server:
        return False, f"\n[!] Server '{server_name}' was not found."

    check_server(find_server)
    storage.save_servers(servers)

    return True, find_server


# A function to filter servers by environment
def filter_servers_in_environment(servers, environment):
    return [
        server for server in servers
        if server.get("environment").strip().lower() == environment.strip().lower()
    ]


# A function for checking if a single server answers a ping request
def check_server(server):
    address = server.get("address")

    """ Execute the ping command using a structured list """
    param = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", param, "1", address],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        server["status"] = "up"
    else:
        server["status"] = "down"

    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")


# Iterates through all servers to check connectivity and saves the updated list
def check_servers(servers):
    for server in servers:
        check_server(server)

    save_servers(servers)

    print("All server checks completed and inventory file updated.")
