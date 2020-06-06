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
from base_simulation.utils import conf_interval


if __name__ == "__main__":

    LOGGER = logging.getLogger(__name__)

    arguments = {
        '--N': ["Population size to consider during the simulation.", int, 1_000],
        '--it': ["Number of iterations to get average.", int, 100],
        '--city': ["Flag to show the city as a grid of densities.", bool, False],
        '--c': ["Alpha factor for the lorenz scaling", float, 2],
        '--r': ["Proportion of rider agents generated by the simulation.", float, 0.95],
        '--n_joins': ["Number of agents that are released to the market at each iteration.", int, 1],
        '--mu_waiting': ["Sets mu_waiting or mu_idle", bool, True],
        '--base': ["Fixes base", float, 0.1]
    }

    parser = argparse.ArgumentParser()
    for arg, (_help, _type, _default) in arguments.items():
        parser.add_argument(arg, help=_help, type=_type, default=_default)
    args = parser.parse_args()

    names = ['Uber', 'Other']

    n = 50
    # Iterate through all possible delays
    delta_ms = np.zeros((n, n))
    for y, delay in tqdm(enumerate(list(range(0, args.N//2, 10))), total=n):
        # Iterate through all possible values of mu
        for x, mu in tqdm(enumerate(np.linspace(0, 1, num=n)), total=n):
            mu_r = [args.base, mu]        if args.mu_waiting else [args.base, args.base]
            mu_d = [args.base, args.base] if args.mu_waiting else [args.base, mu]

            iter_ms = []
            city = City()
            # Run the simulation it times
            for _ in range(args.it):
                sim = AgentSimulator(args.N, names, city_shape=city.density.shape,
                                    rider_proportion=args.r, lorenz=args.c,
                                    mu_D=mu_d, mu_R=mu_r, eta=[0, 0],
                                    n_joins=args.n_joins, delays=[0, delay])
                # Store the returned data
                iter_ms.append(sim.run().get_market_shares())
            # Get means of winner / looser over the runs
            _format = lambda d, i: np.array([conf_interval(np.array(p), axis=0)[i] for p in zip(*d)])
            avg_ms = _format(iter_ms, 0)
            delta_ms[-(y+1), x] = np.abs(avg_ms[0][-1] - avg_ms[1][-1])
    if args.mu_waiting:
        np.savetxt(f'heatmap_data/mu_waiting-{args.base}.txt', delta_ms)
    else:
        np.savetxt(f'heatmap_data/mu_idle-{args.base}.txt', delta_ms)
