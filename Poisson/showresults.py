from Poisson.read_data_from_files import getdata_pnt
from read_data_from_files import getdata_2Dksp, getdata_3Dksp
from matplotlib import pyplot as plt
from typing import List, Tuple, Dict
import numpy as np

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
    

def show2Dgraph(results: List[Tuple[int, int, float]], title: str):
    """
    Given a list with (p, n, t) for each file, we plot 
    curves for each p
    """
    pvals = get_pvals(results)
    nvals = get_nvals(results)
    tvals = get_tvals(results)
    plt.figure()
    for p in pvals:
        plt.scatter(nvals[p], tvals[p], marker=".", label="%d"%p)
    ax = plt.gca()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Malha $n$")
    ax.set_ylabel(r"Tempo $t$")
    plt.legend()
    plt.grid()
    plt.title(title)

def main():
    mainfolder = (sys.argv[0]).replace("showresults.py", "")
    folder = mainfolder + "results_googlecloud4-2022-07-23"
    data = "Google Cloud - e2-highcpu-4 - 23 julho 2022"
    results = getdata_pnt(folder, "2D_ksp")
    show2Dgraph(results, "Resultados 2D - " + data)
    results = getdata_pnt(folder, "3D_ksp")
    show2Dgraph(results, "Resultados 3D - " + data)
    plt.show()

if __name__ == "__main__":
    main()