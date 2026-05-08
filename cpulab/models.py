class Scheduler:

    @staticmethod
    def calculate_metrics(process_metrics):
        if not process_metrics:
            return 0, 0, 0
        n = len(process_metrics)
        avg_wt = sum(p['wt'] for p in process_metrics) / n
        avg_tat = sum(p['tat'] for p in process_metrics) / n
        avg_rt = sum(p['rt'] for p in process_metrics) / n
        return round(avg_wt, 2), round(avg_tat, 2), round(avg_rt, 2)

    @staticmethod
    def run_srtf(processes):
        return Scheduler._simulate_preemptive(
            processes,
            key_func=lambda p: (p['remaining'], p['arrival'])
        )

    @staticmethod
    def run_priority(processes):
        return Scheduler._simulate_preemptive(
            processes,
            key_func=lambda p: (p['priority'], p['arrival'])
        )

    @staticmethod
    def _simulate_preemptive(processes, key_func):
        procs = []
        for p in processes:
            procs.append({
                'id': p['id'],
                'arrival': p['arrival'],
                'burst': p['burst'],
                'priority': p['priority'],
                'remaining': p['burst'],
                'first_cpu': -1,
                'ct': 0,
            })

        n = len(procs)
        completed = 0
        current_time = 0
        gantt = []

        while completed < n:
            # Collect all processes that have arrived and are not yet finished
            available = [
                p for p in procs
                if p['arrival'] <= current_time and p['remaining'] > 0
            ]

            if not available:
                # CPU is idle — jump to the next earliest arrival
                future = [p for p in procs if p['remaining'] > 0]
                if not future:
                    break
                next_time = min(p['arrival'] for p in future)
                gantt.append({'id': 'Idle', 'start': current_time, 'end': next_time})
                current_time = next_time
                continue

            # Select the best process according to the algorithm's key
            available.sort(key=key_func)
            selected = available[0]

            # Record first CPU access (used for Response Time)
            if selected['first_cpu'] == -1:
                selected['first_cpu'] = current_time

            # Determine how long to run before the next decision point:
            #   either a new process arrives, or the selected process completes.
            future_arrivals = [
                p['arrival'] for p in procs
                if p['arrival'] > current_time and p['remaining'] > 0
            ]
            next_arrival = min(future_arrivals) if future_arrivals else float('inf')
            run_until = min(current_time + selected['remaining'], next_arrival)

            # Execute the selected process for the computed duration
            elapsed = run_until - current_time
            selected['remaining'] -= elapsed

            gantt.append({'id': selected['id'], 'start': current_time, 'end': run_until})
            current_time = run_until

            if selected['remaining'] == 0:
                selected['ct'] = current_time
                completed += 1

        # Merge consecutive Gantt segments that belong to the same process
        merged_gantt = []
        for seg in gantt:
            if merged_gantt and merged_gantt[-1]['id'] == seg['id']:
                merged_gantt[-1]['end'] = seg['end']
            else:
                merged_gantt.append(dict(seg))

        # Build per-process metrics
        metrics = []
        for p in procs:
            ct = p['ct']
            tat = ct - p['arrival']
            wt = tat - p['burst']
            rt = p['first_cpu'] - p['arrival']
            metrics.append({
                'id': p['id'],
                'arrival': p['arrival'],
                'burst': p['burst'],
                'priority': p['priority'],
                'ct': ct,
                'tat': tat,
                'wt': wt,
                'rt': rt,
            })

        return merged_gantt, metrics
