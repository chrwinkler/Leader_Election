from node2 import Process
import time
import asyncio
import threading

def sleep(n):
   time.sleep(n)

processes = []

#node1 = Process(1,5001,processes)
t1 = threading.Thread(target=Process(1,5001,processes))

t1.start()

#node2 = Process(2,5002,processes)
t2 = threading.Thread(target=Process(2,5002,processes))
t2.start()


sleep(3)
t3 = threading.Thread(target=Process(3,5003,processes))
t3.start()
# node3 = Process(target=Process(3,5003,processes))








def simulate_bully_algorithm():
    processes = {
        1: {'port': 5001},
        2: {'port': 5002},
        3: {'port': 5003},
        4: {'port': 5004},
        5: {'port': 5005}
    }

    process_objects = {}

    # Create and start all processes
    #for pid, info in processes.items():
    #    process = Process(pid, info['port'], processes)
    #    
    #    process_objects[pid] = process
    processes = []
    node1 = Process(1,5001,processes)
    node2 = Process(2,5002,processes)
    # Simulate process 2 detecting a leader failure and initiating an election
    time.sleep(2)  # Give processes time to start up
    
    return
    


