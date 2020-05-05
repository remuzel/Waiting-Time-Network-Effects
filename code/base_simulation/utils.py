import seaborn as sb; sb.set()
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy import linspace, std, mean, sqrt, savetxt

def plot_market_share(data, arrival_type, N, r, filename=None, ebar_r=10, _type=3):
    """ Plots the different market shares w.r.t. to time.

    Keyword arguments:
    filename -- name of the plot once saved (default None)
    """
    # Get arguments
    version = "v6.3"
    market_shares, error = data['avg_ms'], data['std_ms']
    n_riders, r_error = data['avg_r'], data['std_r']
    n_drivers, d_error = data['avg_d'], data['std_d']

    # Define the colors to use while plotting
    c = plt.cm.RdYlGn(linspace(0, 1, len(market_shares)))

    if _type in [1, 3]:
        # Plot the market share evolution
        for i, market_share in enumerate(market_shares):
            # Plot the error bars (and the curve) in 10% opacity
            plt.errorbar(lrange(market_share), market_share, yerr=error[i], errorevery=100, c=c[i], label=f"Platform {i+1}")
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
        fig, r_ax = plt.subplots()
        r_ax.set_xlabel('Time (t)')
        r_ax.set_ylabel('Riders')
        r_ax.set_ylim(0, int(N*r+sqrt(N*r*(1-r))))
        #r_ax.set_yscale('log')
        plots = []
        # Plot the rider population evolution
        for i, _r in enumerate(n_riders):
            plots.append(r_ax.errorbar(lrange(_r), _r, fmt='^-b', markevery=100, yerr=r_error[i], errorevery=100, c=c[i]))
        plt.grid(False)
        d_ax = r_ax.twinx()
        d_ax.set_ylabel('Drivers')
        d_ax.set_ylim(0, int(N*(1-r)+sqrt(N*r*(1-r))))
        #d_ax.set_yscale('log')
        # Plot the driver population evolution
        for i, _d in enumerate(n_drivers):
            plots.append(d_ax.errorbar(lrange(_d), _d, fmt='s-k', markevery=100, yerr=d_error[i], errorevery=100, c=c[i]))

        lines = [
            Line2D([0], [0], color='blue', linestyle='-', marker='^'),
            Line2D([0], [0], color='black', linestyle='-', marker='s')
        ]
        labels = ["Riders", "Drivers"]
        plt.legend(lines, labels)
        plt.grid(False)
        plt.title(f'Agent population evolution for {arrival_type} growth')
        if filename is not None:
            plt.savefig(f'../../figures/{version}/population_{filename}', dpi=600)
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



def plot_heatmaps(data, n=100, u=0.95, it='', save=False):
    version, u = "v6.3", int(u*100)
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

    ax = fig.add_subplot(2, 3, 1)
    # Plot the delta totals
    ax = sb.heatmap(delta_total, robust=True, cmap='hot', xticklabels=ticks, yticklabels=ticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between platform sizes (N=2)', size=15)

    ax = fig.add_subplot(2, 3, 2)
    # Plot the delta drivers
    ax = sb.heatmap(delta_drivers, robust=True, cmap='hot', xticklabels=ticks, yticklabels=ticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between number of drivers', size=15)

    ax = fig.add_subplot(2, 3, 3)
    # Plot the delta riders
    ax = sb.heatmap(delta_riders, robust=True, cmap='hot', xticklabels=ticks, yticklabels=ticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between number of riders', size=15)

    ax = fig.add_subplot(2, 3, 4)
    # Plot the difference in agents for platform 1
    ax = sb.heatmap(delta_market_share, robust=True, cmap='hot', xticklabels=ticks, yticklabels=ticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Absolute difference between platform market shares', size=15)

    ax = fig.add_subplot(2, 3, 5)
    # Plot the difference in agents for platform 1
    ax = sb.heatmap(delta_inner_1, robust=True, cmap='hot', xticklabels=ticks, yticklabels=ticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Surplus of riders for platform 1 (riders-drivers)', size=15)

    ax = fig.add_subplot(2, 3, 6)
    # Plot the difference in agents for platform 2
    ax = sb.heatmap(delta_inner_2, robust=True, cmap='hot', xticklabels=ticks, yticklabels=ticks[::-1])
    # Set labels and title
    ax.set_xlabel('mu_waiting', size=12)
    ax.set_ylabel('mu_idle', size=12)
    plt.tight_layout()
    plt.title('Surplus of riders for platform 2 (riders-drivers)', size=15)

    # Show entire figure
    path = f'../../figures/{version}'
    Path(path).mkdir(parents=True, exist_ok=True)
    plt.savefig(f'{path}/heatmap{u}r-{it}.png', dpi=150)

    # Save the raw data to text files
    if save:
        # Make sure the path exists
        path = f'../../raw/{version}/{u}r'
        Path(path).mkdir(parents=True, exist_ok=True)
        # Save the data
        savetxt(f'{path}/total.txt', delta_total, fmt='%d')
        savetxt(f'{path}/drivers.txt', delta_drivers, fmt='%d')
        savetxt(f'{path}/riders.txt', delta_riders, fmt='%d')
        savetxt(f'{path}/marketshare.txt', delta_market_share, fmt='%.2f')
        savetxt(f'{path}/plt1.txt', delta_inner_1, fmt='%d')
        savetxt(f'{path}/plt2.txt', delta_inner_2, fmt='%d')
