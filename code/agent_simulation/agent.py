import logging
import numpy as np

LOGGER = logging.getLogger(__name__)

class Agent():
    """ 
    Overall clas for the agents
    """
    def __init__(self, grid_shape, lorenz_coef, geograph_mode):
        # Randomly generate the user in the given grid_shape with the given method
        if geograph_mode == "uniform":
            x = np.random.randint(grid_shape[1])
            y = np.random.randint(grid_shape[0])
        self.position = np.array([y, x])
        self.lorenz = lambda ms: np.power(1 - np.power(ms, lorenz_coef), 1/lorenz_coef)

    def decide(self, data):
        # Unpack the given data
        indices = data['platform_indices']
        u, d = data['users'], data['drivers']
        ms = data['market_shares']
        # Apply the decision function and make the decision
        size_factor = self.lorenz(ms)
        p = (1 - size_factor) * (self.u_factor * u + self.d_factor * d) + size_factor * ms
        choice = np.random.choice(indices, p=p/p.sum())
        self.rhp = choice
        return choice

class User(Agent):
    """ user agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform"):
        super().__init__(grid_shape, lorenz_coef, geograph_mode)
        self.u_factor = 0.6
        self.d_factor = 0.4

class Driver(Agent):
    """ driver agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform"):
        super().__init__(grid_shape, lorenz_coef, geograph_mode)
        self.u_factor = 0.9
        self.d_factor = 0.1