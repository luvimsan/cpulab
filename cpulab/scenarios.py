scenarios = [
    {
        "name": "Basic Case",
        "processes": [
            {"id": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"id": "P2", "arrival": 1, "burst": 3, "priority": 1},
            {"id": "P3", "arrival": 2, "burst": 4, "priority": 3},
        ],
        "quantum": 2
    },
    {
        "name": "Same Arrival Time",
        "processes": [
            {"id": "P1", "arrival": 0, "burst": 6, "priority": 3},
            {"id": "P2", "arrival": 0, "burst": 2, "priority": 1},
            {"id": "P3", "arrival": 0, "burst": 4, "priority": 2},
        ],
        "quantum": 2
    },
    {
        "name": "Different Burst Times",
        "processes": [
            {"id": "P1", "arrival": 0, "burst": 10, "priority": 2},
            {"id": "P2", "arrival": 1, "burst": 2, "priority": 1},
            {"id": "P3", "arrival": 2, "burst": 1, "priority": 3},
        ],
        "quantum": 2
    },
    {
        "name": "Priority vs Burst Conflict",
        "processes": [
            {"id": "P1", "arrival": 0, "burst": 8, "priority": 1},
            {"id": "P2", "arrival": 1, "burst": 2, "priority": 3},
            {"id": "P3", "arrival": 2, "burst": 3, "priority": 2},
        ],
        "quantum": 3
    }
]
