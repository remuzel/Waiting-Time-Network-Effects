import numpy as np

class Platform:
    """
    Platform representing a ride-sharing platform such as Uber or Kapten.
    Will be keeping track of its specific market share and XX
    """

    def __init__(self, platform_name, r_pop=1, d_pop=1):
        self.name = platform_name
        # Set information about market population
        self.r_population = r_pop
        self.d_population = d_pop
        self.population = r_pop + d_pop
        # Initialise with platform's base agents
        self.riders = 1
        self.drivers = 1
        self.users = 2
        self.rider_history = [1]
        self.driver_history = [1]
        self.market_share = [self.users/(d_pop+r_pop)]
        self.d_market_share = [self.drivers/d_pop]
        self.r_market_share = [self.riders/r_pop]

    def get_driver_history(self):
        """ Returns the driver history """
        return self.driver_history

    def get_rider_history(self):
        """ Returns the rider history """
        return self.rider_history

    def update_market_share(self):
        self.market_share.append((self.riders + self.drivers) / self.population)
        self.d_market_share.append(self.drivers/self.d_population)
        self.r_market_share.append(self.riders/self.r_population)

    def add_user(self, n=1, delta_pop=1, driver=True):
        # Increment the corresponding user/driver count 
        if driver:
            self.drivers += n
            self.d_population += delta_pop
        else:
            self.riders += n
            self.r_population += delta_pop
        self.driver_history.append(self.drivers)
        self.rider_history.append(self.riders)
        # Update the population & market shares
        self.population += delta_pop
        self.update_market_share()

    def get_market_share(self):
        return self.market_share

    def get_r_market_share(self):
        return self.r_market_share

    def get_d_market_share(self):
        return self.d_market_share