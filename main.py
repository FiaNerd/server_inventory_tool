from src.storage import load_servers

if __name__ == "__main__":
    servers = load_servers()
    print(servers)

    help(load_servers)