import subprocess
from datetime import datetime
from src.storage import save_servers

# A function for checking if a single server answers a ping request
def check_server(server):
    address = server.get("address")

    """ Execute the ping command using a structured list """
    result = subprocess.run(
        ["ping", "-c", "1", address],
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