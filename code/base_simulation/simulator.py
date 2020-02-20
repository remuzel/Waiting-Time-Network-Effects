import numpy as np
from tqdm import tqdm

from rideshare_platform import Platform
from utils import lrange

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