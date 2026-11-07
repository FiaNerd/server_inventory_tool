from src import controller, storage
from src.storage import save_servers, export_to_csv


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
               print("\n=== SHOW ALL SERVERS ===\n")
               if not servers:
                   print("No servers found. Please add a server first.")
               else:
                   for server in servers:
                       print("-" * 30)
                       print(f"{'Name:':<14} {server.get('name')}")
                       print(f"{'Address:':<14} {server.get('address')}")
                       print(f"{'Environment:':<14} {server.get('environment')}")
                       print(f"{'Status:':<14} {server.get('status', 'unknown').upper()}")
                   print("-" * 30)

            case "2":
                print("\n=== SHOW SERVERS FROM ENVIRONMENT ===")
            case "3":
                print("\n=== ADD NEW SERVER === ")
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
                    print(f" Server '{server_name:<4}' checked successfully!")
                    print(f" Status: {status.upper():<4} | Last checked: {last_checked}")
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