def print_server_table(servers):
    print(f"\n{'NAME':<15}{'ADDRESS':<18}{'ENVIRONMENT':<15}{'ROLE':<20}{'STATUS':<12}{'LAST CHECKED':<15}")
    print("-" * 96)

    for server in servers:
        print(
            f"{server['name']:<15}"
            f"{server['address']:<18}"
            f"{server['environment']:<15}"
            f"{server['role']:<20}"
            f"{server.get('status', 'unknown'):<12}"
            f"{server.get('last_checked', ''):<15}"
        )