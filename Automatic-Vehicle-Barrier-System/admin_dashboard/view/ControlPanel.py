import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QStackedWidget, QHBoxLayout, QFrame, QToolBar,
                             QStatusBar, QMainWindow, QAction, QDialog, QMessageBox)
from PyQt5.QtCore import Qt

from admin_dashboard.view.DashboardLayout import DashboardLayout
from admin_dashboard.view.ReportsLayout import ReportsLayout
from admin_dashboard.view.LoginDialog import LoginDialog
from admin_dashboard.view.UserManagementLayout import UserManagementLayout  # Import the new layout


class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logged_in_user = None  # To store the logged-in user
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Admin Control Panel - Vehicle Barrier System")
        self.setGeometry(100, 100, 1200, 800)  # Main window size

        # Apply modern styles with color scheme inspired from plproject.net
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9f9f9;
                color: #4c4c4c;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #4c87b9;  /* Button color matching the site's blue */
                color: white;
                border: none;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #3a6c94;  /* Hover color for buttons */
            }
            QPushButton:pressed {
                background-color: #2b516e;  /* Pressed color for buttons */
            }
            QFrame {
                background-color: #f3f3f3;  /* Sidebar light gray */
                border-radius: 10px;
                padding: 10px;
            }
            QToolBar {
                background-color: #f3f3f3;
                border-bottom: 2px solid #4c87b9;
            }
            QStatusBar {
                background-color: #e6e6e6;  /* Status bar light gray */
                color: #4c4c4c;
            }
            QStackedWidget {
                background-color: #ffffff;  /* White background for the content area */
            }
        """)

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
        self.createReportsLayout()  # Adding the Reports Layout
        self.createUserManagementLayout()  # Adding the User Management Layout

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

    def createReportsLayout(self):
        """Create the Reports layout for generating and filtering reports."""
        self.reportsPanel = ReportsLayout(self)
        self.stackedWidget.addWidget(self.reportsPanel)

    def createUserManagementLayout(self):
        """Create the User Management layout for managing users."""
        self.userManagementPanel = UserManagementLayout(self)
        self.stackedWidget.addWidget(self.userManagementPanel)

    def createSidebar(self):
        """Create the sidebar with navigation buttons."""
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)

        sidebarLayout = QVBoxLayout(sidebar)

        # Create buttons for switching layouts
        dashboardButton = QPushButton("Dashboard", self)
        reportsButton = QPushButton("Reports", self)
        userManagementButton = QPushButton("User Management", self)  # New button for user management

        # Style the buttons
        dashboardButton.setObjectName("sidebarButton")
        reportsButton.setObjectName("sidebarButton")
        userManagementButton.setObjectName("sidebarButton")  # Style for new button

        # Connect buttons to layout switches
        dashboardButton.clicked.connect(lambda: self.switchLayout(0))
        reportsButton.clicked.connect(lambda: self.switchLayout(1))
        userManagementButton.clicked.connect(lambda: self.switchLayout(2))  # Connect to user management layout

        # Add buttons to sidebar layout
        sidebarLayout.addWidget(dashboardButton)
        sidebarLayout.addWidget(reportsButton)
        sidebarLayout.addWidget(userManagementButton)  # Add user management button

        sidebarLayout.addStretch()  # Push buttons to the top

        self.mainLayout.addWidget(sidebar, 1)  # Add sidebar to the main layout
        self.mainLayout.addWidget(self.stackedWidget, 4)  # Add stackedWidget for content area

    def createToolBar(self):
        """Create a top toolbar for quick access actions."""
        toolbar = QToolBar("Quick Actions", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Logout Action
        logoutAction = QAction("Logout", self)
        logoutAction.triggered.connect(self.logout)

        # Add logout action to the toolbar
        toolbar.addAction(logoutAction)

    def logout(self):
        """Logs the user out and returns to the login screen."""
        reply = QMessageBox.question(self, 'Confirm Logout',
                                     "Are you sure you want to log out?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.logged_in_user = None  # Clear the current user
            self.statusBar.showMessage("Logged out.")
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
