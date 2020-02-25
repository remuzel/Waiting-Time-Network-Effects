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
        n_u, n_d = data['n_users'], data['n_drivers']
        ms = data['market_shares']
        # Get the distances to each platforms' users and drivers
        u = 1 / np.linalg.norm(self.position - u, axis=1)
        d = 1 / np.linalg.norm(self.position - d, axis=1)
        # Apply the decision function and make the decision
        p = n_u * self.u * u/u.sum() + n_d * self.d * d/d.sum()
        if p.min() < 0:
            p -= 2* p.min()
        choice = np.random.choice(indices, p=p/p.sum())
        self.rhp = choice
        return choice

class User(Agent):
    """ user agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform"):
        super().__init__(grid_shape, lorenz_coef, geograph_mode)
        self.d = 1
        self.u = -1

class Driver(Agent):
    """ driver agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform"):
        super().__init__(grid_shape, lorenz_coef, geograph_mode)
        self.d = -1
        self.u = 1