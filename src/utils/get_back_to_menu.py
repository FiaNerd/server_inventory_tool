def print_q_to_console():
        print("Press [q + enter] to return to the menu...\n")

def cancel_input_with_q(input_user, message="\nReturning to menu..."):
    if input_user.strip().lower() == 'q':
        print("\n[!] Operation cancelled.")
        print(message)
        return True
    return False


def press_enter_to_continue():
        input("\nPress [Enter] to return to the menu...").strip()