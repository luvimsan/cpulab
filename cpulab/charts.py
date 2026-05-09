import tkinter as tk
from tkinter import ttk


class InputTable(ttk.Treeview):
    def __init__(self, master):
        cols = ("ID", "Arrival", "Burst", "Priority")
        super().__init__(master, columns=cols, show="headings", height=6)
        for col in cols:
            self.heading(col, text=col)
            self.column(col, width=100, anchor="center")


class MetricsTable(ttk.Treeview):
    def __init__(self, master):
        cols = ("ID", "Arrival", "Burst", "Priority", "CT", "WT", "TAT", "RT")
        super().__init__(master, columns=cols, show="headings", height=6)
        for col in cols:
            self.heading(col, text=col)
            self.column(col, width=65, anchor="center")

    def update_data(self, data):
        self.delete(*self.get_children())
        for row in data:
            self.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["arrival"],
                    row["burst"],
                    row["priority"],
                    row["ct"],
                    row["wt"],
                    row["tat"],
                    row["rt"],
                ),
            )


class GanttChart(tk.Canvas):
    PROCESS_COLORS = [
        "#6fa8dc",
        "#93c47d",
        "#e06666",
        "#f6b26b",
        "#8e7cc3",
        "#c27ba0",
        "#76a5af",
        "#d5a6bd",
    ]
    IDLE_COLOR = "#d9d9d9"

    def __init__(self, master, **kwargs):
        kwargs.setdefault("height", 130)
        kwargs.setdefault("bg", "white")
        super().__init__(master, **kwargs)

    def draw(self, gantt_segments, title):
        self.delete("all")
        self.create_text(400, 15, text=title, font=("Arial", 12, "bold"))

        if not gantt_segments:
            return

        total_time = max(seg["end"] for seg in gantt_segments)
        scale = 700 / max(total_time, 1)

        y, bar_h = 40, 40
        color_map = {}
        c_idx = 0

        for seg in gantt_segments:
            pid = seg["id"]
            start_x = 50 + seg["start"] * scale
            width = (seg["end"] - seg["start"]) * scale

            if pid == "Idle":
                fill = self.IDLE_COLOR
            else:
                if pid not in color_map:
                    color_map[pid] = self.PROCESS_COLORS[
                        c_idx % len(self.PROCESS_COLORS)
                    ]
                    c_idx += 1
                fill = color_map[pid]

            self.create_rectangle(
                start_x, y, start_x + width, y + bar_h, fill=fill, outline="black"
            )
            self.create_text(
                start_x + width / 2, y + bar_h / 2, text=pid, font=("Arial", 9)
            )
            self.create_text(
                start_x, y + bar_h + 15, text=str(int(seg["start"])), font=("Arial", 8)
            )

        last_end = max(seg["end"] for seg in gantt_segments)
        self.create_text(
            50 + last_end * scale,
            y + bar_h + 15,
            text=str(int(last_end)),
            font=("Arial", 8),
        )
