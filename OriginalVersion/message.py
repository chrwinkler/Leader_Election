import json

class Message:
    
    def __init__(self, sender_id: int, reciever_id: int, message_type: str):
        self.sender_id = sender_id
        self.reciever_id = reciever_id
        self.message_type = message_type

    def __str__(self):
        return f"Message(type: {self.message_type}, from: {self.sender_id}, to: {self.reciever_id})"

    # Convert Message object to a JSON string
    def to_json(self):
        return json.dumps({
            'sender_id': self.sender_id,
            'reciever_id': self.reciever_id,
            'message_type': self.message_type
        })

    # Static method to convert JSON string back to Message object
    @staticmethod
    def from_json(json_string: str):
        data = json.loads(json_string)
        return Message(data['sender_id'], data['reciever_id'], data['message_type'])

