from node import Node
import asyncio
from message import Message
import time

"""
    This test is used to to check if the system work in basic scenarios.
    here we disable a node and check if the other nodes can detect it.
    and count the number of messages sent.
"""

# Simulation setup for nodes
async def setup_nodes():
    nodes = []
    nr_msg = 0
    # Create nodes with unique ports
    node1 = Node(1, nodes, nr_msg, 5001)
    node2 = Node(2, nodes, nr_msg, 5002)
    node3 = Node(3, nodes, nr_msg, 5003)
    node4 = Node(4, nodes, nr_msg, 5004)
    print("Running test")
    # Start the servers for all nodes
    # Start servers for all nodes in the background
    asyncio.create_task(node1.start_server())
    asyncio.create_task(node2.start_server())
    asyncio.create_task(node3.start_server())
    asyncio.create_task(node4.start_server())
    
    await asyncio.sleep(5)
    print("DISABLING NODE 4")
    node4.disableNode()
    await asyncio.sleep(3)
    print("NODE 1 CHECKS NODE 4")
    await node1.checkNode(node4)
    await asyncio.sleep(5)
    print("REPEARING NODE 4")
    await node4.repairNode()
     # Keep running the program for further testing
    
    await asyncio.sleep(5)
    print("")
    print(f"Nr of messages sent: {node1.nr_msg+node2.nr_msg+node3.nr_msg+node4.nr_msg}")
    print("---------------------------------------------------------------------------")
    return

if __name__ == '__main__':
    try:
        asyncio.run(setup_nodes())
    except RuntimeError as e:
        # If the event loop is already running, use create_task to handle it
        if str(e) == "asyncio.run() cannot be called from a running event loop":
            loop = asyncio.get_event_loop()
            loop.create_task(setup_nodes())
            loop.run_forever()