import numpy as np
from matplotlib import pyplot as plt
import sys
from typing import List, Tuple, Dict, Iterable, Optional
from read_data_from_files import getdata_pnt

def get_pvals(results: List[Tuple[int, int, float]]) -> List[int]:
    pvals = []
    for p, n, t in results:
        if p not in pvals:
            pvals.append(p)
    return pvals

def get_nvals(results: List[Tuple[int, int, float]]) -> Dict:
    nvals = {}
    pvals = get_pvals(results)
    for p in pvals:
        nvals[p] = []
    for p, n, t in results:
        nvals[p].append(n)
    return nvals

def get_tvals(results: List[Tuple[int, int, float]]) -> Dict:
    tvals = {}
    pvals = get_pvals(results)
    for p in pvals:
        tvals[p] = []
    for p, n, t in results:
        tvals[p].append(t)
    return tvals

def refine_vector(X: Iterable[float], n: Optional[int] = 10):
    xvec = []
    for i in range(len(X)-1):
        xvec += np.linspace(X[i], X[i+1], n, endpoint=False).tolist()
    xvec += [X[-1]]
    xvec = np.array(xvec)
    return xvec


def show2D_TServsTpara(results: List[Tuple[int, int, float]], title: str):
    nvals = get_nvals(results)
    pvals = get_pvals(results)
    tvals = get_tvals(results)
    plt.figure()
    ax = plt.gca()
    Tmax = np.max(tvals[1])
    colors = ["k", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive"]
    for j, p in enumerate(pvals):
        if p == 1:
            continue
        tserial = []
        tparalel = []
        for i, n in enumerate(nvals[1]):
            if n in nvals[p]:
                index = nvals[p].index(n)
                tparalel.append(tvals[p][index])
                tserial.append(tvals[1][i])
        plt.scatter(tserial, tparalel, marker=".", color=colors[j], label="%d"%p)
    tser = refine_vector([0, Tmax], 100)    
    for j, p in enumerate(pvals):
        plt.plot(tser, tser/p, color=colors[j], ls="dotted")
    # ax.set_xscale("log")
    # ax.set_yscale("log")
    ax.set_xlim(xmin=0, xmax=1.1*Tmax)
    ax.set_ylim(ymin=0, ymax=1.1*Tmax)
    ax.set_xlabel(r"Tempo serial $T_s$ (s)")
    ax.set_ylabel(r"Tempo paralelo $T_p$ (s)")
    plt.legend()
    plt.grid()
    plt.title(title)



def main():
    mainfolder = (sys.argv[0]).replace("show_results2.py", "")
    folder = mainfolder + "results_googlecloud8-2022-07-24"
    data = "Google Cloud - e2-highcpu-8 - 24 julho 2022"
    results = getdata_pnt(folder, "2D_ksp")
    show2D_TServsTpara(results, "Resultados 2D - " + data)    
    plt.show()



if __name__ == "__main__":
    main()