def print_server_table(servers):
    print(f"\n{'NAME':<15} {'ADDRESS':<15} {'ENVIRONMENT':<15} {'ROLE':<15} {'STATUS':<15} {'LAST CHECKED':<15}")
    print("-" * 95)

    for server in servers:
        print(
            f"{server['name']:<15} "
            f"{server['address']:<15} "
            f"{server['environment']:<15} "
            f"{server['role']:<15} "
            f"{server.get('status', 'unknown'):<15} "
            f"{server.get('last_checked', ''):<15}"
        )