import argparse
import logging

if __name__ == "__main__":

  LOGGER = logging.getLogger(__name__)

  parser = argparse.ArgumentParser()
  parser.add_argument('--N', help="Population size to consider during the simulation.", type=int, default=1_000)
  parser.add_argument('--t', help="Duration of the simulation."                       , type=int, default=1_000_000)
  args = parser.parse_args()
