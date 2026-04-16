def create_process(pid, arrival, burst):

    process = {
        "id": pid,
        "arrival": arrival,
        "burst": burst,
        "remaining": burst ,
        "finish":0,
        "turnaround":0,
        "waiting":0 
    }
    return process




# if __name__ == "__main__":
#
#   p1 = create_process("P1", 0, 5)
#   p2 = create_process("P2", 2, 8)
#   p3 = create_process("P3", 4, 3)
#
#   processes = [p1, p2, p3]
#
#   print("===== Created Processes =====")
#
#   for p in processes:
#         print(p)
