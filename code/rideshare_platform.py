
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

  def update_market_share(self):
    self.market_share.append(self.users / self.population)

  def add_user(self, n, delta_pop):
    self.users += n
    self.population += delta_pop
    self.update_market_share()

  def get_market_share(self):
    return self.market_share