import numpy as np

class Selector:
    """ Parent class for all random selectors """
    def __init__(self, growth=1):
        self.n = growth

    def select(self, indices):
        """ Given indices to choose from will return one of them
        w.r.t. the specific method.
        Will always return a tuple:
            (index, growth_amount, time_taken)
        """
        # do nothing
        pass

class Random(Selector):
    """ Selects an indice at random, w.r.t. given probabilities """

    def __init__(self, probabilities, growth=1):
        super().__init__(growth)
        self.name = "Random"
        self.ps = probabilities
    
    def select(self, indices):
        super().select(indices)

        return np.random.choice(indices, p=self.ps), self.n, 1

class Uniform(Selector):
    """ Uniformly selects an indice """

    def __init__(self, growth=1):
        super().__init__(growth)
        self.name = "Uniform"

    def select(self, indices):
        super().select(indices)

        return np.random.choice(indices), self.n, 1
    
class Poisson(Selector):
    """ Selects an indice w.r.t. Poisson arrival process """

    def __init__(self, lambdas, growth=1):
        super().__init__(growth)
        self.name = "Poisson"
        self.ls = lambdas

    def select(self, indices):
        super().select(indices)
        arrivals = [np.random.exponential(1/l) for l in self.ls]
        return np.argmin(arrivals), self.n, min(arrivals)