from matplotlib import pyplot as plt

def plot_market_share(market_shares, t, N, filename=None):
    """ Plots the different market shares w.r.t. to time. 

    Keyword arguments:
    filename -- name of the plot once saved (default None)
    """
    for market_share in market_shares:
        plt.plot(list(range(t)), market_share[0][:t], label=market_share[1])
    
    plt.xlabel('Time (t)')
    plt.ylabel('Market Share')
    plt.title(f'Market share evaluation for population of size {N}')
    plt.legend()
    if filename is not None:
        plt.savefig(f'../figures/{filename}')
    plt.show()
