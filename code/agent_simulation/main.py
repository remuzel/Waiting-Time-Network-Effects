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
        '--c': ["Alpha factor for the lorenz scaling", float, 2],
        '--u': ["Proportion of users generated in the simulation.", float, 0.95]
    }

    parser = argparse.ArgumentParser()
    for arg, (_help, _type, _default) in arguments.items():
        parser.add_argument(arg, help=_help, type=_type, default=_default)
    args = parser.parse_args()

    names = ['Uber', 'Black Cab', 'Bolt', 'Kapten', 'Heetch'][:args.P]

    iter_ms = []
    iter_r = []
    iter_d = []
    city = City()
    # Run the simulation it times
    for i in tqdm(range(args.it)):
        sim = AgentSimulator(args.N, names, city_shape=city.density.shape,
                            rider_proportion=args.u, lorenz=args.c)
        # Sort the returned shares and agent numbers (who the winner is doesn't matter)
        m_shares = sorted(sim.run().get_market_shares(), key=lambda x: x[-1])
        riders = sorted(sim.get_riders(), key=lambda x: x[-1])
        drivers = sorted(sim.get_drivers(), key=lambda x: x[-1])
        # Store the data
        iter_ms.append(m_shares)
        iter_r.append(riders)
        iter_d.append(drivers)
    # Get means of winner / looser over the runs
    _format = lambda d, i: np.array([conf_interval(np.array(p), axis=0)[i] for p in zip(*d)])
    avg_ms, avg_r, avg_d = _format(iter_ms, 0), _format(iter_r, 0), _format(iter_d, 0)
    std_ms, std_r, std_d = _format(iter_ms, 1), _format(iter_r, 1), _format(iter_d, 1)
    data = {
        "avg_ms": avg_ms,
        "std_ms": std_ms,
        "avg_r": avg_r,
        "std_r": std_r,
        "avg_d": avg_d,
        "std_d": std_d
    }
    
    # Plot the res////ults
    plot_market_share(data, "agent", filename=args.plt)