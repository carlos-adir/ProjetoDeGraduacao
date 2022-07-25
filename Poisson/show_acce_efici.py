import numpy as np
from matplotlib import pyplot as plt
import sys
from typing import List, Tuple, Dict
from read_data_from_files import getdata_pnt

def get_nvals(results: List[Tuple[int, int, float]]) -> List[int]:
    nvals = []
    for p, n, t in results:
        if n not in nvals:
            nvals.append(n)
    return nvals

def get_pvals(results: List[Tuple[int, int, float]]) -> Dict:
    pvals = {}
    nvals = get_nvals(results)
    for n in nvals:
        pvals[n] = []
    for p, n, t in results:
        pvals[n].append(p)
    return pvals


def get_tvals(results: List[Tuple[int, int, float]]) -> Dict:
    tvals = {}
    nvals = get_nvals(results)
    for n in nvals:
        tvals[n] = []
    for p, n, t in results:
        tvals[n].append(t)
    return tvals


def show2D_TvsP(results: List[Tuple[int, int, float]], title: str):
    nvals = get_nvals(results)
    pvals = get_pvals(results)
    tvals = get_tvals(results)
    plt.figure()
    for n in nvals:
        ps, ts = zip(*sorted(zip(pvals[n], tvals[n])))
        plt.plot(ps, ts, marker=".", label="%d"%n)
    ax = plt.gca()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Processadores $p$")
    ax.set_ylabel(r"Tempo $t$")
    plt.legend()
    plt.grid()
    plt.title(title)

def show2D_SpeedUp(results: List[Tuple[int, int, float]], title: str):
    nvals = get_nvals(results)
    pvals = get_pvals(results)
    tvals = get_tvals(results)
    plt.figure()
    for n in nvals:
        ps, ts = zip(*sorted(zip(pvals[n], tvals[n])))
        if ps[0] != 1:
            continue
        phi = np.array(ts)/ts[0]
        plt.plot(ps[1:], phi[1:], marker=".", label="%d"%n)
    ax = plt.gca()
    ax.set_xscale("log")
    ax.set_xlabel(r"Processadores $p$")
    ax.set_ylabel(r"SpeedUp $\phi$")
    plt.legend()
    plt.grid()
    plt.title(title)

def show2D_Efficiency(results: List[Tuple[int, int, float]], title: str):
    nvals = get_nvals(results)
    pvals = get_pvals(results)
    tvals = get_tvals(results)
    plt.figure()
    for n in nvals:
        ps, ts = zip(*sorted(zip(pvals[n], tvals[n])))
        if ps[0] != 1:
            continue
        phi = np.array(ts)/ts[0]
        eps = phi/ps
        plt.plot(ps[1:], eps[1:], marker=".", label="%d"%n)
    ax = plt.gca()
    ax.set_xscale("log")
    ax.set_xlabel(r"Processadores $p$")
    ax.set_ylabel(r"Eficiência $\phi$")
    plt.legend()
    plt.grid()
    plt.title(title)

def main():
    mainfolder = (sys.argv[0]).replace("show_acce_efici.py", "")
    folder = mainfolder + "results_googlecloud8-2022-07-24"
    data = "Google Cloud - e2-highcpu-8 - 24 julho 2022"
    results = getdata_pnt(folder, "2D_ksp")
    show2D_TvsP(results, "Resultados 2D - " + data)
    show2D_SpeedUp(results, "Resultados 2D - SpeedUp - " + data)
    show2D_Efficiency(results, "Resultados 2D - SpeedUp - " + data)
    
    plt.show()



if __name__ == "__main__":
    main()