import asyncio
from message import Message
import time
import random

class Node:
    """Initialization"""
    def __init__(self, id: int, nodes: list, nr_msg: int, port: int):
        self.id = id
        self.isLeader = False
        self.leaderID = None
        self.nodes = nodes
        self.port = port  # Node-specific port for socket communication
        nodes.append(self)
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
        try:
            data = await reader.read(1024)
            message = data.decode()
            if message:
                msg_obj = Message.from_json(message)  # Assuming Message class has a from_json method
                await self.recieveMessage(msg_obj)
        except asyncio.TimeoutError:
            print(f"Reading data from connection timed out.")
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
    
    # Send a message to a specific node using asyncio-compatible streams
    async def sendMessage(self, reciever_id: int, message_type):
        if self.isDisabled:
            return
        for node in self.nodes:
            if node.id == reciever_id:
                try:
                    
                    try:
                        reader, writer = await asyncio.open_connection('127.0.0.1', node.port)
                    except asyncio.TimeoutError:
                        print(f"Connection to Node {node.id} timed out.")
                        return
                    message = Message(self.id, node.id, message_type)
                    writer.write(message.to_json().encode())
                    try:
                        # Apply a timeout to writer.drain() as well
                        await writer.drain()
                        print(f"Message sent: {message}")
                    except asyncio.TimeoutError:
                        print(f"Writing to Node {node.id} timed out.")
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

    """Receiving Message"""
    async def recieveMessage(self, message: Message):
        if self.isDisabled:
            return
        print(f"Message received: {message}")
        if message.message_type == "Election":
            if message.sender_id < self.id:
                
                await self.sendMessage(message.sender_id, "Ok")
                if (self.electionInProg == False):
                    self.electionInProg = True
                    await asyncio.sleep(random.uniform(0.1, 1.0))
                    await self.startElection()
        elif message.message_type == "Ok":
            self.ok_recieved = True
        elif message.message_type == "Coordinator":
            self.isLeader = False
            self.leaderID = message.sender_id
            await asyncio.sleep(3)
            self.ok_recieved = False
            self.electionInProg = False
        elif message.message_type == "CheckNode":
            await self.sendMessage(message.sender_id, "RESPONSE")
        elif message.message_type == "RESPONSE":
            self.gotResponse = True

    """Starting Election"""
    async def startElection(self):
        if self.isDisabled or self.ok_recieved:
            return
        
        print("Node "+str(self.id)+" is starting election")
        for node in self.nodes:
            if node.id > self.id:
                await asyncio.sleep(0.1)
                asyncio.create_task(self.sendMessage(node.id, "Election"))
        #Timeout
        await asyncio.sleep(2)
        if self.ok_recieved:
            return
        else:
            await self.IsLeader()

    """Setting Coordinator"""
    async def IsLeader(self):
        self.electionInProg = False
        if self.isLeader:
            return
        self.isLeader = True
        self.leaderID = self.id

        for node in self.nodes:
            if node != self:
                await self.sendMessage(node.id, "Coordinator")