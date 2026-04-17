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
from gant_wiget import *
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QMessageBox
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
            QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
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
    def __init__(self,algorithm, parent=None):
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
        if parent and parent.timer.isActive():
            self.arrival.hide()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

class QuantumDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Time Quantum")

        layout = QFormLayout()

        self.quantum_input = QLineEdit()
        layout.addRow("Quantum:", self.quantum_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

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
            "quantum" : None  ,
            "counter" : 0 ,
            "processes" : self.processes ,
            "timeline" : []

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

        self.running_label = QLabel("Running: None")
        self.mode_combo = QComboBox()
        self.mode_combo.setPlaceholderText("Select Mode")
        self.mode_combo.addItems(["Dynamic", "Static"])
        mainlayout.addWidget(self.mode_combo)
    

        self.time_label = QLabel(f'time : 0')

        mainlayout.addWidget(self.time_label)


        mainlayout.addWidget(self.running_label)



        # TableChartLayout -- > Contains Table / Chart
        TableChartLayout = QHBoxLayout()
        self.table = createTable(self)
        TableChartLayout.addWidget(self.table,0)


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.gantt_widget = GanttWidget()
        self.scroll.setWidget(self.gantt_widget)

        TableChartLayout.addWidget(self.scroll,1)

        ## Setting Table/Chart Ratios
        self.table.setFixedWidth(500)  # adjust (450–600 based on your UI)
        self.scroll.setWidgetResizable(True)
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
        ## Start Button Event 
        self.Start_Btn.clicked.connect(self.safe_start)
        ButtonsContainer.addWidget(self.Start_Btn)


        # combo box for selecting scheduling algorithm
        self.combo = QComboBox()
        self.combo.setPlaceholderText("Select Algorithm")
        self.combo.addItems([
            "FCFS",
            "Priority Preemptive",
            "Priority Non-Preemptive",
            "Round Robin",
            "SJF Preemptive",
            "SJF Non-Preemptive"
        ])
        self.combo.setCurrentIndex(-1)
        self.combo.currentTextChanged.connect(self.change_algorithm)
        ButtonsContainer.addWidget(self.combo)

        # Add to layout
        mainlayout.addLayout(ButtonsContainer)

        central_widget.setLayout(mainlayout)
        self.setCentralWidget(central_widget)

    # =============== Core Functions ====================
    def safe_start(self):
        if self.timer.isActive():
            return
        if self.Start_Btn.text()=="Reset":
            self.resetSimulation()
            return

        if not self.processes:
            QMessageBox.warning(self, "Error", "Please add at least one process.")
            return

        if self.state["algorithm"] is None:
            QMessageBox.warning(self, "Error", "Please select an algorithm first.")
            return
        if self.state["algorithm"] == "Round Robin" and not self.state["quantum"]:
            QMessageBox.warning(self, "Error", "Please set time quantum.")
            return

        # start simulation
        mode = self.mode_combo.currentText()

        if not mode:
            QMessageBox.warning(self, "Error", "Please select a mode first.")
            return

        # disable controls
        self.add_btn.setEnabled(True)
        self.combo.setEnabled(False)
        self.mode_combo.setEnabled(False)
        self.Start_Btn.setEnabled(False)
        self.Start_Btn.setText("Running")

        if mode == "Dynamic":
            self.timer.start(1000)

        else:  # STATIC MODE

            while True:
                # check if done BEFORE stepping
                done = all(p["remaining"] == 0 for p in self.processes)

                if done:
                    self.update_simulation()  # ✅ show popup ONLY
                    break

                self.step()  # ✅ run ONE step (NOT update_simulation)



    

    def add_process(self):
        dialog = AddProcessDialog(self.state["algorithm"],self)

        if dialog.exec():
            ## --> Get Dialoge entries
            # if running → auto arrival
            if self.timer.isActive() :
                arrival = self.state["time"]
            else:
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


    def change_algorithm(self, text):
        self.state["algorithm"] = text

        if "Priority" in text:
            self.table.setColumnHidden(4, False)
        else:
            self.table.setColumnHidden(4, True)

        if text == "Round Robin":
            dialog = QuantumDialog()
            if dialog.exec():
                try:
                    q = int(dialog.quantum_input.text())
                    if q <= 0:
                        raise ValueError
                    self.state["quantum"] = q
                except:
                    QMessageBox.warning(self, "Error", "Invalid quantum value")
                    self.state["algorithm"] = None
                    self.combo.setCurrentIndex(-1)

    def step(self):
        run_step(self.state)

        # 2. update labels
        self.time_label.setText("Time: " + str(max(0, self.state["time"] - 1)))

        current_id = None
        if self.state["current"]:
            current_id = self.state["current"]["id"]
            self.running_label.setText("Running: " + current_id)
        else:
            self.running_label.setText("Running: None")

        for row, p in enumerate(self.processes):

            # update remaining
            item = self.table.item(row, 3)
            if item:
                item.setText(str(p["remaining"]))

            pid_item = self.table.item(row, 0)

            if not pid_item:
                continue

            # color logic
            if p["remaining"] == 0:
                pid_item.setBackground(QColor("#bdc3c7"))  # gray

            elif p["id"] == current_id:
                pid_item.setBackground(QColor(46, 204, 113, 150))  # green

            else:
                pid_item.setBackground(QColor(0, 0, 0, 0))  # reset

        self.gantt_widget.set_data(self.state["timeline"])

    def update_simulation(self):
        done = True
        for p in self.processes:
            if p["remaining"] == 0 : continue
            else:
                done = False
                break

        if done  :
            total_wt = 0
            total_tat = 0

            for p in self.processes:
                ct = p.get("completion", 0)
                tat = ct - p["arrival"]
                wt = tat - p["burst"]

                total_wt += wt
                total_tat += tat

            avg_wt = total_wt / len(self.processes)
            avg_tat = total_tat / len(self.processes)
            msg = QMessageBox(self)
            msg.setWindowTitle("Simulation Results")
            msg.setText(
                f"Average Waiting Time: {avg_wt:.2f}\n"
                f"Average Turnaround Time: {avg_tat:.2f}"
            )
            msg.exec()
            if self.timer.isActive():
                self.timer.stop()
                

            print("Simulation Finished: All processes completed.")
            self.add_btn.setEnabled(False)
            self.Start_Btn.setText("Reset")
            self.Start_Btn.setEnabled(True)
            self.running_label.setText("Finished")
            return 
        self.step()
        for row, p in enumerate(self.processes):
            new_value = str(p["remaining"]) 
            self.table.setItem(row, 3, QTableWidgetItem(new_value))



    def resetSimulation(self):
       while self.table.rowCount() > 0:
            self.table.removeRow(0)
       self.processes.clear()
       self.state["time"]=0
       self.state["timeline"].clear()
       self.gantt_widget.set_data([])
       self.time_label.setText("Time: " + str(self.state["time"]))
       self.combo.setCurrentIndex(-1)
       self.mode_combo.setCurrentIndex(-1)
       self.running_label.setText("Running: None")
       self.add_btn.setEnabled(True)
       self.Start_Btn.setText("Start")
       self.combo.setEnabled(True)
       self.mode_combo.setEnabled(True)
       self.Start_Btn.setEnabled(True)





# Run App

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()
    sys.exit(app.exec())
    

  


        

