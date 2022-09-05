import numpy as np
from matplotlib import pyplot as plt

import matplotlib.ticker as ticker


def ahmdal():
    plt.figure()
    ax = plt.gca()
    ax2 = ax.twinx()
    fvals = [0, 0.01, 0.05, 0.1, 0.2, 0.5, 1]
    p = np.exp(np.linspace(np.log(1.5), np.log(8), 129))
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
    ax.plot(p, p, ls="dashed", color="k", label="0")
    for i, f in enumerate(fvals):
        psi = 1/(f + (1-f)/p)
        eps = psi/p
        ax.plot(p, psi, color=colors[i], label=r"$f=%.2f$" % f)
        ax2.plot(p, eps, color=colors[i], ls="dotted")
    # ax.set_xscale("log", base=2)
    ax.set_ylabel(r"Aceleração $\psi$")
    ax2.set_ylabel(r"Eficiência $\varepsilon$")
    plt.xlim(1.5, 8.5)
    ax.set_ylim((0, 8))
    ax2.set_ylim((0, 1))
    ax.legend(loc="lower right")
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:g}'.format(x)))
    ax.set_xlabel(r"Número de processadores $p$")
    plt.grid()


def gustafson():
    plt.figure()
    ax = plt.gca()
    ax2 = ax.twinx()
    svals = [0, 0.05, 0.2, 0.5, 0.7, 0.9, 1]
    p = np.exp(np.linspace(np.log(2), np.log(8), 129))
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
    ax.plot(p, p, ls="dashed", color="k", label="0")
    for i, s in enumerate(svals):
        psi = p + (1-p)*s
        eps = psi/p
        ax.plot(p, psi, color=colors[i], label=r"$s=%.2f$" % s)
        ax2.plot(p, eps, color=colors[i], ls="dotted")
    # ax.set_xscale("log", base=2)
    ax.set_ylabel(r"Aceleração $\psi$")
    ax2.set_ylabel(r"Eficiência $\varepsilon$")
    plt.xlim(2, 8)
    ax.set_ylim((0, 8))
    ax2.set_ylim((0, 1))
    ax.legend()
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:g}'.format(x)))
    ax.set_xlabel(r"Número de processadores $p$")
    plt.grid()
    
def main():
    colorsdot = ["k", "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    ahmdal()
    gustafson()    
    plt.show()


if __name__ == "__main__":
    main()
    