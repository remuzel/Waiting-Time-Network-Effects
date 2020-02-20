

class Agent():
    """ 
    Overall clas for the agents
    """
    def __init__(self, name, shape, mode="uniform"):
        self.name = name
        # Randomly generate the user in the given shape with the given method
        if mode == "uniform":
            x = np.random.randint(shape[1])
            y = np.random.randint(shape[0])
        self.position = np.array([y, x])

class User(Agent):
    """ user agent """
    def __init__(self, name):
        super().__init__(name)

    def decide(self, data):
            pass

class Driver(Agent):
    """ driver agent """
    def __init__(self, name):
        super().__init__(name)

    def decide(self, data):
        pass