# SJF vs Priority Comparison Project

## Evaluation Rubric Summary

## Criterion                         Marks   Specific focus                                 Notes for evaluator

- Interface and usability (15) -Clean layout, easy data entry, easy comparison workflow, readable output.

- Input handling and validation (10) -Reject invalid numeric input, duplicate IDs, missing values, invalid quantum/priority values.

- Algorithm A correctness (15) -Correct process selection, arrival handling, ties, completion behavior, and algorithm-specific rules.

- Algorithm B correctness (15) -Correct process selection, arrival handling, ties, completion behavior, and algorithm-specific rules.

- Gantt charts and execution visualization (10) -Separate readable Gantt chart for each algorithm with correct time markers and execution order.

- Metrics calculation (10) -Correct WT, TAT, RT for each process and correct averages, consistent with charts.

- Comparison quality and fairness (10) -Same workload, correct comparison tables, valid analysis of trade-offs and recommendation.

- Required test scenarios (5) -Normal case, behavior-revealing case, and invalid-input validation case are all included.

- Report and technical explanation (5) -Clear write-up, screenshots, assumptions, limitations, and technically correct conclusions.

- Viva / team understanding (5) -Team members can explain both algorithms, outputs, metrics, and design decisions.

## Variant-Specific Checklist

Use this page during review. A project should not be considered complete until all variant- specific items have been checked.


Check   Checklist Item
□       SJF selection is based on the shortest available burst time.
□       Priority rule is stated clearly and applied consistently.
□       At least one workload shows conflict between short burst time and high priority.
□       Comparison tables use the same dataset for both algorithms.
□       Conclusion explains efficiency versus urgency trade-off.

## Project-Specific Notes for Students

Project- Specific Notes for Students- Use the same workload in both algorithms.- Assume preemptive SJF and Priority Scheduling.- Discuss efficiency versus urgency when short jobs and high- priority jobs conflict.- Explain whether either policy causes unfair delay.
