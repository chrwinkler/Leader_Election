class Message:
    
    def __init__(self,sender_id: int,reciever_id: int, message_type: str):
        
        self.sender_id = sender_id
        self.reciever_id = reciever_id
        self.message_type = message_type
        

    def __str__(self):
        return f"Message(type: {self.message_type}, from: {self.sender_id}, to: {self.reciever_id})"
