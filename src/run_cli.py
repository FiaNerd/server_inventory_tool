import sys
from argparse import Namespace, ArgumentParser

from src import storage, controller, menu
from src.controller import check_servers, verify_server_by_name
from src.utils.print_server_table import print_server_table


def run_cli():
    parser = ArgumentParser(
        prog='server_inventory_tool',
        description='A command-line and interactive tool to manage and monitor server inventories.',
        epilog='Example: python3 main.py --list or python3 main.py --list --environment prod'
    )

    parser.add_argument("--list", action="store_true", help="Show all servers")
    parser.add_argument("--environment", metavar="ENVIRONMENT NAME", type=str, help="Filter by environment")
    parser.add_argument("--check", type=str, metavar="NAME", help="Check a specific server")
    parser.add_argument("--check-all", action="store_true", help="Check all servers")
    parser.add_argument("--export", action="store_true", help="Export report as CSV")

    args: Namespace = parser.parse_args()

    servers = storage.load_servers()

    if len(sys.argv) == 1:
        menu.show_menu(servers)
        sys.exit(0)

    if args.environment and not args.list:
        print("[!] Error: --environment requires --list flag.")
        sys.exit(1)

    if args.list:
        servers = storage.load_servers()

        if args.environment:
            target_servers = controller.filter_servers_in_environment(servers, args.environment)
        else:
            target_servers = servers

        if not target_servers:
            print("No servers found.")
        else:
            print_server_table(target_servers)
        sys.exit(0)

    if args.environment and not args.list:
        print("[!] Error: --environment requires --list flag.")
        sys.exit(1)

    if args.check:
        success, result = verify_server_by_name(servers, args.check, storage)

        if not success:
            print(result)
            sys.exit(1)

        print(f"\nServer '{result['name']}' checked successfully!")
        print(f"Status: {result['status'].upper()} | Last Checked: {result['last_checked']}")

        if result.get("status") == "down":
            sys.exit(1)

        sys.exit(0)

    if args.check_all:
        check_servers(servers)

        print_server_table(servers)

        if any(server.get("status") == "down" for server in servers):
            sys.exit(1)

        sys.exit(0)

    if args.export:
        success = storage.export_to_csv(servers)

        if success:
            sys.exit(0)
        else:
            sys.exit(1)