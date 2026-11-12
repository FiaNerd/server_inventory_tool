import sys
from src import menu
from src.controller import filter_servers_in_environment
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
        print(
            f"\n{'NAME':<12} {'ADDRESS':<15} {'ENVIROMENT':<16} {'ROLE':<16} {'STATUS':<12} {'LAST CHECKED':<16}")
        print("-" * 95)

        for server in servers:
            print(
                f"{server['name']:<12} "
                f"{server['address']:<15} "
                f"{server['environment']:<16} "
                f"{server['role']:<16} "
                f"{server.get('status', 'unknown'):<12} "
                f"{server.get('last_checked', ''):<16}"
            )
        sys.exit(0)


    if args.environment:
        filtered_servers = filter_servers_in_environment(servers, args.environment)

        if not filtered_servers:
            print(f"No servers found in environment '{args.environment}'.")
            sys.exit(1)

        print(f"\n{'NAME':<12} {'ADDRESS':<15} {'ENVIRONMENT':<16} {'ROLE':<16} {'STATUS':<12} {'LAST CHECKED':<16}")
        print("-" * 95)

        for server in filtered_servers:
            print(
                f"{server['name']:<12} "
                f"{server['address']:<15} "
                f"{server['environment']:<16} "
                f"{server['role']:<16} "
                f"{server.get('status', 'unknown'):<12} "
                f"{server.get('last_checked', ''):<16}"
            )
        sys.exit(0)