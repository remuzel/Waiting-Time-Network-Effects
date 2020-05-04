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
                city_shape=(500,500), delta_ts=[], rider_proportion=0.8,
                agent_vision=None, lorenz=2, mu_R=0.5, mu_D=0.5):
                
        # Set the population size
        self.N = population_size
        # Create the platforms and index them
        self.platforms = [Platform(name, len(platform_names)) for name in platform_names]
        self.platform_indices = lrange(self.platforms)
        # If a stary delay is present, apply it 
        self.delay_platforms(delta_ts)

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

    def delay_platforms(self, delta_ts):
        """ Turns off a set of platforms until the given timestep is met """
        for p_index, delta_t in delta_ts:
            self.platforms[p_index].deactivate(delta_t)

    def growth(self, indices, is_driver, g=1, t=1, position=None):
        """ Adds the indicated growth (g) to the flagged platforms.
        """
        for i in indices:
            self.platforms[i].add_user(position, n=g, delta_pop=t, driver=is_driver)

    def sample_agent(self):
        """ Randomly generate either a user or a driver """
        is_driver = np.random.choice([0, 1], p=self.rider_proportion)
        if is_driver:
            return is_driver, Driver(self.xy, lorenz_coef=self.c, mu_R=self.mu_R, mu_D=self.mu_D)
        else:
            return is_driver, Rider(self.xy, lorenz_coef=self.c, mu_R=self.mu_R, mu_D=self.mu_D)

    def get_drivers(self):
        """ Returns the number of drivers of each registered platform. """
        return [platform.get_driver_history() for platform in self.platforms if platform.isActive()]

    def get_riders(self):
        """ Returns the number of riders of each registered platform. """
        return [platform.get_rider_history() for platform in self.platforms if platform.isActive()]

    def get_market_shares(self):
        """ Returns the market share of each registered platform. """
        return [platform.get_market_share() for platform in self.platforms if platform.isActive()]

    def get_recent_market_shares(self):
        """ Returns the most recent market share of each platform """
        return [platform.get_market_share()[-1] for platform in self.platforms if platform.isActive()]

    def get_recent_r_market_shares(self):
        """ Returns the most recent RIDER market share of each platform """
        return [platform.get_r_market_share()[-1] for platform in self.platforms if platform.isActive()]

    def get_recent_d_market_shares(self):
        """ Returns the most recent DRIVER market share of each platform """
        return [platform.get_d_market_share()[-1] for platform in self.platforms if platform.isActive()]

    def get_platform_indices(self):
        """ Returns the indices of active platforms """
        return [i for i,p in enumerate(self.platforms) if p.isActive()]

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
                'n_riders': np.array([p.users for p in self.platforms]),
                'drivers': self.get_average_drivers(),
                'n_drivers': np.array([p.drivers for p in self.platforms]),
                'market_shares': self.get_recent_market_shares(),
                'r_market_shares': self.get_recent_r_market_shares(),
                'd_market_shares': self.get_recent_d_market_shares()
            }
            # Make the agent chose a platform
            growing_platform = agent.decide(data)
            if growing_platform is None:
                # Don't grow any platform
                self.growth(self.platform_indices, is_driver, g=0, position=pos, t=0)
            else:
                # Grow them accordingly
                self.growth([growing_platform], is_driver, position=pos)
                self.growth(np.delete(self.platform_indices, growing_platform), is_driver, g=0, position=pos)
        return self