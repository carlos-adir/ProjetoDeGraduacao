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
    """
    Recebe um vetor, e então insere pontos dentro do vetor. Exemplo:
        Input: [0, 1]
        Output: [0, 0.2, 0.4, 0.6, 0.8, 1]
    """
    xvec = []
    for i in range(len(X)-1):
        xvec += np.linspace(X[i], X[i+1], n, endpoint=False).tolist()
    xvec += [X[-1]]
    xvec = np.array(xvec)
    return xvec


def get_names():
    names = ["results-e2highcpu8-13-08-2022",
             "results-e2highcpu8-24-07-2022",
             "results-e2memory8-22-08-2022",
             "results-e2memory8-23-08-2022",
             "results-e2memory8-26-08-2022",
             "results-e2standard8-12-08-2022",
             "results-e2standard8-16-08-2022"]
    return names
    

def get_allresults(tipo: str):
    """
    Returns a List[List[(p, n, t)]] 
    """
    mainfolder = (sys.argv[0]).replace("show_results2.py", "")
    pastas = get_names()
    allresults = []
    for pasta in pastas:
        folder = mainfolder + pasta
        results = getdata_pnt(folder, tipo)
        allresults.append(results)
    return allresults

def get_table(tipo: str):
    """
    Retorna uma tupla com shape (3, m)
        em que m é o numero de arquivos
    allps, allns, allts = get_table()
    """
    allresults = get_allresults(tipo)
    allps = []
    allns = []
    allts = []
    for results in allresults:
        for p, n, t in results:
            allps.append(p)
            allns.append(n)
            allts.append(t)
    allps = np.array(allps, dtype="int16")
    allns = np.array(allns, dtype="int32")
    allts = np.array(allts, dtype="float64")
    return allps, allns, allts

def get_nselect(nlower: int=None, nupper: int=None) -> Tuple[int]:
    """
    Retorna todos os valores de n que estao dentro de [nlower, nupper]
    """
    if nlower is None:
        nlower = 1
    if nupper is None:
        nupper = 50000
    ns = list(set(allns))
    nselect = []
    for i, n in enumerate(ns):
        if n < nlower:
            continue
        if nupper < n:
            continue
        if n not in nselect:
            nselect.append(n)
    nselect.sort()

    if "2D" in tipo:
        if size == "small":
            nval = [100, 200, 256, 325]  # 2D small
        elif size == "med":
            nval = [400, 650, 850, 1000]  # 2D med
        elif size == "big":
            nval = [2000, 3000, 5000, 7500, 10000]  # 2D big
        else:
            raise ValueError("Not expect")
    elif "3D" in tipo:
        if size == "small":
            nval = [20, 40, 65, 75]  # 3D small
        elif size == "med":
            nval = [100, 128, 180, 200]  # 3D med
        elif size == "big":
            nval = [250, 300, 350, 400]  # 3D big
        else:
            raise ValueError("Not expect")
    else:
        raise ValueError("Not expect")
    for n in nval:
        if n not in nselect:
            raise ValueError("n = %d is not in %s" % (n, str(nselect)))
    return tuple(nval)

def main1():
    """
    Plota gráficos com
        * numero de malha nas abscissas
        * tempo nas ordenadas
    """
    fig = plt.figure()
    ax = plt.gca()
    for p in range(1, 9):
        mask = (allps == p)
        ns = allns[mask]
        ts = allts[mask]
        plt.scatter(ns, ts, marker="+", color=colors[p-1], label=r"$p=%d$"%p)
    plt.xlabel(r"Numero de malha $n$")
    plt.ylabel(r"Tempo $t$ (s)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.grid()
    plt.legend(loc="lower right")
    plt.savefig("Poisson/img/TempoLogXMalhaLog_" + tipo + ".png")
    plt.close(fig)

def main2():
    """
    Plota gráficos com
        * numero de processadores
        * tempo nas ordenadas
    """
    nselect = get_nselect()
    fig = plt.figure()
    ax = plt.gca()
    for i, n in enumerate(nselect):
        mask = (allns == n)
        plt.scatter(allps[mask], allts[mask], marker="+", color=colors[i], label=r"$n=%d$"%n)
    ax.set_yscale("log")
    ax.set_ylabel(r"Tempo $t$ (s)")
    ax.set_xlabel(r"Processadores $p$")
    plt.legend()
    plt.savefig("Poisson/img/TempoLogXProc_" + tipo + "_n" + size + ".png")
    plt.close(fig)

def main3():
    """
    Plota gráficos com
        * numero de processadores
        * aceleracao
    """
    
    nselect = get_nselect()
    fig = plt.figure()
    ax = plt.gca()
    # fs = np.linspace(0, 0.2, 5)
    pplot = np.linspace(1, 8, 1025)
    fs = [0, 0.02, 0.05, 0.15]
    dottedlines = []
    solidlines = []
    for i, f in enumerate(fs):
        psi = 1/(f + (1-f)/pplot)
        dotline, = plt.plot(pplot, psi, ls="dotted", color=colorsdot[i], label=r"$f=%.2f$"%f)
        dottedlines.append(dotline)
    for i, n in enumerate(nselect):
        maskn = (allns == n)
        maskp1 = (allps == 1)
        maskpO = (allps > 1)
        tp1 = np.mean(allts[maskn * maskp1])
        ps = allps[maskn * maskpO]
        ts = allts[maskn * maskpO]
        psi = tp1/ts
        solline = plt.scatter(ps, psi, color=colors[i], marker="+", label=r"$n=%d$"%n)
        solidlines.append(solline)
    first_legend = plt.legend(handles=dottedlines, loc='lower right')
    plt.gca().add_artist(first_legend)
    plt.legend(handles=solidlines, loc='upper left')
    plt.grid()
    plt.xlim(1.5, 8.5)
    plt.ylim(0, 8)
    ax.set_ylabel(r"Aceleracao $\psi$")
    ax.set_xlabel(r"Processadores $p$")
    plt.savefig("Poisson/img/AceleracaoXProc_" + tipo + "_n" + size + ".png")
    plt.close(fig)
    
def main4():
    """
    Plota gráficos com
        * numero de processadores
        * eficiencia
    """
    nselect = get_nselect()
    ps = np.arange(1, 9)
    pref = np.linspace(2, 8, 129)
    fig = plt.figure()
    ax = plt.gca()
    # fs = np.linspace(0, 0.2, 5)
    fs = [0, 0.02, 0.05, 0.15]
    dottedlines = []
    solidlines = []
    for i, f in enumerate(fs):
        psi = 1/(f + (1-f)/pref)
        eps = psi/pref
        dotline, = plt.plot(pref, eps, color=colorsdot[i], ls="dotted", label=r"$f=%.2f$"%f)
        dottedlines.append(dotline)
    maxeps = 1
    for i, n in enumerate(nselect):
        maskn = (allns == n)
        maskp1 = (allps == 1)
        maskpO = (allps > 1)
        tp1 = np.mean(allts[maskn * maskp1])
        ps = allps[maskn * maskpO]
        ts = allts[maskn * maskpO]
        psi = tp1/ts
        eps = psi/ps
        maxeps = max(maxeps, np.max(eps))
        solline = plt.scatter(ps, eps, color=colors[i], marker="+", label=r"$n=%d$"%n)
        solidlines.append(solline)
    first_legend = plt.legend(handles=dottedlines, loc='lower right')
    plt.gca().add_artist(first_legend)
    plt.legend(handles=solidlines, loc='lower left')
    plt.grid()
    plt.xlim(1.5, 8.5)
    plt.ylim(0, 1.1*maxeps)
    ax.set_ylabel(r"Eficiencia $\varepsilon$")
    ax.set_xlabel(r"Processadores $p$")
    plt.savefig("Poisson/img/EficiXProc_" + tipo + "_n" + size + ".png")
    plt.close(fig)


# Programação Paralela para o método de diferenças finitas para o problema de Poisson


if __name__ == "__main__":
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "yellow"]
    colorsdot = ["k", "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    for tipo in ["2D_ksp", "3D_ksp"]:
        allps, allns, allts = get_table(tipo)
        main1()
        for size in ["small", "med", "big"]:
            main2()
            main3()
            main4()
    # plt.show()