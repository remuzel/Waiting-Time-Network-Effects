from matplotlib import pyplot as plt
from numpy import linspace, std, mean, sqrt

def plot_market_share(market_shares, error, arrival_type, filename=None, ebar_r=10):
    """ Plots the different market shares w.r.t. to time. 

    Keyword arguments:
    filename -- name of the plot once saved (default None)
    """
    # Define the colors to use while plotting
    c = plt.cm.RdYlGn(linspace(0, 1, len(market_shares)))
    for i, market_share in enumerate(market_shares):
        # Plot the error bars (and the curve) in 10% opacity
        plt.errorbar(list(range(len(market_share))), market_share, yerr=error[i], errorevery=100, c=c[i], label=f"Platform {i+1}")
    # Plot description
    plt.xlabel('Time (t)')
    plt.ylabel('Market Share')
    plt.ylim(0,1)
    plt.title(f'Market share evaluation for {arrival_type} arrival')
    plt.legend()
    if filename is not None:
        plt.savefig(f'../figures/v1.3/{filename}', dpi=600)
    else:
        plt.show()

def lrange(L):
    """ Wrapper for a list - range - len call """
    return list(range(len(L)))

def conf_interval(data, axis=None):
    """ Computes the 95% confidence interval for the mean of the data """
    if axis is None:
        dev = 1.960 * std(data) / sqrt(len(data))
        return mean(data), dev
    else:
        dev = 1.960 * std(data, axis=axis) / sqrt(len(data))
        return mean(data, axis=axis), dev