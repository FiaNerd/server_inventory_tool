import sys
from src import menu, storage
from src.controller import filter_servers_in_environment, check_server, verify_server_by_name, check_servers
from src.storage import load_servers
from argparse import ArgumentParser, Namespace

from src.utils.print_server_table import print_server_table

if __name__ == "__main__":

    parser = ArgumentParser(
        prog='server_inventory_tool',
        description='A command-line and interactive tool to manage and monitor server inventories.',
        epilog='Example: python3 main.py --list or python3 main.py --environment production'
    )

    parser.add_argument("--list", action="store_true", help="Show all servers")
    parser.add_argument("--environment", metavar="ENVIRONMENT NAME", type=str, help="Filter by environment")
    parser.add_argument("--check", type=str, metavar="NAME", help="Check a specific server")
    parser.add_argument("--check-all", action="store_true", help="Check all servers")
    parser.add_argument("--export", action="store_true", help="Export report as CSV")

    args: Namespace = parser.parse_args()

    servers = load_servers()

    if len(sys.argv) == 1:
        menu.show_menu(servers)
        sys.exit(0)

    if args.list:
        print_server_table(servers)
        sys.exit(0)

    if args.environment:
        filtered_servers = filter_servers_in_environment(servers, args.environment)

        if not filtered_servers:
            print(f"No servers found in environment '{args.environment}'.")
            sys.exit(1)

        print_server_table(filtered_servers)
        
        sys.exit(0)


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
        export_report = storage.export_to_csv(servers)

        print("Inventory successfully exported!")

        sys.exit(0)
