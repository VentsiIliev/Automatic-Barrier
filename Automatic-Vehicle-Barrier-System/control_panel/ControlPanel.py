from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from control_panel.view.AdminPanel import AdminPanel
from view.Login import LoginLayout


class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Control Panel", self)
        self.layout.addWidget(self.label)

        # Create an instance of LoginLayout
        self.login_layout = LoginLayout(self)
        self.layout.addWidget(self.login_layout)

        self.admin_panel = AdminPanel()
        # Hide the admin panel by default
        self.admin_panel.hide()
        self.layout.addWidget(self.admin_panel)


# sample usage
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    controlPanel = ControlPanel()
    controlPanel.show()

    sys.exit(app.exec_())
