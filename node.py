from message import Message
import time
import asyncio

class Node:
    """Initialization"""
    def __init__(self, id: int, nodes: list):
        self.id = id
        self.isLeader = False
        self.leaderID = None
        self.nodes = nodes
        nodes.append(self)
        self.ok_recieved = False
        self.isDisabled = False
        self.gotResponse = False
        
        if (len(self.nodes) == 0):
            self.isLeader()
        else:
            self.isHighestID()

    #Tells that it is the highist id
    def isHighestID(self):
        c = 0
        for node in self.nodes:
            if node.id > self.id:
                c += 1
        if (c == 0):
            asyncio.run(self.startElection())
    
    # Make the function wait n seconds
    def sleep(self, n):
        time.sleep(n)

    # Check if it get response from node
    # Used for testing if node is alive
    async def checkNode(self, node):
        await self.sendMessage(node.id, "CheckNode")
        await asyncio.sleep(2)
        if self.gotResponse == False:
            self.gotResponse = True
            await (self.startElection())
        else:
            pass
    
    # Turns off the node
    def disableNode(self):
        self.isDisabled = True
        self.isLeader = False
    
    # Turns on the node
    def repairNode(self):
        self.isDisabled = False
        self.isHighestID()
    
    """Recieving Messege"""    
    async def recieveMessage(self,message:Message ):
        if self.isDisabled == True:
            return
        else:
            print(f"Message recieved: {message}")
            if message.message_type == "Election":
                if message.sender_id < self.id:
                    await self.sendMessage(message.sender_id, "Ok")
                    await self.startElection()
                else:
                    pass

            elif message.message_type == "Ok":
                self.ok_recieved = True
                pass
            
            elif message.message_type == "Coordinator":
                self.isLeader = False
                self.leaderID = message.sender_id
            elif message.message_type == "CheckNode":
                await self.sendMessage(message.sender_id, "RESPONSE")
            elif message.message_type == "RESPONSE":
                self.gotResponse = True
        
    
    """Send Messege"""
    async def sendMessage(self,reciever_id: int, message_type):
        #time_stamp = time
        if self.isDisabled == True:
            return
        else:
            for node in self.nodes:
                if node.id == reciever_id:
                    ## Checking through - test
                    print(f"Message sent: {Message(self.id,node.id,message_type)}")
                    await node.recieveMessage(Message(self.id,node.id,message_type))    

    """Starting Election"""
    async def startElection(self):
        if self.isDisabled == True:
            return
        else:
            print("Node "+str(self.id)+" is starting election")
            for node in self.nodes:
                if node.id > self.id:
                    asyncio.create_task(self.sendMessage(node.id, "Election"))
            
            await asyncio.sleep(2)
            if self.ok_recieved == True:
                self.ok_recieved = False
                pass
            else:
                await (self.IsLeader())
        
    """Setting Coordinator"""
    async def IsLeader(self):
        if (self.isLeader == True):
            return
        self.isLeader = True 
        self.leaderID = self.id

        for node in self.nodes:
            if node != self:
                await self.sendMessage(node.id, "Coordinator")
