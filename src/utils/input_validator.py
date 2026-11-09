def valid_input(user_input):
    while True:
        value = input(user_input).strip()

        if value:
            return value
        print("\n[!] This is required field.\n")