from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        # Create a QLabel instance
        label = QLabel("This is the admin panel")

        # Add the QLabel instance to the layout
        layout.addWidget(label)

        # Create QPushButton instances
        button1 = QPushButton("Button 1", self)
        button2 = QPushButton("Button 2", self)
        button3 = QPushButton("Button 3", self)

        # Optionally connect the clicked signal to a method
        button1.clicked.connect(self.button1_clicked)
        button2.clicked.connect(self.button2_clicked)
        button3.clicked.connect(self.button3_clicked)

        # Add the QPushButton instances to the layout
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        # Set the layout of the AdminPanel
        self.setLayout(layout)

    def button1_clicked(self):
        print("Button 1 clicked")

    def button2_clicked(self):
        print("Button 2 clicked")

    def button3_clicked(self):
        print("Button 3 clicked")

    def resizeEvent(self, event):
        # Adjust the size of the AdminPanel to match the new size of its parent widget
        self.resize(self.parent().size())
        super().resizeEvent(event)