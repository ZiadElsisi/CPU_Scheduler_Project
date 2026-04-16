from PyQt6.QtWidgets import QApplication,QMainWindow,QTableWidget,QTableWidgetItem,QVBoxLayout,QWidget,QHeaderView
def createTable(self):
        table=QTableWidget(0,5)  #assume the user choose to first enter 3 processes it will later be replaced by n process where n is input from user
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) #disable editting the table
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection) #disable selecting cells
        table.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch
        ) #resize the cells width
        table.verticalHeader().setDefaultSectionSize(30) #resize the cells height
        table.verticalHeader().setVisible(False) #hide the indexing of rows
        table.setAlternatingRowColors(True) #make the cells color alternating
        table.setStyleSheet("""
        *{
             color:black;
            font-weight: 550;
            }
            QTableWidget {
            background-color: white;
            font-size: 12px;
            border: none;
        }

            QTableWidget::item {
            padding: 5px;
        }

            QTableWidget::item:selected {
            background-color: #3498db;
            color: white;
        }

        QHeaderView::section {
        background-color: #3498db;
        color: white;
        padding: 6px;
        font-weight: bold;
        font-size:10px;
       border: 0.5px solid #2980b9;
        }

        QTableWidget {
        alternate-background-color: #f5f5f5;
        }
        QTableWidget::item:hover {
        background-color: #d6ecff;
        }

""")
        #creating the initial processes
        table.setHorizontalHeaderLabels(["PID","arrival","burst","remaining","Priority"])
        table.setColumnHidden(4, True) ## --> Hide Periority Initially
        return table