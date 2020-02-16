import numpy as np
from matplotlib import pyplot as plt

lorenz = lambda ms: np.sqrt(1-np.square(ms))
softmax = lambda ms: np.exp(1)-np.exp(ms)
tanh = lambda ms: 1/np.tanh(ms) - 1/np.tanh(1)
lin = lambda ms: 1-ms

xs = np.delete(np.linspace(0, 1), [0, 49])

fs = [lorenz, softmax, tanh, lin]
name = ["Lorenz", "Softmax", "tanh", "linear"]
name = ["Lorenz: √(1-x^2)", "e - e^x", "tanh(x)", "1 - x"]

fig, axes = plt.subplots(2, 2, figsize=(8, 8), subplot_kw={'yticks':[]})
for i,ax in enumerate(axes.flat):
    y = np.array([fs[i](x) for x in xs])
    y = y/y.sum()
    ax.plot(xs, y)
    ax.set_title(name[i])
    ax.set_xlabel('market share')
    ax.set_ylabel('weight')
plt.tight_layout()
plt.show()
