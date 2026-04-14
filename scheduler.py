import time
def round_robin(state):
    queue = state["queue"]
    
    if len(queue) == 0:
      print("The queue is empty!")
      return state
    
    if state['quantum']>0 :
    
        current_process = queue[0]
        print(f"[CPU] Executing: {current_process}")

        # increase counter
        state["counter"] += 1

        #if counter == quantum: move process to end & reset counter
        if state["counter"] == state["quantum"]:
            print(f" Quantum {state['quantum']} reached. Switching processes.....")
            rotated_process = queue.pop(0)
            queue.append(rotated_process)
            state["counter"] = 0
    
    return state


def scheduling_info(state):
    print("------------------------------------")
    print(f"Starting Scheduler...")
    print(f"Quantum={state['quantum']} | Tasks={state['queue']}")
    print("------------------------------------")
    

def run_simulation():
    state_1 = {
        "queue": ["Task_1", "Task_2", "Task_3"],
        "quantum": 2, 
        "counter": 0
    }
    scheduling_info(state_1)
  
    for cycle in range(1, 11):
        print(f"Cycle {cycle}: ", end="")
        state = round_robin(state_1)
        time.sleep(0.5)

    state_2 = {
        "queue": ["Task_4", "Task_5", "Task_6"],
        "quantum": 1, 
        "counter": 0
    }
    
    scheduling_info(state_2)

    for cycle in range(1, 6):
        print(f"Cycle {cycle}: ", end="")
        state_2 = round_robin(state_2)
        time.sleep(0.5)


if __name__ == "__main__":
    run_simulation()