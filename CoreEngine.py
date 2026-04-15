# File: scheduler.py

# our global state to keep track of everything in one place
state = {
    "queue": [],      # List of processes waiting
    "current": None,   # The process the CPU is currently executing
    "time": 0          # The global counter clock { 1 s each time ]
}

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

   #print on console check the process 
    print(f"Time {state['time']}: Process {current_p['id']} is running. Left: {current_p['remaining']}")




# ================== Testing ========

if __name__ == "__main__":
    # Example process 
    test_p = {"id": "P1", "arrival": 0, "burst": 5, "remaining": 5}
    
    state["current"] = test_p
    
    # Simulate 5 seconds 
    for i in range(5):
        run_step(state)