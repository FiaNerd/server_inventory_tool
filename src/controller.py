import subprocess
from datetime import datetime

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