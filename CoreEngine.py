# File: scheduler_Algorithms.py

# This is our global state to keep track of everything in one place
from scheduler_Algorithms import round_robin , priority_Nonpreemptive, priority_preemptive , sjf_Preemptive , sjf_non_preemptive


def get_next_process(state):
    if not state["queue"]:
        return None

    if state["algorithm"] == "Priority Preemptive":
        return priority_preemptive(state)

    elif state["algorithm"] == "Priority Non-Preemptive":
        return priority_Nonpreemptive(state)

    elif state["algorithm"] == "":
        return round_robin(state)

    elif state["algorithm"] == "SJF Preemptive":
        return sjf_Preemptive(state)

    elif state["algorithm"] == "SJF Non-Preemptive":
        return sjf_non_preemptive(state)
    return None


def run_step(state):
    for p in state["processes"]:
        if p["arrival"] == state["time"]:
            if p not in state["queue"] and p != state["current"]:
                state["queue"].append(p)
    # ===== SELECT PROCESS =====
    selected = get_next_process(state)
    if selected is None:
        if state["current"] is None:
            if state["processes"] :
                state["time"] +=1
            return

        else:
            selected = state["current"]

    # ===== SWITCH (IMPORTANT FOR PREEMPTIVE) =====

    if state["current"] != selected:
            if state["current"]:
                state["queue"].append(state["current"])

            state["current"] = selected

            if selected in state["queue"]:
                state["queue"].remove(selected)

    current_p = state["current"]

    # 1. Move the clock forward by 1 second
    state["time"] = state["time"] + 1

    
    # 3. Reduce its remaining time by 1 
    if current_p["remaining"] > 0:
        current_p["remaining"] = current_p["remaining"] - 1

    # 4. Round Robin Logic

    if current_p["remaining"] == 0:
        state["current"] = None

        state["counter"] += 1

        if state["algorithm"] == "Round Robin":
            if state["counter"] == state["quantum"]:
                if state["current"] and state["current"]["remaining"] > 0:
                    state["queue"].append(state["current"])

                state["current"] = None
                state["counter"] = 0

        # print on console
    print(f"Time {state['time']}: Process {current_p['id']} is running. Left: {current_p['remaining']}")

# # ================== Testing ========
#
# if __name__ == "__main__":
#     # Example process
#     state = {
#         "queue": [],  # List of processes waiting
#         "current": None,  # The process the CPU is currently executing
#         "time": 0,  # The global counter clock { 1 s each time ]
#         "algorithm": None
#
#     }
#     test_p = {"id": "P1", "arrival": 0, "burst": 5, "remaining": 5}
#
#     state["current"] = test_p
#
#     # Simulate 5 seconds
#     for i in range(5):
#         run_step(state)