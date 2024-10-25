from ..OriginalVersion.node import Node
import asyncio
from ..OriginalVersion.message import Message
import time

# Simulation setup for nodes
async def setup_nodes():
    nodes = []
    nr_msg = 0
    # Create nodes with unique ports
    node1 = Node(1, nodes,nr_msg, 5001)
    node2 = Node(2, nodes,nr_msg, 5002)
    node3 = Node(3, nodes,nr_msg, 5003)
    node4 = Node(4, nodes,nr_msg, 5004)
    node5 = Node(5, nodes,nr_msg, 5005)
    node6 = Node(6, nodes,nr_msg, 5006)
    node7 = Node(7, nodes,nr_msg, 5007)
    node8 = Node(8, nodes,nr_msg, 5008)
    node9 = Node(9, nodes,nr_msg, 5009)
    node10 = Node(10, nodes,nr_msg, 5010)
    node11 = Node(11, nodes,nr_msg, 5011)
    node12 = Node(12, nodes,nr_msg, 5012)
    node13 = Node(13, nodes,nr_msg, 5013)
    node14 = Node(14, nodes,nr_msg, 5014)
    node15 = Node(15, nodes,nr_msg, 5015)
    node16 = Node(16, nodes,nr_msg, 5016)
    node17 = Node(17, nodes,nr_msg, 5017)
    node18 = Node(18, nodes,nr_msg, 5018)
    node19 = Node(19, nodes,nr_msg, 5019)
    node20= Node(20, nodes,nr_msg, 5020)

    print("Running test")
    # Start the servers for all nodes
    # Start servers for all nodes in the background
    asyncio.create_task(node1.start_server())
    asyncio.create_task(node2.start_server())
    asyncio.create_task(node3.start_server())
    asyncio.create_task(node4.start_server())
    
    await asyncio.sleep(5)
    print("DISABLING NODE 20")
    node20.disableNode()
    await asyncio.sleep(3)
    print("NODE 1 CHECKS NODE 20")
    await node1.checkNode(node20)
    await asyncio.sleep(5)
    print("REPEARING NODE 20")
    await node20.repairNode()
     # Keep running the program for further testing
    
    await asyncio.sleep(5)
    print("")
    print("Orinal Version")
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
