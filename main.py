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
from table_widget import createTable
from models import create_process
from CoreEngine import run_step

## Style ::
Button_style = """
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
            """
Header_style = """
            background-color: #111827;
            color: #E5E7EB;
            font-size: 26px;
            font-weight: bold;
            padding: 20px;
            border-radius: 10px;
            """
# Main Window
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ## Configuration
        self.state = {
            "queue": [],
            "current": None,
            "time": 0,
            "algorithm": None
        }
        self.processes=[]
        self.setWindowTitle("CPU Scheduler")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.resize(1100, 600)
        self.setMinimumSize(1100,600)

        # ==================== UI ====================
        central_widget = QWidget()
        # Main Layout--> Contains Table / chats And Buttons
        mainlayout = QVBoxLayout()
        Header = QLabel("WELCOME TO CPU SCHEDULER")
        Header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Header.setStyleSheet(Header_style)
        mainlayout.addWidget(Header)
    
        # TableChartLayout -- > Contains Table / Chart
        TableChartLayout = QHBoxLayout()
        from table_widget import createTable
        self.table = createTable(self)
        TableChartLayout.addWidget(self.table)

        Chart = QFrame()
        Chart.setStyleSheet("background-color: blue;")
        TableChartLayout.addWidget(Chart)


        TableChartLayout.setStretch(0, 1)
        TableChartLayout.setStretch(1, 1)
        mainlayout.addLayout(TableChartLayout)

    

        ButtonsContainer = QHBoxLayout() ##--> Container For Buttons
        # Add Buttons
        self.add_btn = QPushButton("Add Process")
        self.add_btn.setStyleSheet(Button_style)
        ButtonsContainer.addWidget(self.add_btn)

        ## Add Button Event
        self.add_btn.clicked.connect(self.add_process)

        # Start Button
        self.Start_Btn = QPushButton("Start")
        self.Start_Btn.setStyleSheet(Button_style)
        ## Start Button Event
        self.Start_Btn.clicked.connect(self.start)
        ButtonsContainer.addWidget(self.Start_Btn)


        # combo box for selecting scheduling algorithm
        self.combo = QComboBox()
        self.combo.setPlaceholderText("Select Algorithm")
        self.combo.addItems(
            ["Priority Preemptive", "Priority Non-Preemptive", "Round Robin", "SJF Preemptive", "SJF Non-Preemptive"])
        self.combo.setCurrentIndex(-1)
        self.combo.currentTextChanged.connect(lambda text: (self.state.update(
            {"algorithm": text})))
        ButtonsContainer.addWidget(self.combo)

        # Add to layout
        mainlayout.addLayout(ButtonsContainer)

        central_widget.setLayout(mainlayout)
        self.setCentralWidget(central_widget)

    def start(self):
        self.timer.start(1000)# 1 second
        print("Hello")
     
    def add_process(self):
         if not self.processes:
            nextLastId=1
         else:
            currentLastId=self.processes[-1]["id"]
            nextLastId=int(currentLastId[1:])+1
         p = create_process("P"+str(nextLastId), 0, 5)
         self.processes.append(p)
         row = self.table.rowCount()
         self.table.insertRow(row)
         self.table.setItem(row, 0, QTableWidgetItem(p["id"]))
         self.table.setItem(row, 1, QTableWidgetItem(str(p["arrival"])))
         self.table.setItem(row, 2, QTableWidgetItem(str(p["burst"])))
         self.table.setItem(row, 3, QTableWidgetItem(str(p["remaining"])))

    def update_simulation(self):
        if not self.state["queue"] and self.state["current"] is None:
            self.timer.stop()
            print("Simulation Finished: All processes completed.")
            return 
        run_step(self.state)
        for row, p in enumerate(self.processes):
            new_value = str(p["remaining"]) 
            self.table.setItem(row, 3, QTableWidgetItem(new_value))
   
    

# Run App

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()
    sys.exit(app.exec())
    

  


        

