"""
class Election:

    def __init__(self, initiating_node, higher_priority_nodes):
       self.initiating_node = initiating_node
       self.higher_priority_nodes = higher_priority_nodes
    
    def conductElection(self):
        if not self.higher_priority_nodes:
            self.announceCoordinator()
        else:
            for node in self.higher_priority_nodes:
                self.initiating_node.sendMessage("Election", node.id)

    def announceCoordinator(self):
        self.initiating_node.isLeader = True
        self.initiating_node.leaderID = self.initiating_node.id
        for node in self.initiating_node.nodes:
            if node.id != self.initiating_node.id:
                self.initiating_node.sendMessage("Coordinator", node.id)
"""