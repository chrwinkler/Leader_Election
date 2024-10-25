from node import Node
import asyncio
from message import Message
import time

"""Test 1"""
print("TEST 1: Staring from lowest ID")
# Test setup
nodes = []
nr_msg = 0

node1 = Node(1, nodes, nr_msg, 5001)
node2 = Node(2, nodes, nr_msg, 5002)
node3 = Node(3, nodes, nr_msg, 5003)

# Trigger election from the lowest ID node
async def test_election(node):
    await node.startElection()

# Run the test
#asyncio.run(test_election(node1))

# Check which node became the leader
for node in nodes:
    print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

print("TEST 1 FINISHED")

"""Test 2"""
print("TEST 2: Staring from middle ID")
#Test Setup
node4 = Node(4, nodes, nr_msg, 5004)
node5 = Node(5, nodes, nr_msg, 5001)


#asyncio.run(test_election(node3))

for node in nodes:
    print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

print("TEST 2 FINISHED")


"""Test 3"""
print("TEST 3: Leader is not answering")
node5.disableNode()
asyncio.run(node3.checkNode(node5))
for node in nodes:
    print(f"Node {node.id} is leader: {node.isLeader}, Leader ID: {node.leaderID}, Is disabled: {node.isDisabled}")

print("TEST 3 FINISHED")