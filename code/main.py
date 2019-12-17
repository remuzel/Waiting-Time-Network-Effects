import argparse
import logging
import numpy as np

from tqdm import tqdm
from utils import plot_market_share
from simulator import Simulator
from selector import Random, Uniform, Poisson, Barabasi, Sheep

if __name__ == "__main__":

  LOGGER = logging.getLogger(__name__)

  parser = argparse.ArgumentParser()
  parser.add_argument('--N',   help="Population size to consider during the simulation.",     type=int, default=1_000)
  parser.add_argument('--P',   help="Number of platforms to consider during the simulation.", type=int, default=2)
  parser.add_argument('--t',   help="Duration of the simulation."         ,                   type=int, default=1_000)
  parser.add_argument('--it',  help="Number of iterations to get average.",                   type=int, default=1_000)
  parser.add_argument('--plt', help="Filename underwich to save the figure.",                 type=str, default=None)
  args = parser.parse_args()

  names = ['Uber', 'Black Cab', 'Bolt', 'Kapten', 'Heetch'][:args.P]
  n = len(names)
  selector= Barabasi()
  # Setup average platform share tracker
  platform_shares = []
  print(f"Simulating for {selector.name} selection...")
  iter_ms = []
  # Run simulation it times for each t 
  for i in tqdm(range(args.it)):
    sim = Simulator(args.N, names, selector)
    # Sort the returned shares (who the winner is doesn't matter)
    m_shares = sorted(sim.run(args.t).get_market_shares(), key=lambda x: x[-1])
    # Store the shares
    iter_ms.append(m_shares)
  print(f"...done", end='\n\n')
  # Get means of winner / looser over the runs
  avg = np.array([np.mean(np.array(platform), axis=0) for platform in zip(*iter_ms)])
  std = np.array([np.std(np.array(platform), axis=0) for platform in zip(*iter_ms)])

  plt = None
  if args.plt is not None:
    plt = f"{len(names)}plt-{args.plt}-{selector.name}-{args.t}s-{args.it}it.png"
  plot_market_share(avg, std, selector.name, filename=plt)