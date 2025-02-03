import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QInputDialog
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# FastAPI server URL
SERVER_URL = "http://127.0.0.1:8000"


class Worker(QThread):
    data_ready = pyqtSignal(list)
    operation_complete = pyqtSignal(str)

    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation
        self.args = args

    def run(self):
        try:
            if self.operation == "get_inventory":
                response = requests.get(f"{SERVER_URL}/get_inventory")
                if response.status_code == 200:
                    inventory = response.json()["inventory"]
                    self.data_ready.emit(inventory)
                else:
                    self.operation_complete.emit(f"Error: {response.text}")

            elif self.operation == "update_quantity":
                name, new_quantity = self.args
                response = requests.post(
                    f"{SERVER_URL}/update-quantity",
                    json={"name": name, "new_quantity": new_quantity}
                )
                if response.status_code == 200:
                    self.operation_complete.emit(
                        "Quantity updated successfully"
                    )
                else:
                    self.operation_complete.emit(f"Error: {response.text}")

            elif self.operation == "add_item":
                name, quantity = self.args
                response = requests.post(
                    f"{SERVER_URL}/add-item",
                    json={"name": name, "quantity": quantity}
                )
                if response.status_code == 201:
                    self.operation_complete.emit(
                        f"Item {name} added successfully"
                    )
                else:
                    self.operation_complete.emit(f"Error: {response.text}")

            elif self.operation == "remove_item":
                name = self.args[0]
                response = requests.post(
                    f"{SERVER_URL}/remove-item",
                    json={"name": name}
                )
                if response.status_code == 200:
                    self.operation_complete.emit(
                        f"Item {name} removed successfully"
                    )
                else:
                    self.operation_complete.emit(f"Error: {response.text}")

        except Exception as e:
            self.operation_complete.emit(f"Error: {e}")


class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Quantity"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                gridline-color: #444444;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 5px;
                font-size: 16px;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: #ffffff;
            }
        """)
        self.layout.addWidget(self.table)

        # Buttons Layout
        self.button_layout_top = QHBoxLayout()
        self.button_layout_bottom = QHBoxLayout()

        # Purchase and Return Buttons (Top Row)
        self.purchase_button = QPushButton("Purchase Item")
        self.return_button = QPushButton("Return Item")

        self.purchase_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.return_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)

        self.button_layout_top.addWidget(self.purchase_button)
        self.button_layout_top.addWidget(self.return_button)

        # Add Item, Remove Item, and Update Quantity Buttons (Bottom Row)
        self.add_item_button = QPushButton("Add Item")
        self.remove_item_button = QPushButton("Remove Item")
        self.update_quantity_button = QPushButton("Update Quantity")

        self.add_item_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        self.remove_item_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
        """)

        self.update_quantity_button.setStyleSheet("""
            QPushButton {
                background-color: #9c27b0;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7b1fa2;
            }
        """)

        self.button_layout_bottom.addWidget(self.add_item_button)
        self.button_layout_bottom.addWidget(self.remove_item_button)
        self.button_layout_bottom.addWidget(self.update_quantity_button)

        # Add button layouts to the main layout
        self.layout.addLayout(self.button_layout_top)
        self.layout.addLayout(self.button_layout_bottom)

        # Connect buttons to their respective handlers
        self.purchase_button.clicked.connect(self.handle_purchase)
        self.return_button.clicked.connect(self.handle_return)
        self.add_item_button.clicked.connect(self.handle_add_item)
        self.remove_item_button.clicked.connect(self.handle_remove_item)
        self.update_quantity_button.clicked.connect(
            self.handle_update_quantity
        )

        self.load_inventory()

    def load_inventory(self):
        self.worker = Worker("get_inventory")
        self.worker.data_ready.connect(self.update_table)
        self.worker.operation_complete.connect(self.handle_operation_complete)
        self.worker.start()

    def update_table(self, inventory):
        self.table.setRowCount(len(inventory))
        for row, item in enumerate(inventory):
            name_item = QTableWidgetItem(item["name"])
            name_item.setFlags(
                name_item.flags() & ~Qt.ItemFlag.ItemIsEditable
            )
            self.table.setItem(row, 0, name_item)

            quantity_item = QTableWidgetItem(str(item["quantity"]))
            quantity_item.setFlags(
                quantity_item.flags() & ~Qt.ItemFlag.ItemIsEditable
            )
            self.table.setItem(row, 1, quantity_item)

    def handle_purchase(self):
        self.update_quantity(-1)

    def handle_return(self):
        self.update_quantity(1)

    def update_quantity(self, delta):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select an item.")
            return

        item_name = self.table.item(selected_row, 0).text()
        current_quantity = int(self.table.item(selected_row, 1).text())
        new_quantity = current_quantity + delta

        if new_quantity < 0:
            QMessageBox.warning(
                self,
                "Invalid Operation", "Quantity cannot be negative."
            )
            return

        self.worker = Worker("update_quantity", item_name, new_quantity)
        self.worker.operation_complete.connect(self.handle_operation_complete)
        self.worker.start()

    def handle_add_item(self):
        name, ok = QInputDialog.getText(self, "Add Item", "Enter item name:")
        if not ok or not name.strip():
            return

        quantity, ok = QInputDialog.getInt(
            self,
            "Add Item", "Enter quantity:",
            1,
            0,
            9999
        )
        if not ok:
            return

        self.worker = Worker("add_item", name.strip(), quantity)
        self.worker.operation_complete.connect(self.handle_operation_complete)
        self.worker.start()

    def handle_remove_item(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select an item to remove."
            )
            return

        item_name = self.table.item(selected_row, 0).text()
        self.worker = Worker("remove_item", item_name)
        self.worker.operation_complete.connect(self.handle_operation_complete)
        self.worker.start()

    def handle_update_quantity(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select an item.")
            return

        item_name = self.table.item(selected_row, 0).text()
        new_quantity, ok = QInputDialog.getInt(
            self,
            "Update Quantity",
            f"Enter new quantity for {item_name}:",
            0,
            0,
            9999
        )
        if not ok:
            return

        self.worker = Worker("update_quantity", item_name, new_quantity)
        self.worker.operation_complete.connect(self.handle_operation_complete)
        self.worker.start()

    def handle_operation_complete(self, message):
        if message.startswith("Error"):
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Success", message)
            self.load_inventory()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
