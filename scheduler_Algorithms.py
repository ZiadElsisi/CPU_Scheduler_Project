import time
def sort_key(process):
    return (process["priority"], process["arrival"])  # Note: add priority to the process dictionary

# Priority None Preemptive ----
def priority_Nonpreemptive(state):
    if state["current"] is not None:
        return state["current"]

    if not state["queue"]:  # If there are no processes in the ready queue, we can't run anything
        return None

    state["queue"].sort(key=sort_key)

    return state["queue"][0]


# Priority Preemptive ----

def priority_preemptive(state):
    if not state["queue"] and not state["current"]:
        return None

    candidates = state["queue"][:]
    if state["current"]:
        candidates.append(state["current"])

    return min(candidates, key=sort_key)

# Round Ronin Preemptive ----


def round_robin(state):
    if state["current"]:
        return state["current"]
    if not state["queue"]:
        return None
    return state["queue"][0]



# Shortest Job First Preemptive ----


def sjf_Preemptive(state):
    if not state["queue"] and not state["current"]:
        return None

    candidates = state["queue"][:]
    if state["current"]:
        candidates.append(state["current"])

    return min(candidates, key=lambda p: p["remaining"])


#  First Come First Surved  ----

def fcfs(state):
    if state["current"]:
        return state["current"]
    if not state["queue"]:
        return None
    return state["queue"][0]