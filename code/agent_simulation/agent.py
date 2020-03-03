import logging
import numpy as np

import sys
sys.path.append("..")
from base_simulation.utils import shift

LOGGER = logging.getLogger(__name__)

class Agent():
    """ 
    Overall clas for the agents
    """
    def __init__(self, grid_shape, lorenz_coef, geograph_mode):
        # Randomly generate the rider in the given grid_shape with the given method
        if geograph_mode == "uniform":
            x = np.random.randint(grid_shape[1])
            y = np.random.randint(grid_shape[0])
        self.position = np.array([y, x])
        self.lorenz = lambda ms: np.power(1 - np.power(ms, lorenz_coef), 1/lorenz_coef)

    def decide(self, data):
        # Unpack the given data
        indices = data['platform_indices']
        pos_r, pos_d = data['riders'], data['drivers']
        n_r, n_d = data['n_riders'], data['n_drivers']
        ms = data['market_shares']
        # Get the distances to each platforms' riders and drivers
        dist_r = 1 / np.linalg.norm(self.position - pos_r, axis=1)
        dist_d = 1 / np.linalg.norm(self.position - pos_d, axis=1)
        # The agent count is weighed w.r.t. other platforms to introduce barabasi
        # Platform value is reduced if the agent is surrounded by same-typed agents
        rider_component = shift(n_r/n_r.sum() + self.r * dist_r/dist_r.sum())
        driver_component = shift(n_d/n_d.sum() + self.d * dist_d/dist_d.sum())
        p = self.lorenz(ms) * (rider_component + driver_component)
        choice = np.random.choice(indices, p=p/p.sum())
        self.rhp = choice
        return choice

class Rider(Agent):
    """ rider agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform"):
        super().__init__(grid_shape, lorenz_coef, geograph_mode)
        self.d = 1
        self.r = -1
        self.is_rider = True

class Driver(Agent):
    """ driver agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform"):
        super().__init__(grid_shape, lorenz_coef, geograph_mode)
        self.d = -1
        self.r = 1
        self.is_rider = False