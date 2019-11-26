
class Platform:
  """
  Platform representing a ride-sharing platform such as Uber or Kapten.
  Will be keeping track of its specific market share and XX
  """

  def __init__(self, platform_name, total_population, initial_size=0):
    """ Keyword arguments:
    initial_size -- Number of users in the platform at creation (Default 0)
    """
    self.name = platform_name
    
    self.market_share = [initial_size / total_population]
    self.total_population = total_population
    self.n_users = initial_size

  def update_market_share(self):
    self.market_share.append(self.n_users / self.total_population)

  def add_user(self, n):
    self.n_users += n
    self.update_market_share()

  def get_market_share(self, N):
    return (self.market_share, self.name)