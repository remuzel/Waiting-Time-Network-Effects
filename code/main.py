import argparse
import logging

from utils import plot_market_share
from simulator import Simulator
from selector import Random, Uniform, Poisson, Barabasi, Sheep

if __name__ == "__main__":

  LOGGER = logging.getLogger(__name__)

  parser = argparse.ArgumentParser()
  parser.add_argument('--N', help="Population size to consider during the simulation.",     type=int, default=1_000)
  parser.add_argument('--P', help="Number of platforms to consider during the simulation.", type=int, default=2)
  parser.add_argument('--t', help="Duration of the simulation."                       ,     type=int, default=1_000)
  args = parser.parse_args()

  names = ['Uber', 'Black Cab']
  selectors = [Random([0.7, 0.3]), Uniform(), Poisson([7, 3]), Barabasi(), Sheep(1.01)]
  for selector in selectors:
    print(f"Simulating for {selector.name} selection...")
    sim = Simulator(args.N, names, selector)
    market_shares = sim.run(args.t).get_market_shares()
    plot_market_share(market_shares, args.t, selector.name)
    print(f"...done", end='\n\n')