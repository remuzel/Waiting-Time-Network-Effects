import numpy as np

class Platform:
    """
    Platform representing a ride-sharing platform such as Uber or Kapten.
    Will be keeping track of its specific market share and XX
    """

    def __init__(self, platform_name, n_platforms):
        """ Keyword arguments:
        initial_size -- Number of users in the platform at creation (Default 0)
        """
        self.name = platform_name
        self.r_population = n_platforms
        self.d_population = n_platforms
        self.population = 2 * n_platforms
        self.users = 1
        self.drivers = 1
        self.rider_history = [1]
        self.driver_history = [1]
        self.market_share = [1/n_platforms]
        self.d_market_share = [1/n_platforms]
        self.r_market_share = [1/n_platforms]
        self.delta_t = None

    def set_avg_user(self, x, y):
        """ Sets the initial position of average user """
        self.average_user = np.array([np.random.randint(y), np.random.randint(x)])

    def set_avg_driver(self, x, y):
        """ Sets the initial position of average user """
        self.average_driver = np.array([np.random.randint(y), np.random.randint(x)])

    def get_driver_history(self):
        """ Returns the driver history """
        return self.driver_history

    def get_rider_history(self):
        """ Returns the rider history """
        return self.rider_history

    def activate(self):
        """ Activates the ridesharing platform - allowing to receive new users """
        self.delta_t = None

    def deactivate(self, delta_t):
        """ Turns off the ridesharing platform - blocking it from receiving new users """
        self.delta_t = delta_t

    def isActive(self):
        """ Checks if the platform is active or currently dormant """
        return self.delta_t is None

    def update_market_share(self):
        self.market_share.append((self.users + self.drivers) / self.population)
        self.d_market_share.append(self.drivers/self.d_population)
        self.r_market_share.append(self.users/self.r_population)

    def update_avg_user(self, xy):
        """ Updates the location in space of the average user """
        n = self.users
        self.average_user = ((n-1) * self.average_user + xy) / n

    def update_avg_driver(self, xy):
        """ Updates the location in space of the average driver """
        n = self.drivers
        self.average_driver = ((n-1) * self.average_driver + xy) / n

    def add_user(self, position, n=1, delta_pop=1, driver=True):
        # Increment the corresponding user/driver count 
        if driver:
            self.drivers += n
            self.d_population += delta_pop
            self.update_avg_driver(position)
        else:
            self.users += n
            self.r_population += delta_pop
            self.update_avg_user(position)
        self.driver_history.append(self.drivers)
        self.rider_history.append(self.users)
        # Update the population & market shares
        self.population += delta_pop
        self.update_market_share()
        # Decrese the remaining time until activation
        if self.delta_t is not None:
            self.delta_t -= 1
        # Once delta reached - activate the platform 
        if self.delta_t == 0:
            self.activate()

    def get_market_share(self):
        return self.market_share

    def get_r_market_share(self):
        return self.r_market_share

    def get_d_market_share(self):
        return self.d_market_share