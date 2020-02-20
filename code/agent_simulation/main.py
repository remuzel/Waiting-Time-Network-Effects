import argparse
import logging
import numpy as np
from tqdm import tqdm

np.random.seed(1_218_042)

from simulator import AgentSimulator

# Import some modules from the base simulator
import sys
sys.path.append("..")
from base_simulation.environment import City
from base_simulation.utils import plot_market_share, conf_interval


if __name__ == "__main__":

    LOGGER = logging.getLogger(__name__)

    arguments = {
    '--N': ["Population size to consider during the simulation.", int, 1_000],
    '--P': ["Number of platforms to consider during the simulation.", int, 2],
    '--t': ["Duration of the simulation.", int, 1_000],
    '--it': ["Number of iterations to get average.", int, 1_000],
    '--plt': ["Filename underwich to save the figure.", str, None],
    '--city': ["Flag to show the city as a grid of densities.", bool, False],
    '--f': ["Attenuating factor to be used in size vs distance equation.", str, "lorenz"],
    '--c': ["Alpha factor for the lorenz scaling", float, 2]
    }

    parser = argparse.ArgumentParser()
    for arg, (_help, _type, _default) in arguments.items():
        parser.add_argument(arg, help=_help, type=_type, default=_default)
    args = parser.parse_args()

    names = ['Uber', 'Black Cab', 'Bolt', 'Kapten', 'Heetch'][:args.P]

    iter_ms = []
    city = City()
    # Run the simulation it times
    for i in tqdm(range(args.it)):
        sim = AgentSimulator(args.N, names, city_shape=city.density.shape, lorenz=args.c)
        # Sort the returned shares (who the winner is doesn't matter)
        m_shares = sorted(sim.run().get_market_shares(), key=lambda x: x[-1])
        # Store the shares
        iter_ms.append(m_shares)
    # Get means of winner / looser over the runs
    avg = np.array([conf_interval(np.array(platform), axis=0)[0] for platform in zip(*iter_ms)])
    std = np.array([conf_interval(np.array(platform), axis=0)[1] for platform in zip(*iter_ms)])

    # Plot the results
    plot_market_share(avg, std, "agent", filename=None)