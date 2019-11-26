import argparse
import logging

from utils import plot_market_share
from simulator import Simulator

if __name__ == "__main__":

  LOGGER = logging.getLogger(__name__)

  parser = argparse.ArgumentParser()
  parser.add_argument('--N', help="Population size to consider during the simulation.",     type=int, default=1_000)
  parser.add_argument('--P', help="Number of platforms to consider during the simulation.", type=int, default=2)
  parser.add_argument('--t', help="Duration of the simulation."                       ,     type=int, default=2_000)
  args = parser.parse_args()

  names = ['Uber', 'Black Cab']

  simulator = Simulator(args.N, names)
  market_shares = simulator.run(args.t).get_market_shares()
  plot_market_share(market_shares, args.t, args.N)