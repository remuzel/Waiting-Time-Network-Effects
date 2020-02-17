import numpy as np
from matplotlib import pyplot as plt

lorenz = lambda ms: np.sqrt(1-np.square(ms))
softmax = lambda ms: np.exp(1)-np.exp(ms)
tanh = lambda ms: 1/np.tanh(ms) - 1/np.tanh(1)
i_lorenz = lambda ms: np.square(1-np.sqrt(ms))
cosh = lambda ms: 1/np.cosh(ms)
lin = lambda ms: 1-ms

n = 100
xs = np.delete(np.linspace(0, 1, num=n), [0, n-1])

fs = [lorenz, cosh, softmax, lin, i_lorenz, tanh]
name = ["Lorenz: √(1-m^2)", "sech(m)", "e - e^m", "1 - m", "i_Lorenz: (1-√m)^2", "coth(m)"]

fig, axes = plt.subplots(2, 3, figsize=(12, 8))
for i,ax in enumerate(axes.flat):
    f = fs[i]
    y = np.array([f(x) for x in xs])
    if name[i] == 'e - e^m' or name[i] == 'coth(m)':
        y /= f(xs[0])
    ax.plot(xs, y)
    ax.set_title(name[i])
    ax.set_xlabel('market share')
    ax.set_ylabel('weight')
plt.tight_layout()
plt.show()
