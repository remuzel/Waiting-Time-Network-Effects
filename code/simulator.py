import numpy as np
from tqdm import tqdm

from rideshare_platform import Platform

class Simulator:
    """ This class is responsible for running individual market share simulations. """

    def __init__(self, population_size, platform_names):
        self.N = population_size
        self.platforms = [Platform(name, population_size) for name in platform_names]
        self.platform_indices = list(range(len(self.platforms)))

    def get_market_shares(self):
        """ Returns the market share of each registered platform. """
        return [platform.get_market_share(self.N) for platform in self.platforms]

    def growth(self, indices, g):
        """ Adds the indicated growth (g) to the flagged platforms.
        """
        for i in indices:
            self.platforms[i].add_user(g)

    def run(self, time):
        """ Simulates the change in market share for each platform and
        returns their metrics.
        """

        for _ in tqdm(range(time)): 
            if self.N:
                # Choose a platfrom to grow 
                growing_platform = np.random.choice(self.platform_indices)
                # Grow the chosen platform, and not the rest 
                self.growth([growing_platform], 1)
                self.growth(np.delete(self.platform_indices, growing_platform), 0)
                self.N -= 1
            else:
                self.growth(self.platform_indices, 0)
        return self