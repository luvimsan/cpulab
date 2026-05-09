import tkinter as tk
from tkinter import ttk, messagebox

from cpulab.validator import validate_input
from cpulab.models import Scheduler
from cpulab.charts import MetricsTable, InputTable, GanttChart


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Lab — SJF vs Priority")
        self.root.geometry("1300x700")
        self.root.minsize(850, 650)

        self.processes = []
        self.setup_ui()

    def setup_ui(self):
        input_frame = tk.LabelFrame(self.root, text="Input Panel")
        input_frame.pack(fill="x", padx=10, pady=8)

        tk.Label(input_frame, text="Process ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(input_frame, width=10)
        self.entry_id.grid(row=0, column=1)

        tk.Label(input_frame, text="Arrival:").grid(row=0, column=2, padx=5)
        self.entry_arr = tk.Entry(input_frame, width=10)
        self.entry_arr.grid(row=0, column=3)

        tk.Label(input_frame, text="Burst:").grid(row=0, column=4, padx=5)
        self.entry_brt = tk.Entry(input_frame, width=10)
        self.entry_brt.grid(row=0, column=5)

        tk.Label(input_frame, text="Priority (Lower=Higher):").grid(
            row=0, column=6, padx=5
        )
        self.entry_pri = tk.Entry(input_frame, width=10)
        self.entry_pri.grid(row=0, column=7)

        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=0, column=8, padx=10)

        tk.Button(
            button_frame, text="Add Process", command=self.add_process, bg="#e1f5fe"
        ).pack(side="left", padx=2)
        tk.Button(
            button_frame,
            text="Remove Selected",
            command=self.remove_selected,
            bg="#ffebee",
        ).pack(side="left", padx=2)
        tk.Button(
            button_frame,
            text="Restart All",
            command=self.restart_simulation,
            bg="#f5f5f5",
        ).pack(side="left", padx=2)
        self.tc = ttk.Combobox(
            button_frame,
            values=[
                "Basic Mixed Workload",
                "Conflict between Burst time and Priority",
                "Starvation / Fairness",
            ],
            width=40,
            state="readonly",
        )
        self.tc.set("Select a case scenario")
        self.tc.pack(side="left", padx=2)
        self.tc.bind("<<ComboboxSelected>>", self.test_scenarios)

        self.list_table = InputTable(self.root)
        self.list_table.pack(fill="x", padx=10, pady=5)

        tk.Button(
            self.root,
            text="Run Simulation & Compare",
            bg="lightgreen",
            command=self.run_simulation,
        ).pack(pady=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab_sjf = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sjf, text="SJF Results")
        self.sjf_chart = GanttChart(self.tab_sjf)
        self.sjf_chart.pack(fill="x")
        self.sjf_table = MetricsTable(self.tab_sjf)
        self.sjf_table.pack(fill="x", pady=10)

        self.tab_pri = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pri, text="Priority Results")
        self.pri_chart = GanttChart(self.tab_pri)
        self.pri_chart.pack(fill="x")
        self.pri_table = MetricsTable(self.tab_pri)
        self.pri_table.pack(fill="x", pady=10)

        self.tab_conc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_conc, text="Comparison & Conclusion")
        self.text_conc = tk.Text(
            self.tab_conc, height=15, wrap="word", font=("Arial", 11)
        )
        self.text_conc.pack(fill="both", expand=True, padx=10, pady=10)

    def add_process(self):
        pid = self.entry_id.get().strip()
        existing_ids = [p["id"] for p in self.processes]

        is_valid, result = validate_input(
            pid,
            self.entry_arr.get().strip(),
            self.entry_brt.get().strip(),
            self.entry_pri.get().strip(),
            existing_ids,
        )

        if not is_valid:
            messagebox.showerror("Validation Error", str(result))
            return

        self.processes.append(result)
        self.list_table.insert(
            "",
            "end",
            values=(
                result["id"],
                result["arrival"],
                result["burst"],
                result["priority"],
            ),
        )

        for entry in (self.entry_id, self.entry_arr, self.entry_brt, self.entry_pri):
            entry.delete(0, "end")
        self.entry_id.focus()

    def remove_selected(self):
        selected_item = self.list_table.selection()
        if not selected_item:
            messagebox.showwarning(
                "Selection Error", "Please select a process from the table to remove."
            )
            return

        for item in selected_item:
            values = self.list_table.item(item, "values")
            pid_to_remove = values[0]
            self.processes = [p for p in self.processes if p["id"] != pid_to_remove]
            self.list_table.delete(item)

    def restart_simulation(self):
        if not messagebox.askyesno(
            "Confirm Restart", "This will clear all processes and results. Continue?"
        ):
            return

        self.processes = []
        self.list_table.delete(*self.list_table.get_children())
        self.sjf_table.delete(*self.sjf_table.get_children())
        self.pri_table.delete(*self.pri_table.get_children())
        self.sjf_chart.delete("all")
        self.pri_chart.delete("all")
        self.text_conc.delete("1.0", "end")

        for entry in (self.entry_id, self.entry_arr, self.entry_brt, self.entry_pri):
            entry.delete(0, "end")
        self.entry_id.focus()

    def load_proccess_to_table(self, processes):
        self.list_table.delete(*self.list_table.get_children())
        self.processes = []
        self.processes.extend(processes)
        for p in processes:
            self.list_table.insert(
                "",
                "end",
                values=(
                    p["id"],
                    p["arrival"],
                    p["burst"],
                    p["priority"],
                ),
            )

    def test_scenarios(self, event=None):
        if self.tc.get() == "Basic Mixed Workload":
            basic_mixed = [
                {"id": "P1", "arrival": 0, "burst": 8, "priority": 3},
                {"id": "P2", "arrival": 1, "burst": 4, "priority": 1},
                {"id": "P3", "arrival": 2, "burst": 9, "priority": 4},
                {"id": "P4", "arrival": 3, "burst": 5, "priority": 2},
                {"id": "P5", "arrival": 4, "burst": 2, "priority": 5},
            ]
            self.processes.extend(basic_mixed)
            self.load_proccess_to_table(basic_mixed)
        elif self.tc.get() == "Conflict between Burst time and Priority":
            conflict_case = [
                {"id": "P1", "arrival": 0, "burst": 2, "priority": 5},
                {"id": "P2", "arrival": 0, "burst": 10, "priority": 1},
                {"id": "P3", "arrival": 1, "burst": 3, "priority": 4},
                {"id": "P4", "arrival": 2, "burst": 1, "priority": 3},
            ]
            self.processes.extend(conflict_case)
            self.load_proccess_to_table(conflict_case)
        elif self.tc.get() == "Starvation / Fairness":
            starvation_case = [
                {"id": "P1", "arrival": 0, "burst": 4, "priority": 3},
                {"id": "P2", "arrival": 1, "burst": 2, "priority": 3},
                {"id": "P3", "arrival": 2, "burst": 1, "priority": 3},
                {"id": "P4", "arrival": 0, "burst": 15, "priority": 5},
                {"id": "P5", "arrival": 3, "burst": 1, "priority": 5},
            ]
            self.processes.extend(starvation_case)
            self.load_proccess_to_table(starvation_case)

    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add at least one process.")
            return

        sjf_gantt, sjf_metrics = Scheduler.run_sjf(self.processes)
        pri_gantt, pri_metrics = Scheduler.run_priority(self.processes)

        self.sjf_chart.draw(sjf_gantt, "SJF Gantt Chart")
        self.sjf_table.update_data(sjf_metrics)

        self.pri_chart.draw(pri_gantt, "Priority Gantt Chart")
        self.pri_table.update_data(pri_metrics)

        s_wt, s_tat, s_rt = Scheduler.calculate_metrics(sjf_metrics)
        p_wt, p_tat, p_rt = Scheduler.calculate_metrics(pri_metrics)

        self.generate_conclusion(
            s_wt, s_tat, s_rt, p_wt, p_tat, p_rt, sjf_metrics, pri_metrics
        )

        self.notebook.select(self.tab_sjf)

    def generate_conclusion(
        self, s_wt, s_tat, s_rt, p_wt, p_tat, p_rt, sjf_metrics, pri_metrics
    ):
        self.text_conc.delete("1.0", "end")

        def label(s_val, p_val):
            if s_val < p_val:
                return "SJF"
            elif p_val < s_val:
                return "Priority"
            return "Tie"

        wt_winner = label(s_wt, p_wt)
        tat_winner = label(s_tat, p_tat)
        rt_winner = label(s_rt, p_rt)

        max_wt_sjf = max(p["wt"] for p in sjf_metrics)
        max_wt_pri = max(p["wt"] for p in pri_metrics)
        fairer = label(max_wt_sjf, max_wt_pri)

        scores = {"SJF": 0, "Priority": 0}
        for w in (wt_winner, tat_winner, rt_winner):
            if w in scores:
                scores[w] += 1
        if scores["SJF"] > scores["Priority"]:
            recommendation = "SJF"
        elif scores["Priority"] > scores["SJF"]:
            recommendation = "Priority"
        else:
            recommendation = "neither (tied overall)"

        text = (
            "-----------------------------------------------\n"
            "              COMPARISON SUMMARY\n"
            "-----------------------------------------------\n"
            "\n"
            f"  Metric              SJF        Priority     Winner\n"
            f"  ------------------  ----------  ----------   ----------\n"
            f"  Avg Waiting Time    {s_wt:<10}  {p_wt:<10}   {wt_winner}\n"
            f"  Avg Turnaround      {s_tat:<10}  {p_tat:<10}   {tat_winner}\n"
            f"  Avg Response Time   {s_rt:<10}  {p_rt:<10}   {rt_winner}\n"
            f"  Max Waiting Time    {max_wt_sjf:<10}  {max_wt_pri:<10}   {fairer} (fairer)\n"
            "\n"
            "-----------------------------------------------\n"
            "              FINAL CONCLUSION\n"
            "-----------------------------------------------\n"
            "\n"
        )

        text += f"- Waiting Time:  {wt_winner} achieved a lower average waiting time "
        text += f"({s_wt} vs {p_wt}).\n"
        text += (
            f"- Turnaround:    {tat_winner} achieved a lower average turnaround time "
        )
        text += f"({s_tat} vs {p_tat}).\n"
        text += f"- Response Time: {rt_winner} gave processes CPU access sooner "
        text += f"({s_rt} vs {p_rt}).\n\n"

        text += f"- Fairness:      {fairer} was fairer - its worst-case wait was "
        text += f"{min(max_wt_sjf, max_wt_pri)} vs {max(max_wt_sjf, max_wt_pri)}.\n"

        if max_wt_sjf > 2 * s_wt or max_wt_pri > 2 * p_wt:
            text += "- Starvation Risk: A large gap between max and average WT "
            text += "suggests possible starvation for at least one process.\n"

        text += (
            f"\n- Recommendation: For this workload, {recommendation} "
            f"is the better choice overall.\n"
            f"  SJF minimises wait for short-burst jobs but may starve long ones.\n"
            f"  Priority favours urgent tasks but may delay low-priority work.\n"
        )

        self.text_conc.insert("end", text)
