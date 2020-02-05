import argparse
import logging
import numpy as np

from tqdm import tqdm
from utils import plot_market_share, conf_interval
from simulator import Simulator
from environment import City
from population import PopulationManager
from selector import Random, Uniform, Poisson, Barabasi, Density, DensityBarabasi, Sheep

VERSION = "v1.4"

if __name__ == "__main__":

  LOGGER = logging.getLogger(__name__)

  parser = argparse.ArgumentParser()
  parser.add_argument('--N',     help="Population size to consider during the simulation.",                 type=int,   default=1_000)
  parser.add_argument('--P',     help="Number of platforms to consider during the simulation.",             type=int,   default=2)
  parser.add_argument('--t',     help="Duration of the simulation."         ,                               type=int,   default=1_000)
  parser.add_argument('--it',    help="Number of iterations to get average.",                               type=int,   default=1_000)
  parser.add_argument('--plt',   help="Filename underwich to save the figure.",                             type=str,   default=None)
  parser.add_argument('--delta', help="Adds a delay (%% of t) to the market entrance of the 1st platform.", type=float, default=0)
  parser.add_argument('--city',  help="Flag to show the city as a grid of densities.",                      type=bool,  default=False)
  parser.add_argument('--wtl',   help="Integer representing the waiting time limit for platforms.",         type=int,   default=0)
  args = parser.parse_args()

  names = ['Uber', 'Black Cab', 'Bolt', 'Kapten', 'Heetch'][:args.P]
  #######################################
  # FOR ∆TIME - ∆MS EVALUATION          # 
  # deltas = []
  # delta_e = []
  # ds = np.linspace(0, 1, 1000)[1:151]
  # for d in ds:
  #   delta_t = [(0, int(d * args.t))] 
  #   print(f"Delta is {delta_t}")
  #######################################
  # FOR ∆WTL - ∆MS EVALUATION           #
  # wtls = np.arange(10, 501, step=10)
  # avg_delta = []
  # std_delta = []
  # for wtl in tqdm(wtls):
  #######################################

  # Setup the selector
  city = City()
  pop_manager = PopulationManager(city.density, args.wtl)
  selector = DensityBarabasi(pop_manager)
  # Define the ∆t of platform start
  delta_t = int(args.delta/100 * args.t)
  # Setup average platform share tracker
  platform_shares = []
  # print(f"Simulating for {selector.name} selection...")
  iter_ms = []
  # Run simulation it times for each t 
  for i in tqdm(range(args.it)):
    sim = Simulator(args.N, names, selector, [(0, delta_t)] if args.delta else [])
    # Sort the returned shares (who the winner is doesn't matter)
    m_shares = sorted(sim.run(args.t).get_market_shares(), key=lambda x: x[-1])
    # Store the shares
    iter_ms.append(m_shares)
  # print(f"...done", end='\n\n')
  # Get means of winner / looser over the runs
  avg = np.array([conf_interval(np.array(platform), axis=0)[0] for platform in zip(*iter_ms)])
  std = np.array([conf_interval(np.array(platform), axis=0)[1] for platform in zip(*iter_ms)])


  #######################################
  # FOR ∆WTL - ∆MS EVALUATION
  #   # Append the average diff between the largest and smallest platform
  #   avg_delta.append(np.mean(avg[-1] - avg[0]))
  #   std_delta.append(np.mean(avg[-1] - avg[0]))
  # from matplotlib import pyplot as plt
  # plt.errorbar(wtls, avg_delta, yerr=std_delta, c='black')
  # plt.xlabel('∆wtl')
  # plt.ylabel('∆market-share')
  # plt.title('Impact of waiting time limit on the market')
  # plt.show()
  #######################################
  # FOR ∆TIME - ∆MS EVALUATION     
  #   # Compute the average and errors in time      
  #   t_deltas = np.array([[p[-1] for p in platform] for platform in zip(*iter_ms)])
  #   e_deltas = np.array([conf_interval(delta)[1] for delta in t_deltas])
  #   t_deltas = np.array([np.mean(delta) for delta in t_deltas])
  #   deltas.append(t_deltas[1] - t_deltas[0])
  #   delta_e.append(e_deltas[0])
  # from matplotlib import pyplot as plt
  # plt.errorbar(ds, deltas, yerr=delta_e, c='black')
  # plt.xlabel('∆time (in % of total time)')
  # plt.ylabel('∆market-share')
  # plt.title('Impact of late arrival to the market')
  # plt.show()
  #######################################
  # Show the cities density
  if args.city:
    city.show()
    # from matplotlib import pyplot as plt
    # c = plt.cm.RdYlGn(np.linspace(0, 1, len(sim.platforms)))
    # city.show(positions=[(p.average_user, c[i]) for i,p in enumerate(sim.platforms)])

  plt = None
  if args.plt is not None:
    plt = f"{len(names)}plt-{args.plt}-{selector.name}-{args.t:_}s-{args.it:_}it.png"
  plot_market_share(avg, std, selector.name, filename=plt)