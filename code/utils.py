from matplotlib import pyplot as plt

def plot_market_share(market_shares, error, arrival_type, filename=None, ebar_r=10):
    """ Plots the different market shares w.r.t. to time. 

    Keyword arguments:
    filename -- name of the plot once saved (default None)
    """
    c = ['Orange'] * len(market_shares)
    c[0] = 'Red'
    c[-1] = 'Green'
    for i, market_share in enumerate(market_shares):
        # Plot the error bars (and the curve) in 10% opacity
        plt.errorbar(list(range(len(market_share))), market_share, yerr=error[i], alpha=0.1, c=c[i])
        # Plot the curve a 2nd time to make it visible
        plt.plot(list(range(len(market_share))), market_share, label=f"Platform {i+1}", c=c[i])
    # Plot description
    plt.xlabel('Time (t)')
    plt.ylabel('Market Share')
    plt.ylim(0,1)
    plt.title(f'Market share evaluation for {arrival_type} arrival')
    plt.legend()
    if filename is not None:
        plt.savefig(f'../figures/v1.1/{filename}')
    else:
        plt.show()
