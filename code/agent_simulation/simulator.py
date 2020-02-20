import __init__

import numpy as np
from tqdm import tqdm

from agent import User, Driver

class AgentSimulator(Simulator):
    """ Underlying class for a classical simulator
    """
    def __init__(self, population_size, platform_names, selector,
                delta_ts=0, user_proportion=0.8, agent_vision=150):
        super().__init__(population_size, platform_names, selector, delta_ts)
        self.user_proportion = [user_proportion, 1-user_proportion]
        # Setup a storage for agent-type (0: user, 1: driver) and position
        self.agents = {0: [], 1: []}
        # Register the range of vision of each agent
        self.agent_vision = agent_vision

    def sample_agent(self):
        """ Randomly generate either a user or a driver """
        is_diver = np.random.choice([0, 1], p=self.user_proportion)
        return is_diver, Driver() if is_diver else User()

    def get_platform_indices(self):
        """ Returns the indices of active platforms """
        return [i for i,p in enumerate(self.platforms) if p.isActive()]

    def get_nearby_agents(self, root):
        nearby = [0, 0]
        for i in [0, 1]:
            if len(self.agents[i]):
                # Get the distance from the new user to all others
                distances = np.linalg.norm(root - self.agents[i], axis=1)
                # Count those within the agents vision
                nearby[i] += len(np.where(distances <= self.agent_vision)[0])
        return nearby

    def run(self):
        """ Overwritting the simulators' run method - counting down users instead. """
        for _ in self.N:
            # Generate an agent
            is_user, agent = self.sample_agent()
            pos = agent.position

            # Record its type and position
            self.agents[is_user].append(pos)

            # Gather data about the simulation to pass onto the agent
            nearby_users, nearby_drivers = self.get_nearby_agents(pos)
            data = {
                'platform_indices': self.get_platform_indices(),
                'users': nearby_users,
                'drivers': nearby_drivers,
                'market_shares': self.get_market_shares()
            }

            # Make the agent chose a platform
            growing_platform = agent.decide(data)
            # Grow them accordingly
            self.growth([growing_platform], position=pos)
            self.growth(np.delete(self.platform_indices, growing_platform), n=0, position=pos)
        return self



class Simulator:
    """ This class is responsible for running individual market share simulations. """

    def __init__(self, population_size, platform_names, selector, delta_ts):
        # Set the population size
        self.N = population_size
        # Create the platforms and index them
        self.platforms = [Platform(name, len(platform_names)) for name in platform_names]
        self.platform_indices = lrange(self.platforms)
        # Initialise the selector with the platforms
        self.selector = selector
        self.selector.set_platforms(self.platforms)
        # If a stary delay is present, apply it 
        self.delay_platforms(delta_ts)
        self.is_density = self.selector.name.startswith('Density')

    def delay_platforms(self, delta_ts):
        """ Turns off a set of platforms until the given timestep is met """
        for p_index, delta_t in delta_ts:
            self.platforms[p_index].deactivate(delta_t)

    def get_market_shares(self):
        """ Returns the market share of each registered platform. """
        return [platform.get_market_share() for platform in self.platforms]

    def growth(self, indices, g, t, position):
        """ Adds the indicated growth (g) to the flagged platforms.
        """
        for i in indices:
            self.platforms[i].add_user(g, t, position)

    def run(self, time):
        """ Simulates the change in market share for each platform and
        returns their metrics.
        """

        while time > 0:
            # Choose a platfrom to grow (g), and how long it takes (t)
            if self.is_density:
                growing_platform, g, t, p = self.selector.select()
            else:
                p = None
                growing_platform, g, t = self.selector.select()
            # Grow the chosen platform, and not the rest 
            self.growth([growing_platform], g, g, position=p)
            self.growth(np.delete(self.platform_indices, growing_platform), 0, g, position=p)
            # Progress through time
            time -= t
        return self