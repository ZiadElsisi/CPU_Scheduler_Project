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
from table_widget import createTable

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

## 🔧 Add dialog class
class AddProcessDialog(QDialog ):
    def __init__(self,algorithm):
        super().__init__()
        self.setWindowTitle("Add Process")

        layout = QFormLayout()

        self.arrival = QLineEdit()
        self.burst = QLineEdit()
        self.priority = QLineEdit()

        layout.addRow("Arrival:", self.arrival)
        layout.addRow("Burst:", self.burst)

        if algorithm and "Priority" in algorithm:
            layout.addRow("Priority:", self.priority)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)
# Main Window
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ## Configuration
        self.processes=[]
        self.state = {
            "queue": [],
            "current": None,
            "time": 0,
            "algorithm": None ,
            "quantum" : 1  ,
            "counter" : 0 ,
            "processes" : self.processes ,

        }
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
    
       
        self.time_label = QLabel("Time: 0")

        mainlayout.addWidget(self.time_label)

        self.running_label = QLabel("Running: None")

        mainlayout.addWidget(self.running_label)
       
       
       
        # TableChartLayout -- > Contains Table / Chart
        TableChartLayout = QHBoxLayout()
        self.table = createTable(self)
        TableChartLayout.addWidget(self.table)

        Chart = QFrame()
        Chart.setStyleSheet("background-color: blue;")
        TableChartLayout.addWidget(Chart)

        ## Setting Table/Chart Ratios
        TableChartLayout.setStretch(0, 1)
        TableChartLayout.setStretch(1, 1)
        mainlayout.addLayout(TableChartLayout)

        ##--> Container For Buttons
        ButtonsContainer = QHBoxLayout()
        # Add Buttons
        self.add_btn = QPushButton("Add Process")
        self.add_btn.setStyleSheet(Button_style)
        ButtonsContainer.addWidget(self.add_btn)

        ## Add Button Event
        self.add_btn.clicked.connect(self.add_process)

        # Start Button
        self.Start_Btn = QPushButton("Start")
        self.Start_Btn.setStyleSheet(Button_style)
        ## Start Button Event --> Using Lambda
        self.Start_Btn.clicked.connect(lambda :self.timer.start(1000))
        ButtonsContainer.addWidget(self.Start_Btn)


        # combo box for selecting scheduling algorithm
        self.combo = QComboBox()
        self.combo.setPlaceholderText("Select Algorithm")
        self.combo.addItems(
            ["Priority Preemptive", "Priority Non-Preemptive", "Round Robin", "SJF Preemptive", "SJF Non-Preemptive"])
        self.combo.setCurrentIndex(-1)
        self.combo.currentTextChanged.connect(self.change_algorithm)
        ButtonsContainer.addWidget(self.combo)

        # Add to layout
        mainlayout.addLayout(ButtonsContainer)

        central_widget.setLayout(mainlayout)
        self.setCentralWidget(central_widget)

    # =============== Core Functions ====================

    def add_process(self):
        dialog = AddProcessDialog(self.state["algorithm"])

        if dialog.exec():
            ## --> Get Dialoge entries
            arrival = int(dialog.arrival.text())
            burst = int(dialog.burst.text())
            if dialog.priority.text() :
                priority = int(dialog.priority.text())
            else:
                priority = 0


            if not self.processes:
                nextLastId=1
            else:
                currentLastId=self.processes[-1]["id"]
                nextLastId=int(currentLastId[1:])+1
            p = create_process("P"+str(nextLastId), arrival, burst,priority)
            self.processes.append(p)
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(p["id"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(p["arrival"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(p["burst"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(p["remaining"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(p["priority"])))
            self.combo.setEnabled(False)

    def change_algorithm(self, text):
        self.state["algorithm"] = text

        if "Priority" in text:
            self.table.setColumnHidden(6, False)
        else:
            self.table.setColumnHidden(6, True)

    def update_simulation(self):
    
        run_step(self.state)
        done = True
        for p in self.processes:
            if p["remaining"] > 0:done = False 
            else:
                if p["finish"] == 0:
                    p["finish"] = self.state["time"]
                    p["turnaround"] = p["finish"] - p["arrival"]
                    p["waiting"] = p["turnaround"] - p["burst"]

        for row, p in enumerate(self.processes):
            self.table.setItem(row, 3, QTableWidgetItem(str(p["remaining"])))
            if p["finish"]> 0:
                self.table.setItem(row, 4, QTableWidgetItem(str(p["waiting"])))
                self.table.setItem(row, 5, QTableWidgetItem(str(p["turnaround"])))

        if done and self.state["current"] is None:
            self.timer.stop()
            print("Simulation Finished: All processes completed.")
            return 
        run_step(self.state)
        for row, p in enumerate(self.processes):
            new_value = str(p["remaining"]) 
            self.table.setItem(row, 3, QTableWidgetItem(new_value))
            
            self.time_label.setText(f"Time: {self.state['time']}")
            if self.state["current"]:
                self.running_label.setText(f"Running: {self.state['current']['id']}")
            else:
                self.running_label.setText("Running: None")

    

# Run App

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()
    sys.exit(app.exec())
    

  


        

