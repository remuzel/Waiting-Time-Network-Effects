import numpy as np

class Selector:
    """ Parent class for all random selectors """
    def __init__(self, growth=1):
        self.n = growth

    def select(self):
        """ Given indices to choose from will return one of them
        w.r.t. the specific method.
        Will always return a tuple:
            (index, growth_amount, time_taken)
        """
        # do nothing
        pass

    def set_platforms(self, platforms):
        """ Sets the Platform objects that the selector will select from """
        self.platforms = platforms
        self.p_indices = list(range(len(platforms)))

class Random(Selector):
    """ Selects an indice at random, w.r.t. given probabilities """

    def __init__(self, probabilities, growth=1):
        super().__init__(growth)
        self.name = "Random"
        self.ps = probabilities
    
    def select(self):
        super().select()

        return np.random.choice(self.p_indices, p=self.ps), self.n, 1

class Uniform(Selector):
    """ Uniformly selects an indice """

    def __init__(self, growth=1):
        super().__init__(growth)
        self.name = "Uniform"

    def select(self):
        super().select()

        return np.random.choice(self.p_indices), self.n, 1
    
class Poisson(Selector):
    """ Selects an indice w.r.t. Poisson arrival process """

    def __init__(self, lambdas, growth=1):
        super().__init__(growth)
        self.name = "Poisson"
        self.ls = lambdas

    def select(self):
        super().select()
        arrivals = [np.random.exponential(1/l) for l in self.ls]
        return np.argmin(arrivals), self.n, min(arrivals)

class Barabasi(Selector):
    """ Selects the Platform w.r.t. to it's relative size """

    def __init__(self, growth=1):
        super().__init__(growth)
        self.name = "Barabasi"
    
    def get_platform_shares(self):
        platforms_shares = np.array([p.market_share[-1] for p in self.platforms])
        return platforms_shares / np.sum(platforms_shares)

    def select(self):
        super().select()
        return np.random.choice(self.p_indices, p=self.get_platform_shares()), self.n, 1
