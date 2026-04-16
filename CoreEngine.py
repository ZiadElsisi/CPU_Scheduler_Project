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

    elif state["algorithm"] == "Round Robin":
        return round_robin(state)

    elif state["algorithm"] == "SJF Preemptive":
        return sjf_Preemptive(state)

    elif state["algorithm"] == "SJF Non-Preemptive":
        return sjf_non_preemptive(state)

    return None


def run_step(state):
    # ===== SELECT PROCESS =====
    selected = get_next_process(state)
    if selected is None:
        if state["current"] is None:
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
    

    #when i test the code infinite loop occurs 
    #add this codition to prevent infinite loop
    if current_p["remaining"] <= 0:
        state["current"] = None

   #print on console      
    print(f"Time {state['time']}: Process {current_p['id']} is running. Left: {current_p['remaining']}")

    if current_p["remaining"] == 0:
        state["current"] = None
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