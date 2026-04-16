from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter,QColor


def build_gantt(timeline):
    gantt = []

    if not timeline:
        return gantt

    current_id = timeline[0][1]
    start_time = timeline[0][0]

    for i in range(1, len(timeline)):
        time, pid = timeline[i]

        if pid != current_id:
            gantt.append({
                "id": current_id,
                "start": start_time,
                "end": time
            })

            current_id = pid
            start_time = time

    # close last block
    gantt.append({
        "id": current_id,
        "start": start_time,
        "end": timeline[-1][0] + 1
    })

    return gantt


class GanttWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timeline = []

    def set_data(self, timeline):
        self.timeline = timeline

        # calculate needed width
        if timeline:
            max_time = max(t for t, _ in timeline)
            width_per_time = 35
            total_width = max_time * width_per_time + 150

            self.setMinimumWidth(total_width)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # ---- CONFIG ----
        height = 35
        width_per_time = 35
        left_margin = 80

        # ---- SAFETY ----
        if not self.timeline:
            return

        # ---- GET UNIQUE PROCESSES ----
        processes = list({pid for _, pid in self.timeline})
        processes.sort()

        # ---- MAP PROCESS → Y POSITION ----
        y_map = {}
        for i, pid in enumerate(processes):
            y_map[pid] = 60 + i * 60

        # ---- COLORS ----
        colors = {
            "P1": QColor("#4FC3F7"),
            "P2": QColor("#81C784"),
            "P3": QColor("#FFB74D"),
            "P4": QColor("#BA68C8"),
        }

        # ---- GRID ----
        grid_color = QColor(200, 200, 200, 80)
        painter.setPen(grid_color)

        max_time = max([t for t, _ in self.timeline])

        # ---- VERTICAL GRID (every second) ----
        grid_color = QColor(255, 255, 255, 40)  # soft lines
        painter.setPen(grid_color)

        for t in range(max_time + 2):
            x = left_margin + t * width_per_time
            painter.drawLine(x, 40, x, self.height())




        # ---- TIME AXIS ----
        painter.setPen(QColor("white"))
        for t in range(max_time + 1):
            x = left_margin + t * width_per_time
            painter.drawText(x + 10, 30, str(t))

        # ---- PROCESS LABELS ----
        for pid, y in y_map.items():
            painter.drawText(10, y + 22, pid)

        # ---- DRAW BLOCKS ----
        gantt = build_gantt(self.timeline)

        for block in gantt:
            pid = block["id"]
            start = block["start"]
            end = block["end"]

            x = left_margin + (start - 1) * width_per_time
            y = y_map[pid]
            width = (end - start) * width_per_time  # 🔥 THIS MAKES IT CONNECTED

            painter.setBrush(colors.get(pid, QColor("gray")))
            painter.setPen(QColor("white"))

            painter.drawRect(x, y, width, height)

            # center text inside block
            painter.drawText(
                x, y, width, height,
                0x84,
                pid
            )