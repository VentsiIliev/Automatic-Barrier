from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox

class DashboardLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.whitelisted_vehicles = []  # Store whitelisted vehicles
        self.initUI()

    def initUI(self):
        """Initialize the dashboard layout."""
        layout = QVBoxLayout()

        # Dashboard Title
        label = QLabel("Dashboard - Manage Whitelisted Vehicles", self)
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label)

        # Whitelisted Vehicles Section
        vehicleListLabel = QLabel("Whitelisted Vehicles", self)
        layout.addWidget(vehicleListLabel)

        # Vehicle Table
        self.vehicleTable = QTableWidget()
        self.vehicleTable.setColumnCount(2)
        self.vehicleTable.setHorizontalHeaderLabels(["Registration", "Access Level"])
        layout.addWidget(self.vehicleTable)

        # Add Vehicle Section
        addVehicleLayout = QHBoxLayout()
        addVehicleLabel = QLabel("Add New Vehicle:", self)
        self.addVehicleInput = QLineEdit(self)
        self.addVehicleInput.setPlaceholderText("Enter Registration")

        addAccessLevelLabel = QLabel("Access Level:", self)
        self.addAccessLevelInput = QComboBox(self)
        self.addAccessLevelInput.addItems(["Admin", "User", "Guest"])

        addVehicleButton = QPushButton("Add Vehicle", self)
        addVehicleButton.clicked.connect(self.addVehicle)

        addVehicleLayout.addWidget(addVehicleLabel)
        addVehicleLayout.addWidget(self.addVehicleInput)
        addVehicleLayout.addWidget(addAccessLevelLabel)
        addVehicleLayout.addWidget(self.addAccessLevelInput)
        addVehicleLayout.addWidget(addVehicleButton)

        layout.addLayout(addVehicleLayout)

        # Remove Vehicle Section
        removeVehicleLayout = QHBoxLayout()
        removeVehicleLabel = QLabel("Remove Vehicle:", self)
        self.removeVehicleInput = QLineEdit(self)
        self.removeVehicleInput.setPlaceholderText("Enter Registration")

        removeVehicleButton = QPushButton("Remove Vehicle", self)
        removeVehicleButton.clicked.connect(self.removeVehicle)

        removeVehicleLayout.addWidget(removeVehicleLabel)
        removeVehicleLayout.addWidget(self.removeVehicleInput)
        removeVehicleLayout.addWidget(removeVehicleButton)

        layout.addLayout(removeVehicleLayout)

        # Search Vehicle Section
        searchLayout = QHBoxLayout()
        searchVehicleLabel = QLabel("Search by Registration:", self)
        self.searchVehicleInput = QLineEdit(self)
        self.searchVehicleInput.setPlaceholderText("Enter Registration")

        searchAccessLevelLabel = QLabel("Access Level:", self)
        self.searchAccessLevelInput = QComboBox(self)
        self.searchAccessLevelInput.addItems(["", "Admin", "User", "Guest"])  # Add empty string for "any"

        searchButton = QPushButton("Search", self)
        searchButton.clicked.connect(self.searchVehicle)

        searchLayout.addWidget(searchVehicleLabel)
        searchLayout.addWidget(self.searchVehicleInput)
        searchLayout.addWidget(searchAccessLevelLabel)
        searchLayout.addWidget(self.searchAccessLevelInput)
        searchLayout.addWidget(searchButton)

        layout.addLayout(searchLayout)

        # Placeholder data for whitelisted vehicles
        self.whitelisted_vehicles = [
            {"registration": "ABC123", "access_level": "User"},
            {"registration": "XYZ789", "access_level": "Admin"}
        ]

        # Load whitelisted vehicles into the table
        self.loadVehicleTable()

        self.setLayout(layout)

    def loadVehicleTable(self):
        """Load the whitelisted vehicles into the table."""
        self.vehicleTable.setRowCount(len(self.whitelisted_vehicles))
        for row, vehicle in enumerate(self.whitelisted_vehicles):
            self.vehicleTable.setItem(row, 0, QTableWidgetItem(vehicle["registration"]))
            self.vehicleTable.setItem(row, 1, QTableWidgetItem(vehicle["access_level"]))

    def addVehicle(self):
        """Add a new vehicle to the whitelist."""
        registration = self.addVehicleInput.text().upper()
        access_level = self.addAccessLevelInput.currentText()

        if registration and access_level:
            # Check if the vehicle is already in the list
            for vehicle in self.whitelisted_vehicles:
                if vehicle["registration"] == registration:
                    QMessageBox.warning(self, 'Error', 'Vehicle is already whitelisted.')
                    return

            # Add the new vehicle
            self.whitelisted_vehicles.append({"registration": registration, "access_level": access_level})
            self.loadVehicleTable()
            self.addVehicleInput.clear()

    def removeVehicle(self):
        """Remove a vehicle from the whitelist."""
        registration = self.removeVehicleInput.text().upper()

        if registration:
            self.whitelisted_vehicles = [v for v in self.whitelisted_vehicles if v["registration"] != registration]
            self.loadVehicleTable()
            self.removeVehicleInput.clear()

    def searchVehicle(self):
        """Search vehicles by registration and access level."""
        search_reg = self.searchVehicleInput.text().upper()
        search_access_level = self.searchAccessLevelInput.currentText()

        # Filter the vehicles
        filtered_vehicles = []
        for vehicle in self.whitelisted_vehicles:
            if (not search_reg or vehicle["registration"] == search_reg) and \
               (not search_access_level or vehicle["access_level"] == search_access_level):
                filtered_vehicles.append(vehicle)

        # Update the table with filtered results
        self.vehicleTable.setRowCount(len(filtered_vehicles))
        for row, vehicle in enumerate(filtered_vehicles):
            self.vehicleTable.setItem(row, 0, QTableWidgetItem(vehicle["registration"]))
            self.vehicleTable.setItem(row, 1, QTableWidgetItem(vehicle["access_level"]))
