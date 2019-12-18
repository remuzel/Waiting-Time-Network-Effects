import numpy as np
from utils import lrange

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
        if self.name == "Sheep" and hasattr(self, 'barbasi'):
            """ In the sheep selector model, we also need to initialise the barbasi selector """
            self.barbasi.set_platforms(platforms)

    def p_indices(self):
        """ Wrapper for lrange - self.platforms """
        indices = lrange(self.platforms)
        for i,p in enumerate(self.platforms):
            if not p.isActive():
                indices.remove(i)
        return indices

class Random(Selector):
    """ Selects an indice at random, w.r.t. given probabilities """

    def __init__(self, probabilities, growth=1):
        super().__init__(growth)
        self.name = "Random"
        self.ps = np.array(probabilities)
    
    def select(self):
        super().select()
        i = self.p_indices()
        return np.random.choice(i, p=self.ps[i]), self.n, 1

class Uniform(Selector):
    """ Uniformly selects an indice """

    def __init__(self, growth=1):
        super().__init__(growth)
        self.name = "Uniform"

    def select(self):
        super().select()

        return np.random.choice(self.p_indices()), self.n, 1
    
class Poisson(Selector):
    """ Selects an indice w.r.t. Poisson arrival process """

    def __init__(self, lambdas, growth=1):
        super().__init__(growth)
        self.name = "Poisson"
        self.ls = np.array(lambdas)

    def select(self):
        super().select()
        arrivals = [np.random.exponential(1/l) for l in self.ls[self.p_indices()]]
        return np.argmin(arrivals), self.n, min(arrivals)

class Barabasi(Selector):
    """ Selects the Platform w.r.t. to it's relative size """

    def __init__(self, growth=1):
        super().__init__(growth)
        self.name = "Barabasi"
    
    def get_platform_shares(self):
        platforms_shares = np.array([p.market_share[-1] for p in self.platforms if p.isActive()])
        return platforms_shares / np.sum(platforms_shares)

    def select(self):
        super().select()
        return np.random.choice(self.p_indices(), p=self.get_platform_shares()), self.n, 1

class Sheep(Selector):
    """ Selects a platform with the Barbasi model, but factoring in what the previous arrival did.

    To do this we add bias to the previously selected platform. For the biased probabilities
    to still add to 1, we need to remove some epsilon from the ther probabilities.
    This is the formula to do so:
        Ɛ = p * (b-1) / (n-1) 
            p = previously chosen market share
            b = bias factor (>1) for which we choose p
            n = number of platforms we're choosing from
    """


    def __init__(self, bias, growth=1):
        super().__init__(growth)
        if bias < 1:
            raise ValueError(f"expected bias value > 1, instead got {bias}.")
        self.name = "Sheep"
        self.barbasi = Barabasi()
        self.previous_platform = None
        self.bias = bias

    def select(self):
        super().select()
        if self.previous_platform is None:
            # Get barbasi selection the very first time
            choice, self.n, g = self.barbasi.select()
        else:
            # Get market shares from the barbasi model
            m_shares = self.barbasi.get_platform_shares()
            biased_shares = []
            # Set epsilon
            epsilon = m_shares[self.previous_platform] * (self.bias-1) / self.p_indices()[-1]
            bound = lambda x: min(1, max(0, x)) # Floats might lead to >1 or <0 
            # Add bias 
            for i, share in enumerate(m_shares):
                if i == self.previous_platform:
                    biased_shares.append(bound(self.bias * share))
                else:
                    biased_shares.append(bound(min(1, max(0, share - epsilon))))
            # Make new choice
            choice = np.random.choice(self.p_indices(), p=biased_shares)
        self.previous_platform = choice
        return choice, self.n, 1
