from numpy import std, mean, sqrt
from matplotlib import pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def plot_market_share(data, arrival_type, N, r, filename=None, ebar_r=10, _type=3, delays=None):
    """ Plots the different market shares w.r.t. to time.

    Keyword arguments:
    filename -- name of the plot once saved (default None)
    """
    # Get arguments
    version = "v6.4"
    market_shares, error = data['avg_ms'], data['std_ms']
    n_riders, r_error = data['avg_r'], data['std_r']
    n_drivers, d_error = data['avg_d'], data['std_d']

    if _type in [1, 3]:
        # Plot the market share evolution
        for i, market_share in enumerate(market_shares):
            # Get the correct xs plot wrt delay
            xs = list(range(N+1))[-len(market_share):]
            # Plot the error bars (and the curve) in 10% opacity
            plt.errorbar(xs, market_share, yerr=error[i], errorevery=100, label=f"Platform {i+1}")
        # Plot untapped market
        untapped = []
        for i in range(N+1):
            unt = 1
            for p_index, delay in enumerate(delays):
                unt -= market_shares[p_index][i-delay] if i >= delay else 0
            untapped.append(unt)
        plt.plot(list(range(N+1)), untapped, c='k', ls='--', lw=1, label="Untapped Market")
        # Plot description
        plt.xlabel('Time (t)')
        plt.ylabel('Market Share')
        plt.ylim(0,1)
        plt.title(f'Market share evaluation for {arrival_type} growth')
        plt.legend()
        if filename is not None:
            plt.savefig(f'../../figures/{version}/{filename}', dpi=600)
        else:
            plt.show()

    if _type in [2, 3]:
        for i, _r in enumerate(n_riders):
            xs = list(range(N+1))[-len(_r):]
            plt.plot(xs, _r, label=f'Platform {i+1}')
        plt.legend()
        plt.xlabel('time (t)', size=12)
        plt.xscale('log')
        plt.ylabel('rider population', size=12)
        plt.yscale('log')
        plt.title('Rider population growth', size=15)
        if filename is not None:
            plt.savefig(f'../../figures/{version}/rider_{filename}', dpi=600)
        else:
            plt.show()

        for i, _d in enumerate(n_drivers):
            xs = list(range(N+1))[-len(_d):]
            plt.plot(xs, _d, label=f'Platform {i+1}')
        plt.legend()
        plt.xlabel('time (t)', size=12)
        plt.xscale('log')
        plt.ylabel('driver population', size=12)
        plt.yscale('log')
        plt.title('Driver population growth', size=15)
        if filename is not None:
            plt.savefig(f'../../figures/{version}/driver_{filename}', dpi=600)
        else:
            plt.show()

        for i, (_r, _d) in enumerate(zip(n_riders, n_drivers)):
            _t = _r + _d
            xs = list(range(N+1))[-len(_t):]
            plt.plot(xs, _t, label=f'Platform {i+1}')
        plt.legend()
        plt.xlabel('time (t)', size=12)
        plt.ylabel('total population', size=12)
        plt.yscale('log')
        plt.title('RHP users population growth', size=15)
        if filename is not None:
            plt.savefig(f'../../figures/{version}/total_{filename}', dpi=600)
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

def shift(values):
    """ Shifts values from [-a, b] to [a, b+2a] """
    if values.min() < 0:
        values -= 2*values.min()
    return values

def midpoint_interpolation(data, min_length):
    while len(data) < min_length:
        new_data = []
        for i,d in enumerate(data[:-1]):
            new_data.append(d)
            new_data.append((d+data[i+1])/2)
        data = new_data + [data[-1]]
    return data
