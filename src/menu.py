def show_menu(servers):
    while True:
        print("\n=== SERVER INVENTORY MENU ===")
        print("[1]. Show all servers")
        print("[2]. Show server in specific environment")
        print("[3]. Add new server")
        print("[4]. Delete server")
        print("[5]. Verify server")
        print("[6]. Verify all servers")
        print("[7]. Export report as CSV")
        print("[0]. Exit")

        user_choice = input("Choose an option: ").strip()

        match user_choice:
            case "1":
                print("=== Show all servers ===")
            case "0":
                print("Exit program..")
                break
            case _:
                print(f"\n[!] Invalid option - {user_choice}.")
                print("Choose a number between 0 and 7 ")