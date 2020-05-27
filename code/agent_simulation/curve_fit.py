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
    args = parser.parse_args()

    names = ['Uber', 'Lyft', 'Other']
    
    # Extrapolate from given market-share values
    N = 1025
    data_ms = [
        midpoint_interpolation([1., 0.82982488, 0.72347467, 0.67828489, 0.67600572], N)+[0.67600572],
        midpoint_interpolation([0.10885625, 0.1203821, 0.1825346, 0.21817421], N-257),
        midpoint_interpolation([0.06131887, 0.15614322, 0.1391805, 0.10582007], N-257)
    ]

    # Define the parameters to search for 
    mu_rs = np.linspace(0, 1, num=args.mu_waiting)
    mu_ds = np.linspace(0, 1, num=args.mu_idle)
    parameters = [[[a, b, c], [d, e, f]] for a in mu_rs for b in mu_rs for c in mu_rs for d in mu_ds for e in mu_ds for f in mu_ds]
    # Perform grid search
    scores = []
    best = 1
    for mu_r, mu_d in tqdm(parameters):
        iter_ms = []
        city = City()
        # Run the simulation it times
        for _ in tqdm(range(args.it)):
            sim = AgentSimulator(N, names, rider_proportion=0.95,
                                mu_D=mu_d, mu_R=mu_r, eta=[0, 0, 0],
                                n_joins=1, delays=[0, 257, 257])
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
            with open('rmse_output.txt', 'a') as checkpoints:
                checkpoints.write(f'New best: mu_r: {mu_r} | mu_d: {mu_d}\nRMSE: {rmse}\n\n')
            best = newBest
    np.savetxt('rmse_results.txt', scores)


        