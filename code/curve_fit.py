import argparse
import numpy as np
from tqdm import tqdm
from sklearn.metrics import mean_squared_error

np.random.seed(1_218_042)

from simulator import AgentSimulator
from utils import midpoint_interpolation, conf_interval

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--it', help='Number of iterations to get average', type=int, default=100)
    parser.add_argument('--mu_waiting', help='Number of values to search for mu_r', type=int, default=50)
    parser.add_argument('--mu_idle', help='Number of values to search for mu_d', type=int, default=50)
    parser.add_argument('--fixed', help='Which of the mu_waiting parameters to fix', type=int, default=0)
    args = parser.parse_args()

    names = ['Uber', 'Other']

    # Extrapolate from given market-share values
    N = 1889
    data = np.loadtxt('../raw/real/nyc_rhp_marketshare.txt')
    data_ms = [
        midpoint_interpolation(data[0], N) + [data[0,-1]],
        midpoint_interpolation(data[1], N-95)[65:] + [data[1,-1]],
        midpoint_interpolation(data[2], N-95)[65:] + [data[2,-1]]
    ]
    data_ms = [
        np.array(data_ms[0]),
        np.array(data_ms[1]) + np.array(data_ms[2]),
    ]
    
    # Define the parameters to search for
    mu_rs = np.linspace(0, 1, num=args.mu_waiting)
    mu_rs = np.delete(mu_rs, [0, args.mu_waiting-1])
    mu_ds = np.linspace(0, 1, num=args.mu_idle)
    mu_ds = np.delete(mu_ds, [0, args.mu_idle-1])

    # Assert that for each platform, the average of mu_waiting and mu_idle is not 'high'
    # valid = lambda elements: all([np.mean([elements[i], elements[i+3]]) <= 0.6 for i in [0, 1, 2]])
    valid = lambda elements: all([np.mean([elements[i], elements[i+2]]) <= 0.6 for i in [0, 1]])
    # parameters = [[[a, b, c], [d, e, f]] for a in mu_rs for b in mu_rs for c in mu_rs for d in mu_ds for e in mu_ds for f in mu_ds if valid([a, b, c, d, e, f])]
    parameters = [[[a, b], [c, d]] for a in mu_rs for b in mu_rs for c in mu_ds for d in mu_ds if valid([a, b, c, d])]

    # Perform grid search
    scores = []
    best = 1
    for mu_r, mu_d in tqdm(parameters):
        if mu_d[0] != mu_ds[args.fixed]:
            continue
        try:
            iter_ms = []
            city = City()
            # Run the simulation it times
            for _ in (range(args.it)):
                sim = AgentSimulator(N, names, rider_proportion=0.95,
                                    mu_D=mu_d, mu_R=mu_r, eta=[0, 0],
                                    n_joins=1, delays=[0, 65])
                # Store the returned data
                iter_ms.append(sim.run().get_market_shares())
            # Get means of winner / looser over the runs
            avg_ms = np.array([conf_interval(np.array(p), axis=0)[0] for p in zip(*iter_ms)])

            # Compute RMSE for half of the data
            rmse = []
            for true_ms, pred_ms in zip(data_ms, avg_ms):
                # a = int(len(true_ms) * 0.70)
                # true = true_ms[:a]
                # pred = pred_ms[:a]
                rmse.append(np.sqrt(mean_squared_error(true_ms, pred_ms)))
            # Register score
            scores.append(mu_r + mu_d + rmse)
            newBest = min(best, np.mean(rmse))
            if newBest != best:
                with open(f'txt_out/dual_full_conditional_txtoutput/rmse_output_fixed{args.fixed}.txt', 'a') as checkpoints:
                    checkpoints.write(f'New best: mu_r: {mu_r} | mu_d: {mu_d}\nRMSE: {rmse}\n\n')
                best = newBest
        except Exception as e:
            with open(f'txt_out/dual_full_conditional_txtoutput/rmse_output_fixed{args.fixed}.txt', 'a') as checkpoints:
                checkpoints.write(f'ERROR\nmu_r: {mu_r} | mu_d: {mu_d}\n{e}\n\n')

    np.savetxt(f'txt_out/dual_full_conditional_txtoutput/rmse_results_fixed{args.fixed}.txt', scores)



