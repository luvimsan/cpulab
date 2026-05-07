# src/cpulab/main.py
import tkinter as tk
from tkinter import ttk, messagebox

# Import from our custom modules
from cpulab.validator import validate_input
from cpulab.models import Scheduler
from cpulab.charts import MetricsTable, GanttChart

class CPULabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Lab - SJF vs Priority")
        self.root.geometry("850x650")

        self.processes = [] # Stores our validated process dicts

        self.setup_ui()

    def setup_ui(self):
        # Top Input Frame
        input_frame = tk.LabelFrame(self.root, text="Input Panel")
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Process ID:").grid(row=0, column=0, padx=5)
        self.entry_id = tk.Entry(input_frame, width=10)
        self.entry_id.grid(row=0, column=1)

        tk.Label(input_frame, text="Arrival:").grid(row=0, column=2, padx=5)
        self.entry_arr = tk.Entry(input_frame, width=10)
        self.entry_arr.grid(row=0, column=3)

        tk.Label(input_frame, text="Burst:").grid(row=0, column=4, padx=5)
        self.entry_brt = tk.Entry(input_frame, width=10)
        self.entry_brt.grid(row=0, column=5)

        tk.Label(input_frame, text="Priority (Lower=Higher):").grid(row=0, column=6, padx=5)
        self.entry_pri = tk.Entry(input_frame, width=10)
        self.entry_pri.grid(row=0, column=7)

        tk.Button(input_frame, text="Add Process", command=self.add_process).grid(row=0, column=8, padx=10, pady=5)

        # Process List Table
        self.list_table = MetricsTable(self.root)
        self.list_table.pack(fill="x", padx=10, pady=5)

        # Run Button
        tk.Button(self.root, text="Run Simulation & Compare", bg="lightgreen", command=self.run_simulation).pack(pady=5)

        # Tabs for Results
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 1: SJF Results
        self.tab_sjf = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sjf, text="SJF Results")
        self.sjf_chart = GanttChart(self.tab_sjf)
        self.sjf_chart.pack(fill="x")
        self.sjf_table = MetricsTable(self.tab_sjf)
        self.sjf_table.pack(fill="x", pady=10)

        # Tab 2: Priority Results
        self.tab_pri = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pri, text="Priority Results")
        self.pri_chart = GanttChart(self.tab_pri)
        self.pri_chart.pack(fill="x")
        self.pri_table = MetricsTable(self.tab_pri)
        self.pri_table.pack(fill="x", pady=10)

        # Tab 3: Conclusion
        self.tab_conc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_conc, text="Comparison & Conclusion")
        self.text_conc = tk.Text(self.tab_conc, height=15, wrap="word", font=("Arial", 11))
        self.text_conc.pack(fill="both", expand=True, padx=10, pady=10)

    def add_process(self):
        pid = self.entry_id.get()
        existing_ids = [p['id'] for p in self.processes]

        is_valid, result = validate_input(
            pid, self.entry_arr.get(), self.entry_brt.get(), self.entry_pri.get(), existing_ids
        )

        if not is_valid:
            messagebox.showerror("Validation Error", result)
            return

        self.processes.append(result)
        self.list_table.insert("", "end", values=(result['id'], result['arrival'], result['burst'], result['priority'], "-", "-", "-"))

        # Clear inputs
        for entry in (self.entry_id, self.entry_arr, self.entry_brt, self.entry_pri):
            entry.delete(0, 'end')

    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add at least one process.")
            return

        # 1. Run Algorithms
        sjf_res = Scheduler.run_sjf(self.processes)
        pri_res = Scheduler.run_priority(self.processes)

        # 2. Update Charts & Tables
        self.sjf_chart.draw(sjf_res, "SJF Gantt Chart")
        self.sjf_table.update_data(sjf_res)

        self.pri_chart.draw(pri_res, "Priority Gantt Chart")
        self.pri_table.update_data(pri_res)

        # 3. Calculate Averages & Generate Conclusion
        s_wt, s_tat, s_rt = Scheduler.calculate_metrics(sjf_res)
        p_wt, p_tat, p_rt = Scheduler.calculate_metrics(pri_res)

        self.generate_conclusion(s_wt, s_tat, p_wt, p_tat)

        # Switch to SJF tab automatically
        self.notebook.select(self.tab_sjf)

    def generate_conclusion(self, s_wt, s_tat, p_wt, p_tat):
        self.text_conc.delete("1.0", "end")

        winner = "SJF" if s_wt < p_wt else ("Priority" if p_wt < s_wt else "Tie")

        conclusion = f"""COMPARISON SUMMARY:
----------------------------------------
SJF Averages      -> WT: {s_wt} | TAT: {s_tat}
Priority Averages -> WT: {p_wt} | TAT: {p_tat}

FINAL CONCLUSION:
----------------------------------------
Based on the tested workload, {winner} performed better in terms of Average Waiting Time.

- Efficiency vs Urgency: SJF optimizes overall system efficiency by clearing short jobs quickly, which lowers the average Wait Time. However, Priority scheduling ensures that urgent (high priority) jobs are serviced first, even if they are long.
- Fairness & Starvation: If you used a workload with a long, high-priority job, you likely noticed SJF delayed it significantly. Conversely, Priority scheduling might starve short, low-priority jobs.
"""
        self.text_conc.insert("end", conclusion)

def main():
    root = tk.Tk()
    app = CPULabApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
