def print_server_table(servers):
    print(f"\n{'NAME':<12} {'ADDRESS':<15} {'ENVIRONMENT':<16} {'ROLE':<16} {'STATUS':<12} {'LAST CHECKED':<16}")
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