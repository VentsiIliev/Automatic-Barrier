import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QStackedWidget, QLabel, QHBoxLayout, QFrame, QToolBar,
                             QStatusBar, QMainWindow, QAction, QLineEdit, QTableWidget,
                             QTableWidgetItem, QComboBox, QDateEdit, QDateTimeEdit, QGridLayout, QDialog, QMessageBox)
from PyQt5.QtCore import Qt, QDate

from control_panel.BarrierControlLayout import BarrierControlPanel
from control_panel.DashboardLayout import DashboardLayout
from control_panel.DashboardLayout import DashboardLayout
from control_panel.ReportsLayout import ReportsLayout
from control_panel.SystemSettingsLayout import SystemSettingsPanel
from control_panel.view.LoginDialog import LoginDialog


class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logged_in_user = None  # To store the logged-in user
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Admin Control Panel - Vehicle Barrier System")
        self.setGeometry(100, 100, 1200, 800)  # Main window size

        # Check for login at the start
        self.check_login()

        # Main container widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Main layout will have sidebar + content area
        self.mainLayout = QHBoxLayout(self.centralWidget)

        # QStackedWidget to manage multiple pages
        self.stackedWidget = QStackedWidget(self)

        # Creating multiple layouts (simulating different pages in the control panel)
        self.createDashboardLayout()
        self.createBarrierControlLayout()
        self.createSystemSettingsLayout()
        self.createReportsLayout()  # Adding the Reports Layout

        # Sidebar for navigation between layouts
        self.createSidebar()

        # Add status bar for notifications and show logged-in user
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(f"Logged in as: {self.logged_in_user}")

        # Setup ToolBar
        self.createToolBar()

    def check_login(self):
        """Prompts the user to log in before they can access the control panel."""
        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == QDialog.Accepted:
            self.logged_in_user = login_dialog.get_logged_in_user()
        else:
            sys.exit()  # Close the application if login is cancelled or failed

    def createDashboardLayout(self):

        self.dashboardPanel = DashboardLayout(self)
        self.stackedWidget.addWidget(self.dashboardPanel)

    def createBarrierControlLayout(self):
        """Create the layout for controlling the barrier."""
        self.barrierControlPanel = BarrierControlPanel(self)
        self.stackedWidget.addWidget(self.barrierControlPanel)

    def createSystemSettingsLayout(self):
        """Create the system settings layout and add it to the stack."""
        self.systemSettingsPanel = SystemSettingsPanel(self)
        self.stackedWidget.addWidget(self.systemSettingsPanel)

    def createReportsLayout(self):
        """Create the Reports layout for generating and filtering reports."""
        self.reportsPanel = ReportsLayout(self)
        self.stackedWidget.addWidget(self.reportsPanel)

    def createSidebar(self):
        """Create the sidebar with navigation buttons."""
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)

        sidebarLayout = QVBoxLayout(sidebar)

        # Create buttons for switching layouts
        dashboardButton = QPushButton("Dashboard", self)
        barrierControlButton = QPushButton("Barrier Control", self)
        systemSettingsButton = QPushButton("System Settings", self)
        reportsButton = QPushButton("Reports", self)

        # Style the buttons
        buttonStyle = """
        QPushButton {
            font-size: 18px;
            padding: 10px;
            background-color: #555;
            color: white;
        }
        QPushButton:hover {
            background-color: #777;
        }
        """

        dashboardButton.setStyleSheet(buttonStyle)
        barrierControlButton.setStyleSheet(buttonStyle)
        systemSettingsButton.setStyleSheet(buttonStyle)
        reportsButton.setStyleSheet(buttonStyle)

        # Connect buttons to layout switches
        dashboardButton.clicked.connect(lambda: self.switchLayout(0))
        barrierControlButton.clicked.connect(lambda: self.switchLayout(1))
        systemSettingsButton.clicked.connect(lambda: self.switchLayout(2))
        reportsButton.clicked.connect(lambda: self.switchLayout(3))

        # Add buttons to sidebar layout
        sidebarLayout.addWidget(dashboardButton)
        sidebarLayout.addWidget(barrierControlButton)
        if self.logged_in_user == 'admin':  # Only add the system settings button if the user is an admin
            sidebarLayout.addWidget(systemSettingsButton)
        sidebarLayout.addWidget(reportsButton)

        sidebarLayout.addStretch()  # Push buttons to the top

        self.mainLayout.addWidget(sidebar, 1)  # Add sidebar to the main layout
        self.mainLayout.addWidget(self.stackedWidget, 4)  # Add stackedWidget for content area

    def createToolBar(self):
        """Create a top toolbar for quick access actions."""
        toolbar = QToolBar("Quick Actions", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        openAction = QAction("Open Barrier", self)
        openAction.triggered.connect(lambda: self.statusBar.showMessage("Opening barrier..."))

        closeAction = QAction("Close Barrier", self)
        closeAction.triggered.connect(lambda: self.statusBar.showMessage("Closing barrier..."))

        settingsAction = QAction("Settings", self)
        settingsAction.triggered.connect(lambda: self.switchLayout(2))

        # Logout Action
        logoutAction = QAction("Logout", self)
        logoutAction.triggered.connect(self.logout)

        # Add actions to the toolbar
        toolbar.addAction(openAction)
        toolbar.addAction(closeAction)
        toolbar.addAction(settingsAction)
        toolbar.addAction(logoutAction)

    def logout(self):
        """Logs the user out and returns to the login screen."""
        self.logged_in_user = None  # Clear the current user
        self.statusBar.showMessage("Logged out.")
        # self.close()
        self.check_login()  # Prompt for login again
        self.statusBar.showMessage(f"Logged in as: {self.logged_in_user}")

    def switchLayout(self, index):
        """Switch to a specific layout in the stacked widget."""
        self.stackedWidget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ControlPanel()
    window.show()
    sys.exit(app.exec_())
