import __init__

import argparse
import logging
import numpy as np

np.random.seed(1_218_042)

if __name__ == "__main__":

  LOGGER = logging.getLogger(__name__)

  arguments = {
    '--N': ["Population size to consider during the simulation.", int, 1_000],
    '--P': ["Number of platforms to consider during the simulation.", int, 2],
    '--t': ["Duration of the simulation.", int, 1_000],
    '--it': ["Number of iterations to get average.", int, 1_000],
    '--plt': ["Filename underwich to save the figure.", str, None],
    '--city': ["Flag to show the city as a grid of densities.", bool, False],
    '--f': ["Attenuating factor to be used in size vs distance equation.", str, "lorenz"]
  }

  parser = argparse.ArgumentParser()
  for arg, (_help, _type, _default) in arguments.items():
    parser.add_argument(arg, help=_help, type=_type, default=_default)
  args = parser.parse_args()

  names = ['Uber', 'Black Cab', 'Bolt', 'Kapten', 'Heetch'][:args.P]