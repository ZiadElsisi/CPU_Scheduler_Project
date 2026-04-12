import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit,
    QFormLayout, QDialogButtonBox, QStatusBar, QFrame, QHBoxLayout, QLabel
)


# Main Window
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Scheduler - Task 1")
        self.resize(900, 600)

        # Centeral widget :
        central_widget = QWidget()
        # Main Layout--> Contains Table / chats And Buttons
        mainlayout = QVBoxLayout()
        Header = QLabel("WELCOME TO CPU SCHEDULER")
        Header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Header.setStyleSheet("""
background-color: #111827;
color: #E5E7EB;
font-size: 26px;
font-weight: bold;
padding: 20px;
border-radius: 10px;
""")
        mainlayout.addWidget(Header)
        # TableChartLayout -- > Contains Table / Chart
        TableChartLayout = QHBoxLayout()
        Table = QFrame()

        Table.setStyleSheet("background-color: red;")

        Chart = QFrame()
        Chart.setStyleSheet("background-color: blue;")

        TableChartLayout.addWidget(Table)
        TableChartLayout.addWidget(Chart)
        TableChartLayout.setStretch(0, 1)
        TableChartLayout.setStretch(1, 2)
        mainlayout.addLayout(TableChartLayout)

        # Add Button
        self.add_btn = QPushButton("Add Process")
        self.add_btn.setStyleSheet("""
QPushButton {
    background-color: #3498db;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1c5980;
}
""")
        self.Start_Btn = QPushButton("Start")
        self.Start_Btn.setStyleSheet("""
QPushButton {
    background-color: #3498db;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1c5980;
}
""")
        ButtonsContainer = QHBoxLayout()
        ButtonsContainer.addWidget(self.add_btn)
        ButtonsContainer.addWidget(self.Start_Btn)

        # Add to layout
        # mainlayout.addWidget(self.table)
        mainlayout.addLayout(ButtonsContainer)

        central_widget.setLayout(mainlayout)
        self.setCentralWidget(central_widget)



# Run App

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
    

    