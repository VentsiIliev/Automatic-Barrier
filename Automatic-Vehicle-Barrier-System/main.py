# Main application
import sys

from PyQt5.QtWidgets import QApplication

from AVBS import AVBS

if __name__ == "__main__":
    avbs = AVBS()

    # Start the Qt application event loop
    sys.exit(QApplication.exec_())
