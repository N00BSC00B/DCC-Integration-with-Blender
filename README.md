# DCC Integration

This project integrates Python with a DCC application (Maya or Blender) to manage object transforms and a simple inventory system. It consists of a DCC plugin, a local server, and a SQLite database for inventory management.

## Project Structure

```
dcc-integration
├── dcc_plugin
│   ├── __init__.py
│   ├── plugin.py
│   ├── ui.py
├── server
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── endpoints.py
├── tests
│   ├── test_plugin.py
│   ├── test_server.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Features

- **DCC Plugin**: A plugin for Maya or Blender that allows users to select objects, manipulate their transforms, and submit data to a server.
- **Local Server**: A Flask or FastAPI server that handles requests related to object transforms and inventory management.
- **SQLite Database**: A lightweight database to store inventory items and their quantities.
- **User Interface**: A responsive UI built with PyQt/PySide to display inventory and manage item transactions.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd dcc-integration
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the server:
   ```
   python -m server.app
   ```

4. Load the DCC plugin in Maya or Blender.

## Usage

- Use the DCC plugin to select objects and manipulate their transforms.
- Submit the transform data to the server to update the inventory.
- Access the inventory through the UI to add, remove, or update items.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.