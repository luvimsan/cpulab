class Scheduler:
    @staticmethod
    def calculate_metrics(schedule):
        """Calculates averages for the generated schedule."""
        if not schedule:
            return 0, 0, 0
        avg_wt = sum(p['wt'] for p in schedule) / len(schedule)
        avg_tat = sum(p['tat'] for p in schedule) / len(schedule)
        avg_rt = sum(p['rt'] for p in schedule) / len(schedule)
        return round(avg_wt, 2), round(avg_tat, 2), round(avg_rt, 2)

    @staticmethod
    def run_sjf(processes):
        """Non-preemptive Shortest Job First."""
        return Scheduler._simulate(processes, sort_key=lambda x: x['burst'])

    @staticmethod
    def run_priority(processes):
        """Non-preemptive Priority (Assuming Lower Number = Higher Priority)."""
        return Scheduler._simulate(processes, sort_key=lambda x: x['priority'])

    @staticmethod
    def _simulate(processes, sort_key):
        """Helper method to run non-preemptive algorithms."""
        ready_queue = []
        schedule = []
        current_time = 0

        # Create a copy and sort by arrival time
        remaining = sorted([dict(p) for p in processes], key=lambda x: x['arrival'])

        while remaining or ready_queue:
            # Move arrived processes to ready queue
            while remaining and remaining[0]['arrival'] <= current_time:
                ready_queue.append(remaining.pop(0))

            if ready_queue:
                # Sort ready queue based on the specific algorithm (Burst or Priority)
                ready_queue.sort(key=sort_key)
                p = ready_queue.pop(0)

                start_time = current_time
                end_time = start_time + p['burst']

                # Calculate metrics
                tat = end_time - p['arrival']
                wt = tat - p['burst']
                rt = start_time - p['arrival']

                p.update({'start': start_time, 'end': end_time, 'tat': tat, 'wt': wt, 'rt': rt})
                schedule.append(p)

                current_time = end_time
            else:
                # If CPU is idle, jump to the arrival of the next process
                current_time = remaining[0]['arrival']

        return schedule
