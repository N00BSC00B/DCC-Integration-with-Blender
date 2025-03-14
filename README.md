# DCC Integration with Blender

## Overview

This project integrates Blender with a FastAPI server and a PyQt-based GUI to provide a seamless workflow for managing inventory and object transformations. The system consists of three main components:

1. **Blender Plugin**: A custom Blender add-on for inventory display and object transformation.
2. **FastAPI Server**: A backend server to handle inventory and transformation requests.
3. **PyQt GUI**: A desktop application for managing inventory through a user-friendly interface.

## Features

### Blender Plugin

- **Inventory Display**: View inventory data directly in Blender's sidebar.
- **Object Transformation**: Modify object properties (position, rotation, scale) and send updates to the server.

### FastAPI Server

- **Inventory Management**: Add, remove, update, and fetch inventory items.
- **Object Transformation**: Handle transformation requests for position, rotation, and scale.
- **Endpoints**:
  - `/add-item`: Add an inventory item.
  - `/remove-item`: Remove an inventory item.
  - `/update-quantity`: Update the quantity of an inventory item.
  - `/get_inventory`: Fetch all inventory items.
  - `/transform`, `/translation`, `/rotation`, `/scale`: Handle object transformations.

### PyQt GUI

- **Inventory Management**: Add, remove, and update inventory items.
- **Search and Pagination**: Search for items and navigate through paginated results.
- **Context Menu**: Right-click options for removing or updating items.
- **Real-Time Updates**: Communicates with the FastAPI server to reflect changes instantly.

## Installation

### Prerequisites

- Python 3.10 or higher
- Blender 3.0 or higher
- SQLite (for database storage)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dcc-integration
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python -c "from server.database import create_tables; create_tables()"
   ```
4. Run the FastAPI server:
   ```bash
   python -m server.app
   ```
5. Launch the PyQt GUI:
   ```bash
   python -m ui.gui
   ```
6. Install the Blender plugin:
   - Navigate to `dcc-integration/plugin/`.
   - Zip the `blender_plugin.py` file.
   - Open Blender, go to `Edit > Preferences > Add-ons > Install`, and select the zipped file.

## Usage

### Blender Plugin

1. Open Blender and enable the "DCC Plugin" add-on in the preferences.
2. Access the plugin in the `View3D > Sidebar > DCC Plugin` tab.
3. Use the inventory panel to view inventory data.
4. Use the transformation panel to modify object properties and send updates to the server.

### PyQt GUI

1. Launch the GUI using the command:
   ```bash
   python -m ui.gui
   ```
2. Use the interface to manage inventory:
   - Add, remove, or update items.
   - Search for items using the search bar.
   - Navigate through pages using the pagination buttons.

### FastAPI Server

- The server runs on `http://127.0.0.1:8000` by default.
- Use tools like Postman or cURL to test the API endpoints.

## Project Structure

```
dcc-integration/
├── plugin/                 # Blender plugin
│   └── blender_plugin.py
├── server/                 # FastAPI server
│   ├── app.py
│   ├── endpoints.py
│   ├── database.py
│   └── __init__.py
├── ui/                     # PyQt GUI
│   ├── gui.py
│   └── __init__.py
├── tests/                  # Unit tests
│   ├── test_database.py
│   ├── test_server.py
│   └── conftest.py
├── main.py                 # Entry point for running both server and GUI
├── requirements.txt        # Python dependencies
├── LICENSE                 # License file
└── README.md               # Project documentation
```

## Testing

Run the unit tests using `pytest`:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

<div>
    <a href="https://github.com/N00BSC00B">
        <img src="https://avatars.githubusercontent.com/N00BSC00B" width="100px;" alt=""/>
        <br />
        <b>Sayan Barma</b>
    </a>
</div>
