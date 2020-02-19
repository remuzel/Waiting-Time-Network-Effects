import numpy as np

class PopulationManager():
    """ This class handles the topology of a city and takes it into account
    (with given a platform market share) when yielding a new user
    """

    def __init__(self, density, factor, waiting_time_limit):
        # Map each value to its fraction of the total density
        self.density = density / density.sum()
        self.X_max = density.shape[1]
        self.Y_max = density.shape[0]
        self.m_d = np.sqrt(np.square(self.X_max) + np.square(self.Y_max))
        # Taking int account given market shares using the a scaled factor
        self.factor = {
            'lorenz': lambda ms: np.sqrt(1 - np.square(ms)),
            'exp': lambda ms: (np.exp(1) - np.exp(ms)) / (np.exp(1) - 1), 
            'tanh': lambda ms: (1/np.tanh(ms)) / (1/np.tanh(0.01)),
            'i_lorenz': lambda ms: np.square(1-np.sqrt(ms)),
            'cosh': lambda ms: 1/np.cosh(ms),
            'linear': lambda ms: 1 - ms
        }[factor]
        self.wtl = waiting_time_limit

    def sample_user(self, indices, average_users, market_shares=None):
        # Sample the position of a new user
        x = np.random.randint(self.X_max)
        y = np.random.randint(self.Y_max)
        n_user = np.array([y, x])
        # Compute the distance from this user to the average user of platforms
        distances = np.array([(1/np.linalg.norm(avg - n_user) if np.linalg.norm(avg - n_user) else self.m_d) for avg in average_users])
        # Normalise the distances (for them to be akin to probabilities)
        distances = distances / distances.sum()
        # Return the platform choice
        if market_shares is None:
            # With respect to the distances (only)
            return np.random.choice(indices, p=distances), n_user
        else:
            # Factor the market shares and normalise them
            factor = self.factor(market_shares)
            # Get the probability of joining each platform w.r.t. the factoring
            factor_eq = factor * market_shares + (1-factor) * distances
            return np.random.choice(indices, p=factor_eq/factor_eq.sum()), n_user