from email.mime import text
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit,
    QFormLayout, QDialogButtonBox, QStatusBar, QFrame, QHBoxLayout, QLabel
)



# Main Window
class MyWindow(QMainWindow):
    def __init__(self): 

        self.state = {
    "queue": [],
    "current": None,
    "time": 0,
    "algorithm": None
}
        super().__init__()
        self.setWindowTitle("CPU Scheduler - Task 1")
        self.resize(1100, 600)
        self.setMinimumSize(1100,600)

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
        
        #combo box for selecting scheduling algorithm
        self.combo = QComboBox()
        self.combo.setPlaceholderText("Select Algorithm")
        self.combo.addItems(["Priority Preemptive", "Priority Non-Preemptive", "Round Robin", "SJF Preemptive", "SJF Non-Preemptive"])
        self.combo.setCurrentIndex(-1)
        self.combo.currentTextChanged.connect(
    lambda text: (
        self.state.update({"algorithm": text}))

        )

    
       
      
        
        # TableChartLayout -- > Contains Table / Chart
        TableChartLayout = QHBoxLayout()
        from table_widget import createTable
        self.table = createTable(self)

        Chart = QFrame()
        Chart.setStyleSheet("background-color: blue;")

        TableChartLayout.addWidget(self.table)
        TableChartLayout.addWidget(Chart)
        TableChartLayout.setStretch(0, 1)
        TableChartLayout.setStretch(1, 1)
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
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_simulation)
        # self.add_btn.clicked.connect(self.start)
        ButtonsContainer = QHBoxLayout()
        ButtonsContainer.addWidget(self.add_btn)
        ButtonsContainer.addWidget(self.Start_Btn)
        ButtonsContainer.addWidget(self.combo)

        # Add to layout
        # mainlayout.addWidget(self.table)
        mainlayout.addLayout(ButtonsContainer)

        central_widget.setLayout(mainlayout)
        self.setCentralWidget(central_widget)
    def start(self):
        self.timer.start(1000)  # 1 second
    
   
    

# Run App

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()
    sys.exit(app.exec())
    

    