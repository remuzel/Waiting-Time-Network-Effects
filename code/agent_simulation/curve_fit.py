import argparse
import logging
import numpy as np
from tqdm import tqdm
from sklearn.metrics import mean_squared_error

np.random.seed(1_218_042)

from simulator import AgentSimulator

# Import some modules from the base simulator
import sys
sys.path.append("..")
from base_simulation.environment import City
from base_simulation.utils import midpoint_interpolation, conf_interval


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--it', help='Number of iterations to get average', type=int, default=100)
    parser.add_argument('--mu_waiting', help='Number of values to search for mu_r', type=int, default=50)
    parser.add_argument('--mu_idle', help='Number of values to search for mu_d', type=int, default=50)
    parser.add_argument('--fixed', help='Which of the mu_waiting parameters to fix', type=int, default=0)
    args = parser.parse_args()

    names = ['Uber', 'Lyft', 'Other']

    # Extrapolate from given market-share values
    N = 1889
    data = np.loadtxt('../../raw/rmse/nyc_rhp_marketshare.txt')
    data_ms = [
        midpoint_interpolation(data[0], N) + [data[0,-1]],
        midpoint_interpolation(data[1], N-95)[65:] + [data[1,-1]],
        midpoint_interpolation(data[2], N-95)[65:] + [data[2,-1]]
    ]

    # Define the parameters to search for
    mu_rs = np.linspace(0, 1, num=args.mu_waiting)
    mu_rs = np.delete(mu_rs, [0, args.mu_waiting-1])
    mu_ds = np.linspace(0, 1, num=args.mu_idle)
    mu_ds = np.delete(mu_ds, [0, args.mu_idle-1])

    parameters = [[[a, b, c], [d, e, f]] for a in mu_rs for b in mu_rs for c in mu_rs for d in mu_ds for e in mu_ds for f in mu_ds]
    # Perform grid search
    scores = []
    best = 1
    for mu_r, mu_d in tqdm(parameters):
        if mu_r != mu_rs[args.fixed]:
            continue
        try:
            iter_ms = []
            city = City()
            # Run the simulation it times
            for _ in (range(args.it)):
                sim = AgentSimulator(N, names, rider_proportion=0.95,
                                    mu_D=mu_d, mu_R=mu_r, eta=[0, 0, 0],
                                    n_joins=1, delays=[0, 65, 65])
                # Store the returned data
                iter_ms.append(sim.run().get_market_shares())
            # Get means of winner / looser over the runs
            avg_ms = np.array([conf_interval(np.array(p), axis=0)[0] for p in zip(*iter_ms)])

            # Compute RMSE
            rmse = [np.sqrt(mean_squared_error(true_ms, pred_ms)) for true_ms, pred_ms in zip(data_ms, avg_ms)]
            # Register score
            scores.append(mu_r + mu_d + rmse)
            newBest = min(best, np.mean(rmse))
            if newBest != best:
                with open(f'txtoutput/rmse_output_fixed{args.fixed}.txt', 'a') as checkpoints:
                    checkpoints.write(f'New best: mu_r: {mu_r} | mu_d: {mu_d}\nRMSE: {rmse}\n\n')
                best = newBest
        except:
            with open(f'txtoutput/rmse_output_fixed{args.fixed}.txt', 'a') as checkpoints:
                checkpoints.write(f'Failed to run simulation with:\nmu_r: {mu_r} | mu_d: {mu_d}\n\n')

    np.savetxt(f'txtoutput/rmse_results_fixed{args.fixed}.txt', scores)



