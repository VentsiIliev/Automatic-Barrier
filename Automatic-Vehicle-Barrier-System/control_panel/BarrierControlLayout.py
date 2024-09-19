from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox

class BarrierControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """Initialize the barrier control layout."""
        layout = QVBoxLayout()

        # Barrier Control Title
        titleLabel = QLabel("Barrier Control", self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(titleLabel)

        # Control Buttons
        controlLayout = QHBoxLayout()

        openBarrierButton = QPushButton("Open Barrier", self)
        openBarrierButton.clicked.connect(self.openBarrier)

        closeBarrierButton = QPushButton("Close Barrier", self)
        closeBarrierButton.clicked.connect(self.closeBarrier)

        controlLayout.addWidget(openBarrierButton)
        controlLayout.addWidget(closeBarrierButton)

        layout.addLayout(controlLayout)

        # Finalize Layout
        self.setLayout(layout)

    def openBarrier(self):
        """Open the vehicle barrier."""
        QMessageBox.information(self, "Barrier Control", "Opening barrier...")
        # Here you would add the actual command to open the barrier

    def closeBarrier(self):
        """Close the vehicle barrier."""
        QMessageBox.information(self, "Barrier Control", "Closing barrier...")
        # Here you would add the actual command to close the barrier
