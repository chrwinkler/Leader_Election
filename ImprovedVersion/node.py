import asyncio
from message import Message
import time
import random

class Node:
    """
        Initialization
    """
    def __init__(self, id: int, nodes: list, nr_msg: int, port: int):
        self.id = id
        self.isLeader = False
        self.leaderID = None
        self.nodes = nodes
        self.port = port  # Node-specific port for socket communication
        self.nodes.append(self)
        self.nodes.sort(key=lambda n: n.id, reverse=True)
        self.ok_recieved = False
        self.isDisabled = False
        self.gotResponse = False
        self.nr_msg = nr_msg
        self.electionInProg = False

        if len(self.nodes) == 0:
            self.isLeader()
        else:
            asyncio.create_task(self.isHighestID())

    # Tells that it is the highest ID
    async def isHighestID(self):
        c = 0
        for node in self.nodes:
            if node.id > self.id:
                c += 1
        if c == 0:
            await self.startElection()

    # Make the function wait n seconds
    def sleep(self, n):
        time.sleep(n)

    # Start the server to listen for messages
    async def start_server(self):
        server = await asyncio.start_server(self.handle_connection, '127.0.0.1', self.port)
        print(f"Node {self.id} is listening on port {self.port}")
        async with server:
            await server.serve_forever()

    # Handle incoming connections (asynchronously)
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(1024)
        message = data.decode()
        if message:
            msg_obj = Message.from_json(message)  # Assuming Message class has a from_json method
            await self.recieveMessage(msg_obj)
        writer.close()
        await writer.wait_closed()

    # Send a message to a specific node using asyncio-compatible streams
    async def sendMessage(self, reciever_id: int, message_type):
        if self.isDisabled:
            return
        for node in self.nodes:
            if node.id == reciever_id:
                try:
                    reader, writer = await asyncio.open_connection('127.0.0.1', node.port)
                    message = Message(self.id, node.id, message_type)
                    writer.write(message.to_json().encode())
                    await writer.drain()  # Ensure the message is sent
                    print(f"Message sent: {message}")
                    writer.close()
                    await writer.wait_closed()
                    self.nr_msg += 1
                except Exception as e:
                    print(f"Failed to send message to Node {reciever_id}: {e}")

    # Check if it gets a response from a node
    async def checkNode(self, node):
        try:
            #print(f"Node {self.id} is checking Node {node.id}")
            await self.sendMessage(node.id, "CheckNode")
            await asyncio.sleep(2)
            if not self.gotResponse:
                print(f"No response from Node {node.id}. Starting election...")
                await self.startElection()
            else:
                self.gotResponse = False  # Reset the response flag
        except RuntimeError as e:
            print(f"RuntimeError encountered: {e}. Starting election...")
            await self.startElection()

    # Turns off the node
    def disableNode(self):
        self.isDisabled = True
        self.isLeader = False

    # Turns on the node
    async def repairNode(self):
        self.isDisabled = False
        await self.isHighestID()

    """
        Receiving Message
    """
    async def recieveMessage(self, message: Message):
        # Check if the node is disabled
        if self.isDisabled:
            return # Exit if the node cannot receive messages
        
        print(f"Message received: {message}")
        
        #Process the received message
        if message.message_type == "Election":
            # If the received message is an election message
            if message.sender_id < self.id:
                # Responnd with an "OK" message indicating that this node is still active
                await self.sendMessage(message.sender_id, "Ok")
                # Start a new election
                if (self.electionInProg == False):
                    self.electionInProg = True
                    await asyncio.sleep(random.uniform(0.1, 1.0))
                    await self.startElection()
                    
        elif message.message_type == "Ok":
            # If the received message is an "OK" message
            self.ok_recieved = True
            
        elif message.message_type == "Coordinator":
            # If the received message is a "Coordinator" message
            self.isLeader = False
            self.leaderID = message.sender_id
            await asyncio.sleep(3)
            self.ok_recieved = False
            self.electionInProg = False
            
        elif message.message_type == "CheckNode":
            # If the received message is a "CheckNode" message
            await self.sendMessage(message.sender_id, "RESPONSE")
            
        elif message.message_type == "RESPONSE":
            # If the received message is a "RESPONSE" message
            self.gotResponse = True

    '''
        Improved Version
    '''
    """
        Starting Election
    """
    async def startElection(self):
        # Check if the node is disabled
        if self.isDisabled or self.ok_recieved:
            return # Exit if the node cannot start an election
        
        self.electionInProg = True
        print("Node "+str(self.id)+" is starting election")
        
        # nlen is the total number of nodes
        nlen = len(self.nodes)
        
        # Determine the number of nodes to send the election message to
        if nlen >= 30: # more then 30 nodes, then send to 1/5 of the nodes
            bound = int(nlen / 5)
        elif nlen >= 100: # more then 100 nodes, then send to 1/10 of the nodes
            bound = int(nlen / 10)
        else:
            bound = int(nlen / 2) # Orherwise send to half of the nodes
            
        c = 0
        selfInBound = False # Flag to check if the current node is in the bound range
        
        # Start sending election messages 
        while(self.nodes[c].id >= self.id):
            if (self.ok_recieved):
                return # Exit if the node has received an "OK" message
            
            # Check if the current node is in the bound range
            if (self.nodes[bound].id < self.id):
                selfInBound = True
            
            # Iterate over the range of nodes to send the election message to
            for i in range(c,bound):
                if self.nodes[i].id > self.id:
                    asyncio.create_task(self.sendMessage(self.nodes[i].id, "Election"))
                elif self.nodes[i].id == self.id:
                    selfInBound = True
            
            #Timeout
            await asyncio.sleep(2)
            
            if self.ok_recieved:
                return # Exit if the node has received an "OK" message
            else:
                # Check if the current node is in the bound range
                if selfInBound:
                    await self.IsLeader() # Declare this node as the leader
                    return
                
                # Update the counters for next iteration
                c = bound
                bound += bound
                
                # Ensure that the bound does not exceed the total number of nodes
                if bound > nlen:
                    bound = nlen
        #else:
        await self.IsLeader()


    """
        Setting Coordinator
    """
    async def IsLeader(self):
        # Mark the election as finished
        self.electionInProg = False
        
        # Check if node is already the leader
        if self.isLeader:
            return # Exit if the node is already the leader
        
        # Declare the node as the leader
        self.isLeader = True
        self.leaderID = self.id

        # Notify all other nodes that this node is the new coordinator
        for node in self.nodes:
            if node != self:
                await self.sendMessage(node.id, "Coordinator")