import sys
from src import menu
from src.storage import load_servers
from argparse import ArgumentParser, Namespace

if __name__ == "__main__":

    parser = ArgumentParser(
        prog='server_inventory_tool',
        description='A command-line and interactive tool to manage and monitor server inventories.',
        epilog='Example: python3 main.py --list or python3 main.py --environment production'
    )

    parser.add_argument("--list", action="store_true", help="Show all servers")
    parser.add_argument("--environment", type=str, help="Filter by environment")
    parser.add_argument("--check", type=str, help="Check a specific server")
    parser.add_argument("--check-all", action="store_true", help="Check all servers")
    parser.add_argument("--export", action="store_true", help="Export report as CSV")

    args: Namespace = parser.parse_args()

    servers = load_servers()

    if len(sys.argv) == 1:
        menu.show_menu(servers)
        sys.exit(0)

    if args.list:
        for server in servers:
            print(server)

        sys.exit(0)