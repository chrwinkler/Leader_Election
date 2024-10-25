from node import Node
import asyncio
from message import Message
import time

"""
    This is the final test for the Original version of the project.
    we use it to check different scenarios and see the number of messages sent.
    scenarios: 10, 20, 40, 60, 80, 100, 120 nodes.
    Results: 100, 400, 1600, 3600, 6400, 10000, 14400 messages sent.
"""

async def setup_nodes(i):
    nodes = []
    nr_msg = 0
    sPort = 5000
    # Create nodes with unique ports
    objs = [Node(n, nodes, nr_msg, sPort+n) for n in range(i)]
    # Start servers for all nodes in the background
    for obj in objs:
        asyncio.create_task(obj.start_server())
    
    print("Running test")
    
    
    
    await asyncio.sleep(5)
    objs[i-1].disableNode()
    await objs[0].checkNode(objs[i-1])

    await asyncio.sleep(10)
    print("")
    totMess = 0
    leader_id = 0
    for obj in objs:
        totMess += obj.nr_msg
        if obj.isLeader:
            leader_id = obj.id
    print(f"Leader is: {leader_id}\n")
    print(f"Nr of messages sent: {totMess}")
    print("---------------------------------------------------------------------------")
    return


if __name__ == '__main__':
    try:
        # change the number of nodes for differnt tests.
        asyncio.run(setup_nodes(120))
    except RuntimeError as e:
        # If the event loop is already running, use create_task to handle it
        if str(e) == "asyncio.run() cannot be called from a running event loop":
            loop = asyncio.get_event_loop()
            loop.create_task(setup_nodes())
            loop.run_forever()

