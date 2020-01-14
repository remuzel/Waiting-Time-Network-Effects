import numpy as np

class PopulationManager():
    """ This class handles the topology of a city and takes it into account
    (with given a platform market share) when yielding a new user
    """

    def __init__(self, density):
        # Map each value to its fraction of the total density
        self.density = density / density.sum()
        self.X_max = density.shape[1]
        self.Y_max = density.shape[0]

    def sample_user(self, indices, market_shares, average_users):
        # Sample the position of a new user
        x = np.random.randint(self.X_max)
        y = np.random.randint(self.Y_max)
        n_user = np.array([x, y])
        # Compute the distance from this user to the average user of platforms
        distances = np.array([np.linalg.norm(avg - n_user) for avg in average_users])
        # Make them a probability
        distances = distances / distances.sum()
        # Return the platform choice
        return np.random.choice(indices, p=np.mean([distances, market_shares], axis=0))