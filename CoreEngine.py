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
        return sjf_non_preemptive()




def run_step(state):

    # we need to check if there is a process or not at firdt
    if state["current"] is None:
        print(" Nothing to do.")
        return #we stop the function early so we don't try to subtract time from a non-existent process

    # 1. Move the clock forward by 1 second
    state["time"] = state["time"] + 1
    
    # 2. get the current process from the state
    current_p = state["current"]
    
    # 3. Reduce its remaining time by 1 
    if current_p["remaining"] > 0:
        current_p["remaining"] = current_p["remaining"] - 1

   #print on console      
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