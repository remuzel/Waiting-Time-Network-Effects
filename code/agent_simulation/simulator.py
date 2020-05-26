import logging
import numpy as np
from tqdm import tqdm

from agent import Rider, Driver
from rhp import Platform

import sys
sys.path.append("..")
from base_simulation.utils import lrange

LOGGER = logging.getLogger(__name__)

class AgentSimulator():
    """ Underlying class for a classical simulator
    """
    def __init__(self, population_size, platform_names,
                city_shape=(500,500), rider_proportion=0.8,
                agent_vision=None, lorenz=2, mu_R=0.5, mu_D=0.5, eta=0, n_joins=1):
                
        # Set the population size
        self.N = population_size
        # Create the platforms and index them
        self.platforms = [Platform(name, len(platform_names)) for name in platform_names]
        self.platform_indices = lrange(self.platforms)

        self.rider_proportion = [rider_proportion, 1-rider_proportion]
        # Setup the shape of the city & agents' vision range
        self.xy = city_shape
        # Set the first average user for each platform
        [p.set_avg_user(self.xy[1], self.xy[0]) for p in self.platforms]
        # Set the first average driver for each platform
        [p.set_avg_driver(self.xy[1], self.xy[0]) for p in self.platforms]
        # Set the lorenz coef
        self.c = lorenz
        # Set the death coefficients
        self.mu_R = mu_R
        self.mu_D = mu_D
        # Set the price coefficient
        self.eta = eta
        # Create rate storage
        self.rates = [[], []]
        # Keep track of how many agents join at each iteration
        self.n_joins = n_joins

    def growth(self, indices, is_driver, g=1, t=1, position=None):
        """ Adds the indicated growth (g) to the flagged platforms.
        """
        for i in indices:
            self.platforms[i].add_user(position, n=g, delta_pop=t, driver=is_driver)

    def sample_agent(self):
        """ Randomly generate either a user or a driver """
        is_driver = np.random.choice([0, 1], p=self.rider_proportion)
        if is_driver:
            return is_driver, Driver(self.xy, lorenz_coef=self.c, mu_R=self.mu_R, mu_D=self.mu_D, eta=self.eta)
        else:
            return is_driver, Rider(self.xy, lorenz_coef=self.c, mu_R=self.mu_R, mu_D=self.mu_D, eta=self.eta)

    def get_drivers(self):
        """ Returns the number of drivers of each registered platform. """
        return [platform.get_driver_history() for platform in self.platforms]

    def get_riders(self):
        """ Returns the number of riders of each registered platform. """
        return [platform.get_rider_history() for platform in self.platforms]

    def get_market_shares(self):
        """ Returns the market share of each registered platform. """
        return [platform.get_market_share() for platform in self.platforms]

    def get_recent_market_shares(self):
        """ Returns the most recent market share of each platform """
        return [platform.get_market_share()[-1] for platform in self.platforms]

    def get_recent_r_market_shares(self):
        """ Returns the most recent RIDER market share of each platform """
        return [platform.get_r_market_share()[-1] for platform in self.platforms]

    def get_recent_d_market_shares(self):
        """ Returns the most recent DRIVER market share of each platform """
        return [platform.get_d_market_share()[-1] for platform in self.platforms]

    def get_platform_indices(self):
        """ Returns the indices of active platforms """
        return [i for i,p in enumerate(self.platforms)]

    def get_average_riders(self):
        return [p.average_user for p in self.platforms]

    def get_average_drivers(self):
        return [p.average_driver for p in self.platforms]

    def run(self):
        """ Overwritting the simulators' run method - generating from total pop instead. """
        for _ in range(self.N):
            # Generate an agent
            is_driver, agent = self.sample_agent()
            pos = agent.position
            # Gather data about the simulation to pass onto the agent
            data = {
                'platform_indices': self.get_platform_indices(),
                'riders': self.get_average_riders(),
                'n_riders': np.array([p.riders for p in self.platforms]),
                'drivers': self.get_average_drivers(),
                'n_drivers': np.array([p.drivers for p in self.platforms]),
                'market_shares': self.get_recent_market_shares(),
                'r_market_shares': self.get_recent_r_market_shares(),
                'd_market_shares': self.get_recent_d_market_shares(),
                'total_joins': self.n_joins
            }
            # Make the agent chose a platform
            growths = agent.decide(data)
            # Keep track of the growing rates # TODO: Check the propagation of rates
            self.rates[agent.is_rider].append(agent.rate)
            # Grow all platforms according to their values
            for p, growth in zip(self.platform_indices, growths):
                self.growth([p], is_driver, position=pos, g=growth, t=self.n_joins)
        return self