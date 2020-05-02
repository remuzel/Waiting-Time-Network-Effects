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
from base_simulation.utils import plot_market_share, conf_interval, plot_heatmaps


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
        '--u': ["Proportion of users generated in the simulation.", float, 0.95],
        '--mu_r': ["Rate at which riders leave the platform.", float, 0.5],
        '--mu_d': ["Rate at which drivers leave the platform.", float, 0.5],
        '--raw': ["Flag to save the raw heatmap data.", bool, False]
    }

    parser = argparse.ArgumentParser()
    for arg, (_help, _type, _default) in arguments.items():
        parser.add_argument(arg, help=_help, type=_type, default=_default)
    args = parser.parse_args()

    names = ['Uber', 'Black Cab', 'Bolt', 'Kapten', 'Heetch'][:args.P]

    ####################################################
    # # FOR HEATMAP GENERATION
    # n = 100
    # mu = np.linspace(0, 1, num=n)
    # # Setting up the values
    # delta_market_share = np.zeros((n, n))
    # delta_total = np.zeros((n, n))
    # delta_drivers = np.zeros((n, n))
    # delta_riders = np.zeros((n, n))
    # delta_inner_1 = np.zeros((n, n))
    # delta_inner_2 = np.zeros((n, n))
    # for d, mu_d in tqdm(enumerate(mu), total=n):
    #     for r, mu_r in tqdm(enumerate(mu), total=n):
    ####################################################
    iter_ms = []
    iter_r = []
    iter_d = []
    city = City()
    # Run the simulation it times
    for i in tqdm(range(args.it)):
        sim = AgentSimulator(args.N, names, city_shape=city.density.shape,
                            rider_proportion=args.u, lorenz=args.c, mu_D=args.mu_d, mu_R=args.mu_r)
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
    ####################################################
            # delta_total[d, r] = np.abs((avg_r[0,-1] + avg_d[0,-1]) - (avg_r[1,-1] + avg_d[1,-1]))
            # delta_riders[d, r] = np.abs(avg_r[0,-1] - avg_r[1,-1])
            # delta_drivers[d, r] = np.abs(avg_d[0,-1] - avg_d[1,-1])
            # delta_market_share[d, r] = np.abs(avg_ms[0,-1] - avg_ms[1,-1])
            # delta_inner_1[d, r] = avg_r[0,-1] - avg_d[0,-1]
            # delta_inner_2[d, r] = avg_r[1,-1] - avg_d[1,-1]
    ####################################################
        
    # # Plot the results
    plot_market_share(data, "agent", filename=args.plt)

    # Plot the heatmaps
    # data = {
    #     'delta_t': delta_total,
    #     'delta_r': delta_riders,
    #     'delta_d': delta_drivers,
    #     'delta_ms': delta_market_share,
    #     'delta_i1': delta_inner_1,
    #     'delta_i2': delta_inner_2
    # }
    # plot_heatmaps(data, u=args.u, save=args.raw, it=args.it)