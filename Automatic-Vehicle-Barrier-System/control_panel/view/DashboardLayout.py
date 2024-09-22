from PyQt5.QtWidgets import QLabel, QMessageBox, QHBoxLayout

from API.SingletonDatabase import SingletonDatabase
from control_panel.Settings import Settings
from control_panel.data_managment.ReportType import ReportType
from control_panel.view.BaseTableLayout import BaseLayout
from control_panel.data_managment.Filter import Filter
from control_panel.model.Vehicle import Vehicle
from model.access_events.AccessLevel import AccessLevel

# Constants for Layout and Titles
CSV_FILE = Settings.WHITELISTED_CSV
TABLE_HEADERS = ["Registration", "Access Level", "Owner"]
LAYOUT_TITLE = "Dashboard - Manage Whitelisted Vehicles"
WHITELISTED_VEHICLES_LABEL = "Whitelisted Vehicles"
VEHICLE_REGISTRATION_LABEL = "Vehicle Registration:"
ACCESS_LEVEL_LABEL = "Access Level:"
OWNER_LABEL = "Owner:"
REMOVE_VEHICLE_LABEL = "Remove Vehicle:"
SEARCH_REGISTRATION_LABEL = "Search by Registration:"
SEARCH_ACCESS_LEVEL_LABEL = "Access Level:"
ADD_VEHICLE_BUTTON_LABEL = "Add Vehicle"
UPDATE_VEHICLE_BUTTON_LABEL = "Update Vehicle"
REMOVE_VEHICLE_BUTTON_LABEL = "Remove Vehicle"
SEARCH_BUTTON_LABEL = "Search"

# Warning Messages
WARNING_MESSAGE_NO_VEHICLE_SELECTED = "No vehicle selected."
WARNING_MESSAGE_ENTER_DETAILS = "Please enter registration, access level, and owner."
WARNING_MESSAGE_VEHICLE_ALREADY_WHITELISTED = "Vehicle is already whitelisted."
CONFIRM_UPDATE_TITLE = "Update Confirmation"
CONFIRM_UPDATE_MESSAGE = "Are you sure you want to update vehicle {}?"
CONFIRM_DELETE_TITLE = "Delete Confirmation"
CONFIRM_DELETE_MESSAGE = "Are you sure you want to remove vehicle {}?"


class DashboardLayout(BaseLayout):
    def __init__(self, parent=None):
        super().__init__(LAYOUT_TITLE, TABLE_HEADERS, parent)
        self.selected_vehicle = None  # Track the currently selected vehicle
        self.initUI()


    def initUI(self):
        """Initialize the dashboard layout."""
        # Whitelisted Vehicles Section
        vehicleListLabel = QLabel(WHITELISTED_VEHICLES_LABEL, self)
        self.layout.addWidget(vehicleListLabel)

        # Add/Update Vehicle Section
        addVehicleLayout = QHBoxLayout()
        addVehicleLabel = QLabel(VEHICLE_REGISTRATION_LABEL, self)
        self.addVehicleInput = self.addInputField("Enter Registration")

        addAccessLevelLabel = QLabel(ACCESS_LEVEL_LABEL, self)
        self.addAccessLevelInput = self.addComboBox([level.name for level in AccessLevel])

        addOwnerLabel = QLabel(OWNER_LABEL, self)
        self.addOwnerInput = self.addInputField("Enter Owner")

        addVehicleButton = self.addButton(ADD_VEHICLE_BUTTON_LABEL, self.addVehicle)
        updateVehicleButton = self.addButton(UPDATE_VEHICLE_BUTTON_LABEL, self.updateVehicle)

        addVehicleLayout.addWidget(addVehicleLabel)
        addVehicleLayout.addWidget(self.addVehicleInput)
        addVehicleLayout.addWidget(addAccessLevelLabel)
        addVehicleLayout.addWidget(self.addAccessLevelInput)
        addVehicleLayout.addWidget(addOwnerLabel)
        addVehicleLayout.addWidget(self.addOwnerInput)
        addVehicleLayout.addWidget(addVehicleButton)
        addVehicleLayout.addWidget(updateVehicleButton)

        self.layout.addLayout(addVehicleLayout)

        # Remove Vehicle Section
        removeVehicleLayout = QHBoxLayout()
        removeVehicleLabel = QLabel(REMOVE_VEHICLE_LABEL, self)
        self.removeVehicleInput = self.addInputField("Enter Registration")

        removeVehicleButton = self.addButton(REMOVE_VEHICLE_BUTTON_LABEL, self.removeVehicle)
        removeVehicleLayout.addWidget(removeVehicleLabel)
        removeVehicleLayout.addWidget(self.removeVehicleInput)
        removeVehicleLayout.addWidget(removeVehicleButton)

        self.layout.addLayout(removeVehicleLayout)

        # Search Vehicle Section
        searchLayout = QHBoxLayout()
        searchVehicleLabel = QLabel(SEARCH_REGISTRATION_LABEL, self)
        self.searchVehicleInput = self.addInputField("Enter Registration")

        searchAccessLevelLabel = QLabel(SEARCH_ACCESS_LEVEL_LABEL, self)
        self.searchAccessLevelInput = self.addComboBox(["Any"] + [level.name for level in AccessLevel])

        searchButton = self.addButton(SEARCH_BUTTON_LABEL, self.search_vehicle)

        searchLayout.addWidget(searchVehicleLabel)
        searchLayout.addWidget(self.searchVehicleInput)
        searchLayout.addWidget(searchAccessLevelLabel)
        searchLayout.addWidget(self.searchAccessLevelInput)
        searchLayout.addWidget(searchButton)

        self.layout.addLayout(searchLayout)

        self.addTable(3, TABLE_HEADERS)

        # Connect row selection to the handler
        self.table.itemSelectionChanged.connect(self.on_vehicle_selected)

        # Load whitelisted vehicles into the table
        self.loadVehicleTable()

    def loadVehicleTable(self):
        """Load the whitelisted vehicles into the table."""
        vehicles = SingletonDatabase().getInstance().get_repo(CSV_FILE).get_all()
        self.populate_table([[vehicle.registration_number,
                              AccessLevel(vehicle.access_level).name,
                              vehicle.owner] for vehicle in vehicles])

    def on_vehicle_selected(self):
        """Handle vehicle selection from the table."""
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Store selected registration number
            self.selected_vehicle = self.table.item(selected_row, 0).text()

            # Populate input fields with the selected vehicle's details
            self.addVehicleInput.setText(self.table.item(selected_row, 0).text())  # Registration
            self.addAccessLevelInput.setCurrentText(self.table.item(selected_row, 1).text())  # Access Level
            self.addOwnerInput.setText(self.table.item(selected_row, 2).text())  # Owner

            # Populate the remove vehicle field
            self.removeVehicleInput.setText(self.table.item(selected_row, 0).text())  # Registration for removal
        else:
            # Clear the input fields if no vehicle is selected
            self.selected_vehicle = None
            self.addVehicleInput.clear()
            self.addAccessLevelInput.setCurrentIndex(0)  # Reset access level to default
            self.addOwnerInput.clear()
            self.removeVehicleInput.clear()


    def updateVehicle(self):
        """Update the selected vehicle's information."""
        if not self.selected_vehicle:
            QMessageBox.warning(self, 'Error', WARNING_MESSAGE_NO_VEHICLE_SELECTED)
            return

        registration = self.addVehicleInput.text().upper()
        access_level = self.addAccessLevelInput.currentText()
        owner = self.addOwnerInput.text()

        if not registration or not access_level or not owner:
            QMessageBox.warning(self, 'Error', WARNING_MESSAGE_ENTER_DETAILS)
            return

        # Ask for confirmation before updating
        confirmation = QMessageBox.question(self, CONFIRM_UPDATE_TITLE,
                                            CONFIRM_UPDATE_MESSAGE.format(self.selected_vehicle),
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
            QMessageBox.warning(self, 'Error', WARNING_MESSAGE_ENTER_DETAILS)
            return

        access_level_value = AccessLevel[access_level].value
        vehicle = Vehicle(registration, owner, access_level_value)
        vehicles = SingletonDatabase().getInstance().get_repo(CSV_FILE).get_all()

        for v in vehicles:
            if v.registration_number == registration:
                QMessageBox.warning(self, 'Error', WARNING_MESSAGE_VEHICLE_ALREADY_WHITELISTED)
                return

        SingletonDatabase().getInstance().get_repo(CSV_FILE).insert(vehicle)
        self.loadVehicleTable()
        self.addVehicleInput.clear()
        self.addOwnerInput.clear()

    def removeVehicle(self):
        """Remove a vehicle from the whitelist."""
        registration = self.removeVehicleInput.text().upper()

        if registration:
            # Ask for confirmation before deleting
            confirmation = QMessageBox.question(self, CONFIRM_DELETE_TITLE,
                                                CONFIRM_DELETE_MESSAGE.format(registration),
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                SingletonDatabase().getInstance().get_repo(CSV_FILE).delete(registration)
                self.loadVehicleTable()
                self.removeVehicleInput.clear()

    def create_filters(self):
        """Create a filter object based on the search inputs."""
        return Filter(
            registration_number=self.searchVehicleInput.text().upper() or None,
            access_level=AccessLevel[self.searchAccessLevelInput.currentText()].value
            if self.searchAccessLevelInput.currentText() != "Any" else None
        )

    def search_vehicle(self):
        """Search vehicles based on the input filters."""
        filters = self.create_filters()
        super().generate_report(filters, report_type=ReportType.WHITELISTED)
