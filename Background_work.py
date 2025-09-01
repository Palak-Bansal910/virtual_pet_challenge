from datetime import datetime
from database import update_pet, save_pet_action

def update_pet_status(pet: object, pet_id: int = 1):
    """
    Apply background logic to the pet:
    - Natural decay (hunger ↑, happiness ↓)
    - Neglect system (health decreases if ignored)
    - Update DB after changes
    """

    # Parse last updated time
    if isinstance(pet.get_status()["last_updated"], str):
        last_updated = datetime.fromisoformat(pet.get_status()["last_updated"])
    else:
        last_updated = datetime.now()

    now = datetime.now()
    elapsed_hours = (now - last_updated).total_seconds() / 3600.0

    if elapsed_hours > 0:
        state = pet.get_status()

        # Natural decay
        state["hunger"] = min(100.0, state["hunger"] + 5 * elapsed_hours)      # gets hungrier
        state["happiness"] = max(0.0, state["happiness"] - 3 * elapsed_hours)  # gets sadder

        # Optional: Energy decay
        state["energy"] = max(0.0, state["energy"] - 2 * elapsed_hours)

        # Neglect system: every 6 hours of no interaction → penalty
        neglect_intervals = int(elapsed_hours // 6)
        if neglect_intervals > 0:
            state["happiness"] = max(0.0, state["happiness"] - 10 * neglect_intervals)

        # Update last_updated
        state["last_updated"] = now.isoformat()

        # Save changes to DB
        update_pet(pet_id, state)
        save_pet_action(pet_id, "background_update", f"Auto-update after {elapsed_hours:.2f} hrs")

        return state

    # If no update needed, return current status
    return pet.get_status()
