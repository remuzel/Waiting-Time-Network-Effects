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

    names = ['Lyft']

    # Extrapolate from given market-share values
    N = 1889
    data = np.loadtxt('../../raw/real/nyc_rhp_acc_rides.txt')
    data_rides = [
        midpoint_interpolation(data[0], N) + [data[0,-1]],
        midpoint_interpolation(data[1], N-95)[65:] + [data[1,-1]],
        midpoint_interpolation(data[2], N-95)[65:] + [data[2,-1]]
    ]

    # Extrapolate from the Lyft quarterly values
    N = 961
    data_riders = midpoint_interpolation([3.5, 4.5, 5.7, 6.6, 8.1, 9.4, 11.4, 12.6, 14, 15.5, 17.4, 18.6, 20.5, 21.8, 22.314, 22.9], N)
    data_drivers = midpoint_interpolation([0.31, 0.44, 0.57, 0.7, 0.84, 0.98, 1.12, 1.26, 1.4, 1.52, 1.64, 1.76, 1.88, 2.01, 2.14, 2.27], N)

    # Define the parameters to search for
    mu_rs = np.linspace(0, 1, num=args.mu_waiting)
    mu_rs = np.delete(mu_rs, [0, args.mu_waiting-1])
    mu_ds = np.linspace(0, 1, num=args.mu_idle)
    mu_ds = np.delete(mu_ds, [0, args.mu_idle-1])

    # Assert that for each platform, the average of mu_waiting and mu_idle is not 'high'
    # valid = lambda elements: all([np.mean([elements[i], elements[i+3]]) <= 0.6 for i in [0, 1, 2]])
    # parameters = [[[a, b, c], [d, e, f]] for a in mu_rs for b in mu_rs for c in mu_rs for d in mu_ds for e in mu_ds for f in mu_ds if valid([a, b, c, d, e, f])]
    parameters = [[a], [b] for a in mu_rs for b in mu_ds if np.mean([a, b]) <= 0.6]
    # Perform grid search
    scores = []
    best = None
    for mu_r, mu_d in tqdm(parameters):
        # if mu_r[0] != mu_rs[args.fixed]:
        #     continue
        try:
            iter_riders = []
            iter_drivers = []
            city = City()
            # Run the simulation it times
            for _ in (range(args.it)):
                sim = AgentSimulator(N, names, rider_proportion=0.95,
                                    mu_D=mu_d, mu_R=mu_r, eta=[0],
                                    n_joins=1, delays=[0])
                # Store the returned data

                iter_riders.append(sim.run().get_riders())
                iter_drivers.append(sim.get_drivers())
            # Get means of winner / looser over the runs
            avg_riders = np.array([conf_interval(np.array(p), axis=0)[0] for p in zip(*iter_riders)])
            avg_drivers = np.array([conf_interval(np.array(p), axis=0)[0] for p in zip(*iter_drivers)])
            
            a, b = min(avg_riders), max(avg_riders)
            c, d = min(data_riders), max(data_riders)
            avg_drivers = (((avg_riders - a) / (b-a)) * (d-c)) + c

            a, b = min(avg_drivers), max(avg_drivers)
            c, d = min(data_drivers), max(data_drivers)
            avg_drivers = (((avg_drivers - a) / (b-a)) * (d-c)) + c

            # Compute RMSE for half of the data
            a = int(len(data_riders) * 0.7)
            rmse = np.sqrt(mean_squared_error(data_riders[:a], avg_riders[:a])) + np.sqrt(mean_squared_error(data_drivers[:a], avg_drivers[:a]))

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

    np.savetxt(f'70_pop_fit/rmse_results_fixed{args.fixed}.txt', scores)



