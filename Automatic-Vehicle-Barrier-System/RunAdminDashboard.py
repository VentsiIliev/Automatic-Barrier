import sys

from PyQt5.QtWidgets import QApplication

from admin_dashboard.view.ControlPanel import ControlPanel

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ControlPanel()
    window.show()
    sys.exit(app.exec_())