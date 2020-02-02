import numpy as np

class PopulationManager():
    """ This class handles the topology of a city and takes it into account
    (with given a platform market share) when yielding a new user
    """

    def __init__(self, density, waiting_time_limit):
        # Map each value to its fraction of the total density
        self.density = density / density.sum()
        self.X_max = density.shape[1]
        self.Y_max = density.shape[0]
        self.wtl = waiting_time_limit

    def sample_user(self, indices, average_users, market_shares=None):
        # Sample the position of a new user
        x = np.random.randint(self.X_max)
        y = np.random.randint(self.Y_max)
        n_user = np.array([y, x])
        # Compute the distance from this user to the average user of platforms
        distances = np.array([max(self.wtl, np.linalg.norm(avg - n_user)) for avg in average_users])
        # Make distances probabilities, by making the smallest distance the most likely
        distances = distances / distances.sum()
        distances = 1 - distances
        distances = distances / distances.sum()
        # Return the platform choice
        if market_shares is None:
            # With respect to the distances (only)
            return np.random.choice(indices, p=distances), n_user
        else:
            # Taking int account given market shares
            return np.random.choice(indices, p=np.mean([distances, market_shares], axis=0)), n_user