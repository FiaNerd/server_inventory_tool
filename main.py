from src import menu
from src.storage import load_servers

if __name__ == "__main__":
    servers = load_servers()

    menu.show_menu(servers)