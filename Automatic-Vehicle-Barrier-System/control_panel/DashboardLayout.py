from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox

from API.SingletonDatabase import SingletonDatabase
from model.Vehicle import Vehicle
from model.access_events.AccessLevel import AccessLevel
from repositories.csv_repositories.Constants import ACCESS_LEVEL, REGISTRATION_NUMBER, OWNER


class DashboardLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_vehicle = None  # Track the currently selected vehicle
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
        self.vehicleTable.setColumnCount(3)  # Adding Owner column
        self.vehicleTable.setHorizontalHeaderLabels(["Registration", "Access Level", "Owner"])
        self.vehicleTable.itemSelectionChanged.connect(self.on_vehicle_selected)  # Handle row selection
        layout.addWidget(self.vehicleTable)

        # Add/Update Vehicle Section
        addVehicleLayout = QHBoxLayout()
        addVehicleLabel = QLabel("Vehicle Registration:", self)
        self.addVehicleInput = QLineEdit(self)
        self.addVehicleInput.setPlaceholderText("Enter Registration")

        addAccessLevelLabel = QLabel("Access Level:", self)
        self.addAccessLevelInput = QComboBox(self)
        self.addAccessLevelInput.addItems([level.name for level in AccessLevel])

        addOwnerLabel = QLabel("Owner:", self)
        self.addOwnerInput = QLineEdit(self)
        self.addOwnerInput.setPlaceholderText("Enter Owner")

        addVehicleButton = QPushButton("Add Vehicle", self)
        addVehicleButton.clicked.connect(self.addVehicle)

        updateVehicleButton = QPushButton("Update Vehicle", self)  # New update button
        updateVehicleButton.clicked.connect(self.updateVehicle)

        addVehicleLayout.addWidget(addVehicleLabel)
        addVehicleLayout.addWidget(self.addVehicleInput)
        addVehicleLayout.addWidget(addAccessLevelLabel)
        addVehicleLayout.addWidget(self.addAccessLevelInput)
        addVehicleLayout.addWidget(addOwnerLabel)
        addVehicleLayout.addWidget(self.addOwnerInput)
        addVehicleLayout.addWidget(addVehicleButton)
        addVehicleLayout.addWidget(updateVehicleButton)

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
        self.searchAccessLevelInput.addItems(["Any"] + [level.name for level in AccessLevel])

        searchButton = QPushButton("Search", self)
        searchButton.clicked.connect(self.searchVehicle)

        searchLayout.addWidget(searchVehicleLabel)
        searchLayout.addWidget(self.searchVehicleInput)
        searchLayout.addWidget(searchAccessLevelLabel)
        searchLayout.addWidget(self.searchAccessLevelInput)
        searchLayout.addWidget(searchButton)

        layout.addLayout(searchLayout)

        # Load whitelisted vehicles into the table
        self.loadVehicleTable()

        self.setLayout(layout)

    def loadVehicleTable(self):
        """Load the whitelisted vehicles into the table."""
        vehicles = SingletonDatabase().getInstance().get_repo('whitelisted').get_all()
        self.vehicleTable.setRowCount(len(vehicles))

        for row, vehicle in enumerate(vehicles):
            registration_number = vehicle.registration_number
            access_level = AccessLevel(vehicle.access_level).name  # Convert access level to name
            owner = vehicle.owner  # Assume OWNER is in your CSV structure
            self.vehicleTable.setItem(row, 0, QTableWidgetItem(registration_number))
            self.vehicleTable.setItem(row, 1, QTableWidgetItem(access_level))
            self.vehicleTable.setItem(row, 2, QTableWidgetItem(owner))

    def on_vehicle_selected(self):
        """Handle vehicle selection from the table."""
        selected_row = self.vehicleTable.currentRow()

        if selected_row >= 0:
            self.selected_vehicle = self.vehicleTable.item(selected_row, 0).text()  # Store selected registration number

            # Populate input fields with the selected vehicle's details
            self.addVehicleInput.setText(self.vehicleTable.item(selected_row, 0).text())  # Registration
            self.addAccessLevelInput.setCurrentText(self.vehicleTable.item(selected_row, 1).text())  # Access Level
            self.addOwnerInput.setText(self.vehicleTable.item(selected_row, 2).text())  # Owner

            # Populate the remove vehicle field
            self.removeVehicleInput.setText(self.vehicleTable.item(selected_row, 0).text())  # Registration for removal

    def updateVehicle(self):
        """Update the selected vehicle's information."""
        if not self.selected_vehicle:
            QMessageBox.warning(self, 'Error', 'No vehicle selected.')
            return

        registration = self.addVehicleInput.text().upper()
        access_level = self.addAccessLevelInput.currentText()
        owner = self.addOwnerInput.text()

        if not registration or not access_level or not owner:
            QMessageBox.warning(self, 'Error', 'Please enter registration, access level, and owner.')
            return

        # Ask for confirmation before updating
        confirmation = QMessageBox.question(self, 'Update Confirmation',
                                            f"Are you sure you want to update vehicle {self.selected_vehicle}?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            access_level_value = AccessLevel[access_level].value
            # Update the vehicle's information
            vehicle_repo = SingletonDatabase().getInstance().get_repo('whitelisted')
            vehicle_repo.update(registration, owner, access_level_value)  # Assume an update method exists

            self.loadVehicleTable()
            self.addVehicleInput.clear()
            self.addOwnerInput.clear()
            self.removeVehicleInput.clear()
            self.selected_vehicle = None

    def addVehicle(self):
        """Add a new vehicle to the whitelist."""
        registration = self.addVehicleInput.text().upper()
        access_level = self.addAccessLevelInput.currentText()
        owner = self.addOwnerInput.text()

        if not registration or not access_level or not owner:
            QMessageBox.warning(self, 'Error', 'Please enter registration, access level, and owner.')
            return

        access_level_value = AccessLevel[access_level].value
        vehicle = Vehicle(registration, owner, access_level_value)
        vehicles = SingletonDatabase().getInstance().get_repo('whitelisted').get_all()

        for v in vehicles:
            if v.registration_number == registration:
                QMessageBox.warning(self, 'Error', 'Vehicle is already whitelisted.')
                return

        SingletonDatabase().getInstance().get_repo('whitelisted').insert(vehicle)
        self.loadVehicleTable()
        self.addVehicleInput.clear()
        self.addOwnerInput.clear()

    def removeVehicle(self):
        """Remove a vehicle from the whitelist."""
        registration = self.removeVehicleInput.text().upper()

        if registration:
            # Ask for confirmation before deleting
            confirmation = QMessageBox.question(self, 'Delete Confirmation',
                                                f"Are you sure you want to remove vehicle {registration}?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                SingletonDatabase().getInstance().get_repo('whitelisted').delete(registration)
                self.loadVehicleTable()
                self.removeVehicleInput.clear()

    def searchVehicle(self):
        """Search vehicles by registration and access level."""
        search_reg = self.searchVehicleInput.text().upper()
        search_access_level = self.searchAccessLevelInput.currentText()

        vehicles = SingletonDatabase().getInstance().get_repo('whitelisted').get_all()
        filtered_vehicles = []

        for vehicle in vehicles:
            access_level = AccessLevel(vehicle.access_level).name
            if (not search_reg or vehicle.registration_number == search_reg) and \
               (search_access_level == "Any" or access_level == search_access_level):
                filtered_vehicles.append(vehicle)

        self.vehicleTable.setRowCount(len(filtered_vehicles))
        for row, vehicle in enumerate(filtered_vehicles):
            registration_number = vehicle.registration_number
            access_level = AccessLevel(vehicle.access_level).name  # Convert access level to name
            owner = vehicle.owner  # Assume OWNER is in your CSV structure
            self.vehicleTable.setItem(row, 0, QTableWidgetItem(registration_number))
            self.vehicleTable.setItem(row, 1, QTableWidgetItem(access_level))
            self.vehicleTable.setItem(row, 2, QTableWidgetItem(owner))
