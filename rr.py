state = {
    "current": None, 
    "queue": [],        
    "time": 0,
    "quantum": 0,
    "counter": 0
}

def round_robin(state):
    
    if state["quantum"] <= 0:
        raise ValueError("Quantum time must be > 0")

    if state["current"] is None and len(state["queue"]) > 0:
        state["current"] = state["queue"].pop(0)
        state["counter"] = 0
    
    if state["current"] is None:
        return state
     
    state["counter"] += 1
    
    
    
    if state["counter"] == state["quantum"] : 
            state["queue"].append(state["current"])
            state["counter"] = 0
            state["current"] = None
    return state
 