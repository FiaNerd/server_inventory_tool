from src import controller, storage
from src.utils.input_validator import valid_input
from src.utils.press_enter_to_continue import press_enter_to_continue
from src.utils.print_server_table import print_server_table


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

        user_choice = input("\nChoose an option: ").strip()

        match user_choice:
            case "1":
               print("\n=== SHOW ALL SERVERS ===")
               if not servers:
                   print(f"No servers found '{user_choice}'. Please add a server first.")
               else:
                   print_server_table(servers)
               press_enter_to_continue()

            case "2":
                while True:
                    print("\n=== SHOW SERVERS FROM ENVIRONMENT ===")
                    print(" [press 'q' to go back to the menu]\n")

                    input_environment = input("Which environment (dev, test, prod)?: ").strip().lower()

                    if input_environment == "q":
                        break

                    matched_servers = controller.filter_servers_in_environment(servers, input_environment)

                    if not matched_servers:
                        print(
                            f"\n[!] No servers found in the environment - {input_environment}. \nTry again or add a server.")
                        continue

                    else:
                        print(f"\nServers in environment '{input_environment}':")

                        print_server_table(matched_servers)

                    break

                press_enter_to_continue()

            case "3":
                print("\n=== ADD NEW SERVER === ")
                print("Press [q] at any time to return to the menu.\n")

                while True:
                    server_name = valid_input("Enter server name: ").strip()

                    if server_name.lower() == 'q':
                        print("\nReturning to menu...")
                        break

                    if any(server.get("name", "").lower() == server_name.lower() for server in servers):
                        print(f"\n[!] The server name '{server_name}' already exists.\nTry another server name.\n")
                    else:
                        break

                if server_name.lower() != 'q':
                    address = valid_input("Enter address: ").strip()

                    while True:
                        environment = valid_input("Enter environment (dev, test, prod): ").strip()

                        if environment in ["dev", "test", "prod"]:
                            break

                        print(f"\n[!] Sorry, the environment '{environment}' is invalid. \n Try again.\n")

                    role = valid_input("Enter role: ").strip()

                    controller.add_new_server(servers, server_name, address, environment, role, storage)

                    print(f"\n[+] Server '{server_name}' added successfully!")

                    press_enter_to_continue()

            case "4":
                print("\n=== DELETE A SERVER ===")
                print("Press [q] at any time to return to the menu.\n")

                while True:
                    server_name = input("What server to delete?: ").strip()

                    if server_name.lower() == "q":
                        print("\nReturning to menu...")
                        break

                    server_exist = next((server for server in servers
                                         if server.get("name", "").lower() == server_name.lower()),
                                         None)

                    if not server_exist:
                        print(f"\n[!] Server '{server_name}' was not found.\nTry again.\n")
                    else:

                        delete_confirmation = input(f"Are you sure to delete '{server_name}'? (y/n) ").strip().lower()

                        if delete_confirmation in ["y"]:

                            environment_prod = server_exist.get("environment", "").lower()

                            if environment_prod in ["prod"]:
                                print(f"\n[!] WARNING: {server_name} is in production!\n Are you sure you wanna delete '{server_name}'")

                                prod_confirmation = input(f"\nConfirm the server name '{server_name}' again: ").strip()

                                if prod_confirmation.lower() != server_name.lower():
                                    print("\n[!] The name did not match. Canceld delation\n")
                                    continue

                            success, result = controller.delete_server_by_name(servers, server_name)

                            if success:
                                print(f"\n{result}\n")
                                break
                            else:
                                print(f"\n[!] {result}\n")
                                break
                                
                        elif delete_confirmation in ["n"]:
                            print("\nThe deletion was canceled.\n")
                            break
                        else:
                            print("\nSorry, invalid input. Press ['y'] or ['n']. \n Try again!")

                        press_enter_to_continue()

            case "5":
                print("\n=== VERIFY SINGLE SERVER ===")
                server_name = input("Enter the name of the server to verify: ").strip()

                success, result = controller.verify_server_by_name(servers, server_name, storage)

                if success:
                    status = result.get("status", "unknown")
                    last_checked = result.get("last_checked", "")
                    print(f"\nPinging the address: {result.get('address')}")
                    print(f"Server '{server_name}' checked successfully!")
                    print(f"Status: {status.upper():<4} | Last checked: {last_checked}")
                else:
                    print(f"[!] {result}")

                press_enter_to_continue()

            case "6":
                print("\n=== VERIFY ALL SERVERS ===")
                controller.check_servers(servers)

                press_enter_to_continue()

            case "7":
                print("\n=== EXPORT REPORT TO CSV ===")
                storage.export_to_csv(servers)

                press_enter_to_continue()

            case "0":
                print("Exit program..")
                print("Hope to see you again!")
                break

            case _:
                print(f"\n[!] Invalid option - {user_choice}.")
                print("Choose a number between 0 and 7 ")