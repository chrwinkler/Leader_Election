from node import Node
import asyncio
from message import Message

async def setup_nodes(node_count):
    nodes = []
    nr_msg = 0
    sPort = 5000

    # Create nodes with unique ports
    objs = [Node(n, nodes, nr_msg, sPort+n) for n in range(1, node_count + 1)]

    # Start servers for all nodes in the background
    for obj in objs:
        asyncio.create_task(obj.start_server())

    # Allow time for all nodes to start listening
    await asyncio.sleep(2)

    return objs

async def run_test1(nodes):
    print ("")
    print("---------------------------------------------------------------------------")
    print ("")
    print("TEST 1: Starting from lowest ID")

    # Trigger election from the lowest ID node
    await nodes[0].startElection()  # Node 1 starts the election

    # Wait for the election to finish
    await asyncio.sleep(5)  # Adjust this time if necessary

    # Check which node became the leader
    for node in nodes:
        print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

async def run_test2(nodes):
    print ("")
    print("---------------------------------------------------------------------------")
    print ("")
    print("TEST 2: Starting from middle ID")

    # Reset necessary states
    for node in nodes:
        node.isLeader = False
        node.leaderID = None  # Reset leader ID for all nodes

    # Trigger election from the middle node (Node 3 if nodes are 5)
    await nodes[2].startElection()  # Node 3 starts the election

    # Wait for election to finish
    await asyncio.sleep(5)

    # Check results
    for node in nodes:
        print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

async def run_test3(nodes):
    print ("")
    print("---------------------------------------------------------------------------")
    print ("")
    print("TEST 3: Leader is not answering")

    # Simulate the leader being disabled (Node 3 as an example)
    nodes[2].disableNode()  # Disable Node 3
    await nodes[0].checkNode(nodes[2])  # Node 1 checks Node 3

    # Wait for the response check to finish
    await asyncio.sleep(5)

    for node in nodes:
        print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

async def main():
    # Setup nodes with a maximum of 5 nodes
    nodes = await setup_nodes(5)

    await run_test1(nodes)
    await run_test2(nodes)
    await run_test3(nodes)

    # Clean up: Assume a way to close any active connections if needed
    # This can be implemented depending on how you want to handle server shutdown
    # For now, we skip the shutdown logic as per your request not to modify Node class

if __name__ == '__main__':
    asyncio.run(main())
