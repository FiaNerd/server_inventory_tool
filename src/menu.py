from src import controller, storage
from src.utils.input_validator import valid_input


def show_menu(servers):
    while True:
        print("\n=== SERVER INVENTORY MENU ===")
        print("[1] Show all servers")
        print("[2] Show server in specific environment")
        print("[3] Add new server")
        print("[4] Delete server")
        print("[5] Verify server")
        print("[6] Verify all servers")
        print("[7] Export report as CSV")
        print("[0] Exit")

        user_choice = input("Choose an option: ").strip()

 # TODO: if there is time, se if you can do when the user press a number, the user should press another key for getting back to the menu
        match user_choice:
            case "1":
               print("\n=== SHOW ALL SERVERS ===")
               if not servers:
                   print(f"No servers found {user_choice}. Please add a server first.")
               else:
                   for server in servers:
                       print("-" * 30)
                       print(f"{'NAME:':<14} {server.get('name').lower()}")
                       print(f"{'ADDRESS:':<14} {server.get('address').lower()}")
                       print(f"{'ENVIRONMENT:':<14} {server.get('environment').lower()}")
                       print(f"{'STATUS:':<14} {server.get('status', 'unknown').lower()}")

                       last_checked = server.get('last_checked')

                       if not last_checked:
                           checked = "never"
                       else:
                           checked = last_checked

                       print(f"{'LAST CHECKED:':<14} {checked}")


                   print("-" * 30)

            case "2":
                print("\n=== SHOW SERVERS FROM ENVIRONMENT ===")
                input_env = input("Which enviorment (dev, test, prod)?: ").strip()

                matched_servers =  controller.filter_servers_in_environment(servers, input_env)

                if not matched_servers:
                    print(f"\n[!] No servers found in the enviorment - {input_env}. \nTry again or add a server.")

                else:
                    print(f"\nServer in enviorment '{input_env}'")
                    print(f"\n{'NAME':<12} {'ADDRESS':<15} {'ENVIROMENT':<16} {'ROLE':<16} {'STATUS':<12} {'LAST CHECKED':<16}")
                    print("-" * 100)

                    for server in matched_servers:
                        print(
                            f"{server['name']:<12} "
                            f"{server['address']:<15} "
                            f"{server['environment']:<16} "
                            f"{server['role']:<16} "
                            f"{server['status']:<13}"
                            f"{server['last_checked']}")
                        print()

            case "3":
                print("\n=== ADD NEW SERVER === ")
                server_name = valid_input("Enter server name: ")

                if any(server.get("name", "").lower() == server_name.lower() for server in servers):
                    print(f"\n[!] The server name '{server_name}' already exists.\nTry another server name.")
                else:
                    address = valid_input("Enter address: ").strip()
                    # TODO: if there is time, change to swtich case so the user enter number instead of writing dev, test, prod
                    while True:
                        environment = valid_input("Enter environment (dev, test, prod): ").strip()

                        if environment in ["dev", "test", "prod"]:
                            break

                        print(f"\n[!] Sorry, the environment '{environment}' is invalid. \n Try again.\n")

                    role = valid_input("Enter role: ").strip()

                    new_server = {
                        "name": server_name,
                        "address": address,
                        "environment": environment,
                        "role": role,
                        "status": "unknown",
                        "last_checked": ""
                    }

                    servers.append(new_server)
                    print(f"Server {server_name} added successfully!")
            case "4":
                print("\n=== DELETE A SERVER ===")

            case "5":
                print("\n=== VERIFY SINGLE SERVER ===")
                server_name = input("Enter the name of the server to verify: ").strip()

                # Find server by name (case-insensitive), returns None if not found
                found_server = next(
                    (server for server in servers if server.get("name", "").lower() == server_name.lower()),
                    None
                )

                if found_server:
                    print(f"\nPinging the address: {found_server.get('address')}")

                    controller.check_server(found_server)
                    storage.save_servers(servers)

                    status = found_server.get("status")
                    last_checked = found_server.get("last_checked")
                    print(f"Server '{server_name:<4}' checked successfully!")
                    print(f"Status: {status.upper():<4} | Last checked: {last_checked}")
                else:
                    print(f"[!] Server '{server_name}' was not found.")

            case "6":
                print("\n=== VERIFY ALL SERVERS ===")
                controller.check_servers(servers)
            case "7":
                print("\n=== EXPORT REPORT TO CSV ===")
                storage.export_to_csv(servers)

            case "0":
                print("Exit program..")
                break
            case _:
                print(f"\n[!] Invalid option - {user_choice}.")
                print("Choose a number between 0 and 7 ")