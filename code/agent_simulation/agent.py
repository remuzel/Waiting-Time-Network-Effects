

class Agent():
    """ 
    Overall clas for the agents
    """
    def __init__(self, name):
        self.name = name

    def decide(self, data):
        pass

class User(Agent):
    """ user agent """
    def __init__(self, name):
        super().__init__(name)


class Driver(Agent):
    """ driver agent """
    def __init__(self, name):
        super().__init__(name)
