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
    def __init__(self, grid_shape, lorenz_coef, geograph_mode, mu_R, mu_D):
        # Randomly generate the rider in the given grid_shape with the given method
        if geograph_mode == "uniform":
            x = np.random.randint(grid_shape[1])
            y = np.random.randint(grid_shape[0])
        self.position = np.array([y, x])
        self.lorenz = lambda ms: np.power(1 - np.power(ms, lorenz_coef), 1/lorenz_coef)
        self.mu_D = mu_D
        self.mu_R = mu_R
        self.eta = lambda : 0

    def decide(self, data):
        # Unpack the given data
        indices = data['platform_indices']
        pos_r, pos_d = data['riders'], data['drivers']
        n_r, n_d = data['n_riders'], data['n_drivers']
        ms, r_ms, d_ms = data['market_shares'], data['r_market_shares'], data['d_market_shares']
        n_joins = data['total_joins']
        # Decision based on rider or driver agent
        if self.is_rider:
            p = (d_ms - self.mu_R * (n_r/(n_d+n_r)) - self.eta()*n_d).clip(min=0)
            # p in [-mu_R, 1] -> [0, 1]
            # p = (p+self.mu_R)/(1+self.mu_R)
        else:
            p = (r_ms*self.c_I() - self.mu_D/(1+self.mu_A*self.c_A()) * (n_d/(n_r+n_d)) + self.eta()*n_r).clip(min=0)
            # p in [-mu_D, 1] -> [0, 1]
            # p = (p+self.mu_D)/(1+self.mu_D)
        self.rate = p
        # Translates the rates into actual joining numbers
        if len(p) > 1:
            # If there are multiple platforms, normalise the joining rates
            p = p/p.sum()
        return p * n_joins

class Rider(Agent):
    """ rider agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform", mu_R=0.5, mu_D=0.5):
        super().__init__(grid_shape, lorenz_coef, geograph_mode, mu_R, mu_D)
        self.d = 1
        self.r = -1
        self.is_rider = True

class Driver(Agent):
    """ driver agent """
    def __init__(self, grid_shape, lorenz_coef=2, geograph_mode="uniform", mu_R=0.5, mu_D=0.5):
        super().__init__(grid_shape, lorenz_coef, geograph_mode, mu_R, mu_D)
        self.d = -1
        self.r = 1
        self.is_rider = False
        # From the cell population model
        self.mu_A = 0
        self.c_A = lambda : 0
        self.c_I = lambda : 1