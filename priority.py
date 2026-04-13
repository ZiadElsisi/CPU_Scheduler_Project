def sort_key(process):
    return (process["priority"], process["arrival"]) #Note: add priority to the process dictionary


def priority_Nonpreemptive(state):
   
    if state["current"] is not None: # If there is a currently running process, we don't preempt it
        return state
    if not state["queue"]: # If there are no processes in the ready queue, we can't run anything
        return state
    
    state["queue"].sort(key=sort_key) 

    state["current"] = state["queue"].pop(0)
    
    return state



def priority_preemptive(state):

    if state["current"] is None and not state["queue"]:
        return state

    state["queue"].sort(key=sort_key)

    if state["current"] is None:
        state["current"] = state["queue"].pop(0)  # If there is no current process, we take the highest priority process from the queue

    elif state["queue"] and sort_key(state["queue"][0]) < sort_key(state["current"]): #compare between the priority of the current process with the highest priority process in the queue
        state["queue"].append(state["current"]) #if so, we put the current process back in the queue
        state["current"] = state["queue"].pop(0) #add the highest priority process from the queue to be the current process

    return state