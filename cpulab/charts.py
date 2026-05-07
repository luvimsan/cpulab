# src/cpulab/charts.py
import tkinter as tk
from tkinter import ttk

class MetricsTable(ttk.Treeview):
    def __init__(self, master):
        cols = ("ID", "Arrival", "Burst", "Priority", "WT", "TAT", "RT")
        super().__init__(master, columns=cols, show="headings", height=6)
        for col in cols:
            self.heading(col, text=col)
            self.column(col, width=70, anchor="center")

    def update_data(self, data):
        self.delete(*self.get_children()) # Clear old data
        for row in data:
            self.insert("", "end", values=(
                row['id'], row['arrival'], row['burst'],
                row['priority'], row['wt'], row['tat'], row['rt']
            ))

class GanttChart(tk.Canvas):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('height', 120)
        kwargs.setdefault('bg', 'white')
        super().__init__(master, **kwargs)
        self.colors = ["#add8e6", "#90ee90", "#ffb6c1", "#ffffe0", "#e6e6fa", "#ffdab9"]

    def draw(self, schedule, title):
        self.delete("all")
        self.create_text(400, 15, text=title, font=("Arial", 12, "bold"))

        if not schedule:
            return

        # Calculate dynamic scaling to fit the canvas width
        total_time = max([p['end'] for p in schedule])
        scale = 700 / max(total_time, 1) # Prevent divide by zero

        x, y, height = 50, 40, 40
        color_map = {}
        c_idx = 0

        for p in schedule:
            pid = p['id']
            if pid not in color_map:
                color_map[pid] = self.colors[c_idx % len(self.colors)]
                c_idx += 1

            width = (p['end'] - p['start']) * scale
            start_x = 50 + (p['start'] * scale)

            self.create_rectangle(start_x, y, start_x + width, y + height, fill=color_map[pid])
            self.create_text(start_x + width/2, y + height/2, text=pid)
            self.create_text(start_x, y + height + 15, text=str(p['start']))

        last_end = max([p['end'] for p in schedule])
        self.create_text(50 + (last_end * scale), y + height + 15, text=str(last_end))
