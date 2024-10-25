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
    print("")
    print("---------------------------------------------------------------------------")
    print("")
    print("TEST 1: Starting from lowest ID")
    
    # Node 1 starts the election
    await nodes[0].startElection()  # Node 1 initiates the election

    # Wait for the election to finish
    await asyncio.sleep(5)

    # Check which node became the leader
    for node in nodes:
        print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

async def run_test2(nodes):
    print("")
    print("---------------------------------------------------------------------------")
    print("")
    print("TEST 2: Starting from middle ID")
    

    # Reset leader states for all nodes
    for node in nodes:
        node.isLeader = False
        node.leaderID = None  # Reset leader ID

    # Node 3 starts the election
    await nodes[2].startElection()  # Node 3 initiates the election

    # Wait for election to finish
    await asyncio.sleep(5)

    # Check results
    for node in nodes:
        print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

async def run_test3(nodes):
    print("")
    print("---------------------------------------------------------------------------")
    print("")
    print("TEST 3: Leader is not answering")
    print("")

    # Simulate Node 5 becoming disabled
    nodes[4].disableNode()  # Disable Node 5
    
    # Node 2 checks the status of Node 5 (the leader)
    await nodes[1].checkNode(nodes[4])  # Node 2 checks Node 5

    # Since Node 5 is disabled, Node 2 starts an election
    await nodes[1].startElection()

    # Wait for election to finish
    await asyncio.sleep(5)

    # Check results after election
    for node in nodes:
        print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

async def main():
    # Setup nodes with a maximum of 5 nodes
    nodes = await setup_nodes(5)

    await run_test1(nodes)
    await run_test2(nodes)
    await run_test3(nodes)

if __name__ == '__main__':
    asyncio.run(main())
