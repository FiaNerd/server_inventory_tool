# Technical Report – Server Inventory Tool

## 1. Three Code Constructs

In my code I use several iterations, conditions, and functions. Here are three examples:

- **Loop (List Comprehension):** In `src/controller.py`, I use a compact expression loop to filter servers based on the environment.
  - **What it does:** It loops through every server in the list and builds a new filtered list in a single, clean statement.
  - **How the syntax works:** Instead of a traditional multiline loop with a colon (`:`), a list comprehension wraps the loop and condition inside brackets `[...]`. It evaluates `server for server in servers` and filters them using the `if` condition, and then returns the resulting list.

*Example from `src/controller.py` (start line: 53)*
```python
  def filter_servers_in_environment(servers, environment):
      return [
          server for server in servers
          if server.get("environment").strip().lower() == environment.strip().lower()
      ]
```
<br>

- **Conditional Statement (`if / elif / else`):** In `src/menu.py `, I use conditional statements to check different user inputs and decide what the program should do next.
  - **What it does:** It checks whether the user's confirmation input is `"y"` (to proceed), `"n"` (to cancel), or something invalid, and directs the program down the correct path based on the answer.
  - **How the syntax works:** Python checks the conditions from top to bottom. The `if` statement checks the first condition. If it is false, it continues to the next statement (`elif` / "else if") to check alternative options, and if nothing is true, `else` catches anything that didn't match the above.
  
*Example from `src/menu.py` (start line: 111):*
```python
  if delete_confirmation in ["y"]:
      # If the user press "y"
      ...
  elif delete_confirmation in ["n"]:
      print("\nThe deletion was canceled.\n")
      break
  else:
      print("\nSorry, invalid input. Try again!")
```
<br>&nbsp;<br>

- **Functions with parameters and return value:** In `src/controller.py`, I use functions with parameters and return values to modularize the code, separate concerns, and make the program easier to maintain and test.
  - **What it does:** This function takes a server list, a server name, and a storage object. It searches for the server, runs a check on it, saves the updated list to storage, and sends back a success/failure status along with the server data.

  - **How the syntax works:**
 It uses parameters (`servers`, `server_name`, `storage`) to receive data into the function.
 It uses Python's built-in `next()` function to efficiently find the first matching server without writing a long `for`-loop. It uses multiple `return` statements to exit early if the server isn't found, or return a success status (`True`) and the server data at the end.
 
*Example from `src/controller.py` (start line: 36):*
 ```python
  def verify_server_by_name(servers, server_name, storage ):
    # Find server by name (case-insensitive), returns None if not found
    find_server = next(
        (server for server in servers if server.get("name", "").lower() == server_name.lower()),
        None
    )

    if not find_server:
        return False, f"\n[!] Server '{server_name}' was not found."

    check_server(find_server)
    storage.save_servers(servers)

    return True, find_server
 ```
**How it is called:** In `src/menu.py`, the function is called by passing the three required arguments (servers, server_name, and storage), and it unpacks the result into success and result:
  
*Example from `src/menu.py ` (start line 145)`*
```python
success, result = controller.verify_server_by_name(servers, server_name, storage)
```
---
## 2. Data Structure & Data Types

- **Why a list of dictionaries is used for servers:**
  Dictionaries work like digital info cards. They store data as key–value pairs, where every key is unique (for example, `"name"`). Instead of remembering a number position, we just ask for the key (like `server["name"]`) to get the right value.

- **Data types used in the server:**
  In this case, all values inside the json server record are saved as Strings (`str`) of text (which is easy to see because of the quotation marks `""`). So even if a value represents a number or a date/time, it is stored as a string because it is wrapped in quotation marks `""`. (Python dictionaries can also handle other data types like booleans, integers and floats.)

```text
  name: String (str) – e.g., "web01"
  address: String (str) – e.g., "192.168.1.10"
  environment: String (str) – e.g., "dev", "test", or "prod"
  role: String (str) – e.g., "webserver"
  status: String (str) – e.g., "up"
  last_checked: String (str) – e.g., "2026-11-14 15:10"
```
---
## 3. JSON for Storage vs. CSV for Exports

- **Why JSON is used for internal storage:**
  JSON (JavaScript Object Notation) matches Python’s lists and dictionaries almost perfectly. When the program saves or loads server data, JSON keeps the structure intact. This allows the tool to easily read the file, update the data in memory, and save it back without breaking the formatting. It is also well-organized and easy to read for the human eye.

- **Why CSV is used for generating reports:**
  CSV (Comma-Separated Values) is used when creating flat report exports. Unlike JSON (which keeps data nested like dictionaries), CSV separates the values with commas. When you open a CSV file, programs like Microsoft Excel or Google Sheets automatically turn those commas into tables with columns and rows. This makes it super easy for anyone to open, sort, and read the report without needing any coding knowledge.

---
## 4. Program Structure: Modules and Functions
The program is divided into modular files to keep the code clean, organized, and easy to maintain. By separating user interactions from core logic and storage handling, each file has a single responsibility:

**MAIN `src/main.py` (Entry Point):**
<br>
**Responsibility:** Acts as the starting point of the application. It initializes the program, loads the initial data, handles command-line arguments (using `argparse`), and launches the main menu loop.
  
**MENU `src/menu.py` (User Interface & Navigation):**
<br>
**Responsibility:** Handles all interactions with the user in the console. It displays menus, collects user input (such as server names or environment choices), checks for valid input using conditional statements, and decides what action to trigger next.

**CONTROLLER `src/controller.py` (Business Logic):**
<br>
**Responsibility:** Contains the core logic functions of the application. It handles data manipulation, such as filtering servers by environment using list comprehensions or verifying specific servers by name using efficient search methods.

**STORAGE `src/storage.py` (Saving & Exporting Data):**
<br>
 **Responsibility:** Handles reading and writing files. It saves and loads server data in JSON format so the structure stays intact, and exports CSV reports that can be opened in spreadsheet programs like Excel.

**UTILS `src/utils.py` (Helper Functions):**
<br>
**Responsibility:** Contains shared helper functions used across the entire application. This avoids repeating the same code in multiple places and keeps the project clean and easy to maintain.

---
## 5. Standard Library Modules
The application uses several built-in modules from Python's standard library to handle system tasks, cross-platform compatibility, and file management without needing external packages:

- **sys / argparse (Command-Line & System):**
  - **Used for:** Handling command-line arguments when starting the script and controlling how the program exits.

*Example from `main.py`*
```python
  # Line 27 -29
  if len(sys.argv) == 1:
      menu.show_menu(servers)
      sys.exit(0)  # Exits successfully after the menu closes
  
  # Line 37 - 39    
  if not target_servers:
      print(f"No servers found in environment '{args.environment}'.")
      sys.exit(1)  # Exits with an error code if nothing was found
```

- **Subprocess & Platform** 
  - **subprocess (System Commands):**<br/>
    **Used for:** Running terminal commands from within Python-specifically executing network ping commands to check if servers are online and responsive.<br/>
  <br/>

  - **platform (Operating System Detection):**<br/>
    **Used for:** Checking whether the user is running Windows, Linux, or macOS. This is crucial because different operating systems use different syntax for network commands (e.g., ping -n on Windows vs ping -c on Linux/macOS).

*Example from `src/controller.py` (start line: 82)*
```python
def check_server(server):
    address = server.get("address")

    """ Execute the ping command using a structured list """
    param = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", param, "1", address],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        server["status"] = "up"
    else:
        server["status"] = "down"

    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")

```

- **json (Data Storage):**
<br>
  **Used for:** Converting the saved text file into Python lists and dictionaries so the program can easily read and use the server data.
<br>

*Example of `servers.json`:*
  ```json
  [
      {
          "name": "web01",
          "address": "example.com",
          "environment": "prod",
          "role": "webserver",
          "status": "up",
          "last_checked": "2026-11-14 15:10"
      }
  ]
  ```
*Example from `src/storage.py` (start line: 11)*
```python
    def load_servers():
        """Load server data from the JSON file."""
        if not CONFIG_DATAFILE.is_file():
           return []
  
        with CONFIG_DATAFILE.open("r", encoding="utf-8") as file:
            return json.load(file)
```

- **Pathlib, DateTime & CSV**
  - **pathlib (Path) & os (File Paths & Directories):**<br/>
  **Used for:** Creating the reports directory safely if it doesn't already exist and building correct file paths across different operating systems.<br/>
<br/>
  - **datetime (Timestamps):**<br/>
  **Used for:** Generating a unique, timestamped filename for every exported report (e.g., inventory_2026-11-15_1241.csv) so previous reports aren't overwritten.<br/>
<br/>
  - **csv (Report Exporting):**<br/>
  **Used for:** Formatting and writing flat data rows so reports can be opened easily in spreadsheet tools like Excel. Translating Python dictionaries into formatted flat rows and columns using csv.DictWriter.

*Example from `src/storage.py`  (start line: 35)*
```python
def export_to_csv(servers):
    """Export all servers to a timestamped CSV file in the 'reports' directory"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    now = datetime.now()
    current_filename = f"inventory_{now.strftime('%Y-%m-%d_%H%M')}.csv"
    report_path = report_dir / current_filename

    fieldnames = ["name", "address", "environment", "role", "status", "last_checked"]

    with open(report_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(servers)

    print(f"Report has been exported to {report_path}")

```
---
## 6. Three Examples of Good Practice
**1. Input Validation & Cancel Option:**
  - **1a. Validation:** Essential for preventing bad data—such as accidental whitespace or empty fields and ensuring the user provides correct and expected information.
  - **1b. Cancel at any time:** A users should never feel trapped. Giving the option to cancel (`[q]` to quit) alongside solid validation keeps the data clean and makes the tool much easier to use.

*From `src/utils/input_validator.py`*
```python
# Validation for user input. 
def valid_input(user_input):
    while True:
        value = input(user_input).strip()

        if value:
            return value
        print("\n[!] This is required field.\n")
```

  *Example from `src/menu.py` (start line: 57)*
  ```python
  case "3":
      print("\n=== ADD NEW SERVER === ")
      # if the user regrat to add a new server 
      print("Press [q] at any time to return to the menu.\n")

      while True:
          server_name = valid_input("Enter server name: ").strip()
```

**2. Defensive Programming:**
  - **Try and except:** Even if an application runs smoothly under normal conditions, unexpected file corruption can occur. Using `try...except` with `json.JSONDecodeError` ensures that the program fails gracefully rather than crashing abruptly, returning a safe default value instead.

  *Example from `src/storage.py` (start line: 11)*
  ```python
  def load_servers():
      """Load server data from the JSON file safely."""
      if not CONFIG_DATAFILE.is_file():
         return []

      try:
          with CONFIG_DATAFILE.open("r", encoding="utf-8") as file:
              return json.load(file)
      except json.JSONDecodeError:
          print("\n[!] Error: 'servers.json' is corrupted or invalid. Returning empty list.")
          return []
  ```

**3. Cross-Platform Compatibility:**
  - **Different operating system:** To ensure the script works smoothly on  both Windows and Linux/macOS environments, the code dynamically checks the operating system using `platform.system()`. It automatically switches the ping parameter (`-n` for Windows and `-c` for Unix-based systems) to prevent errors and make the tool truly cross-platform.

*Example from `src/storage.py` (start line: 61)*
```python
def check_server(server):
    address = server.get("address")

    """ Execute the ping command using a structured list """
    param = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", param, "1", address],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        server["status"] = "up"
    else:
        server["status"] = "down"

    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")

```
---
## 7. Sources and Tools Used

In addition to school lectures and course presentations, the following tools and external sources have been utilized during the project:

### Tools & Environment
- **PyCharm:** Main Integrated Development Environment (IDE) for Python development.
- **Ubuntu:** Linux environment used for testing and compatibility.
- **Terminal & Git:** Version control and repository management.
- **GitHub:** Remote repository hosting.
- **Markdown Tree Generator:** Used to generate the visual layout of the project structure for the `README.md` file ([DevTool Tree Generator](https://devtool.tech/en/tree)).

### Sources & Documentation

- **Python Documentation:** Official documentation for the `json` and `csv` modules to understand parameter behaviors and file handling ([Python Docs](https://docs.python.org/3/library/csv.html)).

- **DataCamp - JSON Data in Python:** Referenced for structuring and parsing JSON data files ([DataCamp Tutorial](https://www.datacamp.com/tutorial/json-data-python)).

- **GitHub Documentation:** Guidelines and formatting syntax for writing a clear and structured `README.md` file ([GitHub Docs](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)).

- **DataCamp - Dictionary Methods:** Used as a reference for secure key access and modification using methods like `.get()` ([DataCamp Dictionary Methods](https://www.datacamp.com/tutorial/python-dictionary-methods)).

- **Python `next()` Function:** Used in combination with a generator expression to efficiently find and retrieve the first matching server dictionary by name. The default `None` argument was utilized to safely handle cases where no match is found 
  - [tutorialspoint](https://www.tutorialspoint.com/python/python_next_function.htm)
  - [Youtube](https://www.youtube.com/watch?v=3E9bS-W-4Wc) 

- **Ping info:** About ping and how it works.
[computerhope](https://www.computerhope.com/jargon/p/ping.htm) 

- **Argparse:** Referenced to better understand how to build command-line interfaces and handle arguments using Python's standard library.
  - [YouTube](https://www.youtube.com/watch?v=BOrEO-GLTQA)
  - [Python Docs](https://docs.python.org/3/library/argparse.html)
  - [Real Python](https://realpython.com/command-line-interfaces-python-argparse/)

- **AI (Artificial Intelligence):** Helped me with explanations whenever there was something I didn't understand. Used as a sounding board when I needed to talk about my ideas, and helped me find relevant documentation and resources for the information I was looking for.