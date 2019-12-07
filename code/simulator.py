import numpy as np
from tqdm import tqdm

from rideshare_platform import Platform

class Simulator:
    """ This class is responsible for running individual market share simulations. """

    def __init__(self, population_size, platform_names, selector):
        self.N = population_size
        self.platforms = [Platform(name, len(platform_names)) for name in platform_names]
        self.platform_indices = list(range(len(self.platforms)))
        self.selector = selector
        self.selector.set_platforms(self.platforms)

    def get_market_shares(self):
        """ Returns the market share of each registered platform. """
        return [platform.get_market_share() for platform in self.platforms]

    def growth(self, indices, g, t):
        """ Adds the indicated growth (g) to the flagged platforms.
        """
        for i in indices:
            self.platforms[i].add_user(g, t)

    def run(self, time):
        """ Simulates the change in market share for each platform and
        returns their metrics.
        """

        while time > 0:
            # Choose a platfrom to grow (g), and how long it takes (t)
            growing_platform, g, t = self.selector.select()
            # Grow the chosen platform, and not the rest 
            self.growth([growing_platform], g, g)
            self.growth(np.delete(self.platform_indices, growing_platform), 0, g)
            # Progress through time
            time -= t
        return self