from PyQt5 import QtWidgets, QtCore

class DCCPluginUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCC Plugin Interface")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QtWidgets.QVBoxLayout()

        self.object_selection = QtWidgets.QComboBox()
        self.layout.addWidget(QtWidgets.QLabel("Select Object:"))
        self.layout.addWidget(self.object_selection)

        self.transform_controls = QtWidgets.QGroupBox("Transform Controls")
        self.transform_layout = QtWidgets.QFormLayout()
        self.position_input = QtWidgets.QLineEdit()
        self.rotation_input = QtWidgets.QLineEdit()
        self.scale_input = QtWidgets.QLineEdit()
        self.transform_layout.addRow("Position:", self.position_input)
        self.transform_layout.addRow("Rotation:", self.rotation_input)
        self.transform_layout.addRow("Scale:", self.scale_input)
        self.transform_controls.setLayout(self.transform_layout)
        self.layout.addWidget(self.transform_controls)

        self.endpoint_dropdown = QtWidgets.QComboBox()
        self.layout.addWidget(QtWidgets.QLabel("Select Endpoint:"))
        self.layout.addWidget(self.endpoint_dropdown)

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def update_transform_controls(self, position, rotation, scale):
        self.position_input.setText(str(position))
        self.rotation_input.setText(str(rotation))
        self.scale_input.setText(str(scale))