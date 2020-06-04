import seaborn as sb; sb.set()
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy import linspace, std, mean, sqrt, savetxt

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
        plt.title('Rider population growth')
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
        plt.title('Driver population growth')
        if filename is not None:
            plt.savefig(f'../../figures/{version}/driver_{filename}', dpi=600)
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

def plot_heatmaps(data, n=100, u=0.95, it='', save=False):
    version, u = "v6.4", int(u*100)
    # Retrieve the data
    delta_total = data['delta_t'][::-1][:n,-n:] if n != 100 else data['delta_t'][::-1]
    delta_drivers = data['delta_d'][::-1][:n,-n:] if n != 100 else data['delta_d'][::-1]
    delta_riders = data['delta_r'][::-1][:n,-n:] if n != 100 else data['delta_r'][::-1]
    delta_market_share = data['delta_ms'][::-1][:n,-n:] if n != 100 else data['delta_ms'][::-1]
    delta_inner_1 = data['delta_i1'][::-1][:n,-n:] if n != 100 else data['delta_i1'][::-1]
    delta_inner_2 = data['delta_i2'][::-1][:n,-n:] if n != 100 else data['delta_i2'][::-1]

    # Setting up the figure size
    fig = plt.figure(figsize=(24, 12))
    # Writing the ticks for the mu's
    ticks = [str(i/100) if i%10==0 else '' for i in range(0, n+1)]
    yticks = [str(i//2) if i%10==0 else '' for i in range(0, n+1)]

    ax = fig.add_subplot(2, 3, 1)
    # Plot the delta totals
    ax = sb.heatmap(delta_total, robust=True, cmap='hot', xticklabels=ticks, yticklabels=yticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between platform sizes (N=2)', size=15)

    ax = fig.add_subplot(2, 3, 2)
    # Plot the delta drivers
    ax = sb.heatmap(delta_drivers, robust=True, cmap='hot', xticklabels=ticks, yticklabels=yticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between number of drivers', size=15)

    ax = fig.add_subplot(2, 3, 3)
    # Plot the delta riders
    ax = sb.heatmap(delta_riders, robust=True, cmap='hot', xticklabels=ticks, yticklabels=yticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between number of riders', size=15)

    ax = fig.add_subplot(2, 3, 4)
    # Plot the difference in agents for platform 1
    ax = sb.heatmap(delta_market_share, robust=True, cmap='hot', xticklabels=ticks, yticklabels=yticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between platform market shares', size=15)

    ax = fig.add_subplot(2, 3, 5)
    # Plot the difference in agents for platform 1
    ax = sb.heatmap(delta_inner_1, robust=True, cmap='hot', xticklabels=ticks, yticklabels=yticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Surplus of riders for platform 1 (riders-drivers)', size=15)

    ax = fig.add_subplot(2, 3, 6)
    # Plot the difference in agents for platform 2
    ax = sb.heatmap(delta_inner_2, robust=True, cmap='hot', xticklabels=ticks, yticklabels=yticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Surplus of riders for platform 2 (riders-drivers)', size=15)

    # Show entire figure
    path = f'../../figures/{version}'
    Path(path).mkdir(parents=True, exist_ok=True)
    plt.savefig(f'{path}/heatmap{u}r-{it}-50d.png', dpi=150)

    # Save the raw data to text files
    if save:
        # Make sure the path exists
        path = f'../../raw/{version}/{u}r-50d'
        Path(path).mkdir(parents=True, exist_ok=True)
        # Save the data
        savetxt(f'{path}/total.txt', delta_total, fmt='%d')
        savetxt(f'{path}/drivers.txt', delta_drivers, fmt='%d')
        savetxt(f'{path}/riders.txt', delta_riders, fmt='%d')
        savetxt(f'{path}/marketshare.txt', delta_market_share, fmt='%.2f')
        savetxt(f'{path}/plt1.txt', delta_inner_1, fmt='%d')
        savetxt(f'{path}/plt2.txt', delta_inner_2, fmt='%d')
