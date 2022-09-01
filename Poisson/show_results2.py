import numpy as np
from matplotlib import pyplot as plt
import sys
from typing import List, Tuple, Dict, Iterable, Optional
from read_data_from_files import getdata_pnt

def get_processors(results: List[Tuple[int, int, float]]):
    pairs = {}
    for p, n, t in results:
        if p not in pairs.keys():
            pairs[p] = []
        pairs[p].append((n, t))
    return pairs    

def get_numbermesh(results: List[Tuple[int, int, float]]):
    pairs = {}
    for p, n, t in results:
        if n not in pairs.keys():
            pairs[n] = []
        pairs[n].append((p, t))
    return pairs



def refine_vector(X: Iterable[float], n: Optional[int] = 10):
    xvec = []
    for i in range(len(X)-1):
        xvec += np.linspace(X[i], X[i+1], n, endpoint=False).tolist()
    xvec += [X[-1]]
    xvec = np.array(xvec)
    return xvec


def show2D_TServsTpara(results: List[Tuple[int, int, float]], title: str, punique: int):
    nvals = get_nvals(results)
    pvals = get_pvals(results)
    tvals = get_tvals(results)
    # plt.figure()
    ax = plt.gca()
    Tmax = np.max(tvals[1])
    colors = ["k", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive"]
    for j, p in enumerate(pvals):
        if p == 1:
            continue
        if p != punique:
            continue
        # if p != 2:
        #     continue
        tserial = []
        tparalel = []
        for i, n in enumerate(nvals[1]):
            if n in nvals[p]:
                index = nvals[p].index(n)
                tparalel.append(tvals[p][index])
                tserial.append(tvals[1][i])
        # plt.scatter(tserial, tparalel, marker=".", color=colors[j], label="%d"%p)
        plt.scatter(tserial, tparalel, marker=".", color=colors[j])
    tser = refine_vector([0, Tmax], 129)
    for j, p in enumerate(pvals):
        if p != punique and p != 1:
            continue
        plt.plot(tser, tser/p, color=colors[j], ls="dotted")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(xmin=0.1, xmax=1.1*Tmax)
    ax.set_ylim(ymin=0.1, ymax=1.1*Tmax)
    ax.set_xlabel(r"Tempo serial $T_s$ (s)")
    ax.set_ylabel(r"Tempo paralelo $T_p$ (s)")
    # plt.legend()
    plt.grid()
    # plt.title(title)

def get_names():
    names = ["e2highcpu8-13-08-2022",
             "e2highcpu8-24-07-2022",
             "e2memory8-22-08-2022",
             "e2memory8-23-08-2022",
             "e2memory8-26-08-2022",
             "e2standard8-12-08-2022",
             "e2standard8-16-08-2022"]
    

def get_allresults():
    mainfolder = (sys.argv[0]).replace("show_results2.py", "")
    pastas = ["results-e2highcpu8-13-08-2022",
              "results-e2highcpu8-24-07-2022",
              "results-e2memory8-22-08-2022",
              "results-e2memory8-23-08-2022",
              "results-e2memory8-26-08-2022",
              "results-e2standard8-12-08-2022",
              "results-e2standard8-16-08-2022"]
    allresults = []
    for pasta in pastas:
        folder = mainfolder + pasta
        results = getdata_pnt(folder, "2D_ksp")
        allresults.append(results)
    return allresults


def main1():
    """
    Plota gráficos com
        * numero de malha nas abscissas
        * tempo nas ordenadas
    """
    allresults = get_allresults()
    for p in range(2, 9):
        plt.figure()
        ax = plt.gca()
        for results in allresults:
            pairs = get_processors(results)
            array = np.array(pairs[p])
            plt.scatter(array[:, 0], array[:, 1], color="k")
        # plt.savefig("TserialVSTparalelo_2D_p%d_logarm.png" % p)
        ax.set_xscale("log")
        ax.set_yscale("log")
    plt.show()

def main2():
    """
    Plota gráficos com
        * numero de processadores
        * tempo nas ordenadas
    """
    plt.figure()
    allresults = get_allresults()
    nplot = [1000]
    for n in nplot:
        ax = plt.gca()
        for results in allresults:
            pairs = get_numbermesh(results)
            array = np.array(pairs[n])
            plt.scatter(array[:, 0], array[:, 1], label="%d"%n)
        # plt.savefig("TserialVSTparalelo_2D_p%d_logarm.png" % p)
        # ax.set_xscale("log")
        # ax.set_yscale("log")
        plt.legend()
    
    


# Programação Paralela para o método de diferenças finitas para o problema de Poisson


if __name__ == "__main__":
    main2()
    plt.show()