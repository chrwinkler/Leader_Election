import asyncio
from SecondITR.node2 import Node
from FirstITR.message import Message

"""Test 1"""
print("TEST 1: Staring from lowest ID")
# Test setup
nodes = []

node1 = Node(1, nodes)
node2 = Node(2, nodes)
node3 = Node(3, nodes)

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
node4 = Node(4, nodes)
node5 = Node(5, nodes)


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