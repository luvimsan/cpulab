def validate_input(pid, arrival, burst, priority, existing_ids):
    """Safely validates user input before adding a process."""

    # 1. Check for missing fields
    if not pid or not arrival or not burst or not priority:
        return False, "All fields (ID, Arrival, Burst, Priority) are required."

    # 2. Check for duplicate IDs
    if pid in existing_ids:
        return False, f"Duplicate Process ID: {pid}. Please use a unique ID."

    # 3. Check for non-numeric input
    try:
        arr = int(arrival)
        brt = int(burst)
        pri = int(priority)
    except ValueError:
        return False, "Arrival, Burst, and Priority must be integers."

    # 4. Check logical constraints
    if arr < 0:
        return False, "Arrival time cannot be negative."
    if brt <= 0:
        return False, "Burst time must be greater than zero."
    if pri < 0:
        return False, "Priority cannot be negative."

    # If all checks pass, return the cleaned dictionary
    clean_data = {"id": pid, "arrival": arr, "burst": brt, "priority": pri}
    return True, clean_data
