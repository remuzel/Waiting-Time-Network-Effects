import logging
import numpy as np
from tqdm import tqdm

from agent import User, Driver

import sys
sys.path.append("..")
from base_simulation.rideshare_platform import Platform
from base_simulation.simulator import Simulator

LOGGER = logging.getLogger(__name__)

class AgentSimulator(Simulator):
    """ Underlying class for a classical simulator
    """
    def __init__(self, population_size, platform_names,
                city_shape=(500,500), delta_ts=[], user_proportion=0.8,
                agent_vision=None, lorenz=2):
        super().__init__(population_size, platform_names, None, delta_ts)
        self.user_proportion = [user_proportion, 1-user_proportion]
        # Setup a storage for agent-type (0: user, 1: driver) and position
        self.agents = {0: [], 1: []}
        # Setup the shape of the city & agents' vision range
        self.xy = city_shape
        self.agent_vision = agent_vision
        if agent_vision is None:
            self.agent_vision = 0.05 * np.mean(self.xy)
        # Set the first average user for each platform
        [p.set_avg_user(self.xy[1], self.xy[0]) for p in self.platforms]
        # Set the lorenz coef
        self.c = lorenz

    def sample_agent(self):
        """ Randomly generate either a user or a driver """
        is_diver = np.random.choice([0, 1], p=self.user_proportion)
        return is_diver, Driver(self.xy, lorenz_coef=self.c) if is_diver else User(self.xy, lorenz_coef=self.c)

    def get_platform_indices(self):
        """ Returns the indices of active platforms """
        return [i for i,p in enumerate(self.platforms) if p.isActive()]

    def get_nearby_agents(self, root):
        nearby = [[], []]
        for i in [0, 1]:
            for agent in self.agents[i]:
                if np.linalg.norm(root - agent.position) <= self.agent_vision:
                    nearby[i].append(agent)
        return nearby

    def run(self):
        """ Overwritting the simulators' run method - generating from total pop instead. """
        for _ in range(self.N):
            # Generate an agent
            is_user, agent = self.sample_agent()
            pos = agent.position
            # Gather data about the simulation to pass onto the agent
            nearby_users, nearby_drivers = self.get_nearby_agents(pos)
            # Get the number of users in each platform
            platform_u = [0] * len(self.get_platform_indices())
            for u in nearby_users:
                platform_u[u.rhp] += 1
            # Get the number of drivers in each platform
            platform_d = [0] * len(self.get_platform_indices())
            for d in nearby_drivers:
                platform_d[d.rhp] += 1
            data = {
                'platform_indices': self.get_platform_indices(),
                'users': np.array(platform_u),
                'drivers': np.array(platform_d),
                'market_shares': self.get_recent_market_shares()
            }
            # Make the agent chose a platform
            growing_platform = agent.decide(data)
            # Grow them accordingly
            self.growth([growing_platform], position=pos)
            self.growth(np.delete(self.platform_indices, growing_platform), g=0, position=pos)
            # Keep the agent in memory
            self.agents[is_user].append(agent)
        return self