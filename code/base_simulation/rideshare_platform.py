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
    self.population = 2
    self.users = 1
    self.market_share = [1/n_platforms]
    self.delta_t = None

  def set_avg_user(self, x, y):
    """ Sets the initial position of average user """
    self.average_user = np.array([np.random.randint(y), np.random.randint(x)])
  
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
    self.market_share.append(self.users / self.population)

  def update_avg_user(self, xy):
    """ Updates the location in space of the average user """
    n = self.users
    self.average_user = ((n-1) * self.average_user + xy) / n

  def add_user(self, n=1, delta_pop=1, position=None):
    self.users += n
    self.population += delta_pop
    # Decrese the remaining time until activation
    if self.delta_t is not None:
      self.delta_t -= 1
      # Once delta reached - activate the platform 
      if self.delta_t == 0:
        self.activate()
    self.update_market_share()

    if position is not None:
      self.update_avg_user(position)

  def get_market_share(self):
    return self.market_share