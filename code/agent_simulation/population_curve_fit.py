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
    parser.add_argument('--it', help='Number of iterations to get average', type=int, default=10)
    parser.add_argument('--mu_waiting', help='Number of values to search for mu_r', type=int, default=4)
    parser.add_argument('--mu_idle', help='Number of values to search for mu_d', type=int, default=4)
    parser.add_argument('--fixed', help='Which of the mu_waiting parameters to fix', type=int, default=0)
    args = parser.parse_args()

    names = ['Uber', 'Lyft', 'Other']

    # Extrapolate from given market-share values
    N = 1889
    data = np.loadtxt('../../raw/real/nyc_rhp_acc_rides.txt')
    data_rides = [
        midpoint_interpolation(data[0], N) + [data[0,-1]],
        midpoint_interpolation(data[1], N-95)[65:] + [data[1,-1]],
        midpoint_interpolation(data[2], N-95)[65:] + [data[2,-1]]
    ]

    # Define the parameters to search for
    mu_rs = np.linspace(0, 1, num=args.mu_waiting)
    mu_rs = np.delete(mu_rs, [0, args.mu_waiting-1])
    mu_ds = np.linspace(0, 1, num=args.mu_idle)
    mu_ds = np.delete(mu_ds, [0, args.mu_idle-1])

    # Assert that for each platform, the average of mu_waiting and mu_idle is not 'high'
    valid = lambda elements: all([np.mean([elements[i], elements[i+3]]) <= 0.6 for i in [0, 1, 2]])
    parameters = [[[a, b, c], [d, e, f]] for a in mu_rs for b in mu_rs for c in mu_rs for d in mu_ds for e in mu_ds for f in mu_ds if valid([a, b, c, d, e, f])]
    
    # Perform grid search
    scores = []
    best = None
    for mu_r, mu_d in tqdm(parameters):
        if mu_r[0] != mu_rs[args.fixed]:
            continue
        try:
            iter_rides = []
            city = City()
            # Run the simulation it times
            for _ in (range(args.it)):
                sim = AgentSimulator(N, names, rider_proportion=0.95,
                                    mu_D=mu_d, mu_R=mu_r, eta=[0, 0, 0],
                                    n_joins=1, delays=[0, 65, 65])
                # Store the returned data

                iter_rides.append(sim.run().get_riders() + sim.get_drivers())
            # Get means of winner / looser over the runs
            avg_rides = np.array([conf_interval(np.array(p), axis=0)[0] for p in zip(*iter_rides)])
            
            # Compute RMSE for half of the data
            rmse = []
            for true, pred in zip(data_rides, avg_rides):
                a = int(len(pred) * 0.7)
                rmse.append(np.sqrt(mean_squared_error(true[:a], pred[:a])))

            # Register score
            scores.append(mu_r + mu_d + rmse)
            if best is None:
                best = np.mean(rmse) + 1
            newBest = min(best, np.mean(rmse))
            if newBest != best:
                with open(f'70_pop_fit/rmse_output_fixed{args.fixed}.txt', 'a') as checkpoints:
                    checkpoints.write(f'New best: mu_r: {mu_r} | mu_d: {mu_d}\nRMSE: {rmse}\n\n')
                best = newBest
        except Exception as e:
            with open(f'70_pop_fit/rmse_output_fixed{args.fixed}.txt', 'a') as checkpoints:
                checkpoints.write(f'ERROR\nmu_r: {mu_r} | mu_d: {mu_d}\n{e}\n\n')
