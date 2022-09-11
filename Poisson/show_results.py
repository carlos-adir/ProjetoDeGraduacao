import numpy as np
from matplotlib import pyplot as plt
import sys
from typing import List, Tuple, Dict, Iterable, Optional
from read_data_from_files import *
try:
    from compmec.nurbs import SplineCurve, SplineBaseFunction
    from compmec.nurbs.knotspace import GeneratorKnotVector
    doregressao = True
except:
    import os
    os.system("pip install compmec-nurbs")
    from compmec.nurbs import SplineCurve, SplineBaseFunction
    from compmec.nurbs.knotspace import GeneratorKnotVector
    doregressao = True

def regressao_spline(x: Iterable[float], y: Iterable[float], t: Iterable[float]=None) -> np.ndarray:
    """
    Recebe pontos (x, y) e um vetor (t) chamado KnotVector (De Splines)
    E faz regressao usando SplineCurve,
    retornando o conjunto de pontos (x, y) que estão sobre a curva Spline
    """
    points = np.array([x, y]).T
    knotvec = GeneratorKnotVector.uniform(p=3, n=10)
    splinefunc = SplineBaseFunction(knotvec)
    ubar = (x-np.min(x))/(np.max(x)-np.min(x))
    L = splinefunc(ubar)
    points = np.linalg.solve(L @ L.T, L @ points)
    curve = SplineCurve(splinefunc, points)
    if t is None:
        t = np.linspace(0, 1, 129)
    return curve(t)

def regressao_linear(x: Iterable[float], y: Iterable[float]):
    n = len(x)
    L = np.ones((n, 2))
    L[:, 1] = x[:]
    y = np.array(y)
    Sol = np.linalg.solve( L.T @ L, L.T @ y)
    nplot = 129
    t = np.linspace(0, 1, nplot)
    points = np.zeros((nplot, 2))
    points[:, 0] = t * np.max(x) + (1-t) * np.min(x)
    points[:, 1] += Sol[0] + points[:, 0]*Sol[1]
    return points

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
    return nselect

def get_nvals(codigodim: str, size: str):
    if "2D" in codigodim:
        if size == "small":
            nvals = [100, 200, 256, 325]  # 2D small
        elif size == "med":
            nvals = [400, 650, 850, 1000]  # 2D med
        elif size == "big":
            nvals = [2000, 3000, 5000, 7500, 10000]  # 2D big
        else:
            raise ValueError("Not expect")
    elif "3D" in codigodim:
        if size == "small":
            nvals = [20, 40, 65, 75]  # 3D small
        elif size == "med":
            nvals = [100, 128, 180, 200]  # 3D med
        elif size == "big":
            nvals = [250, 300, 350, 400]  # 3D big
        else:
            raise ValueError("Not expect")
    else:
        raise ValueError("Not expect")
    return tuple(nvals)

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
        if doregressao:
            logns = np.log(ns)
            logts = np.log(ts)
            points = regressao_spline(logns, logts)
            nplot = np.exp(points[:, 0])
            tplot = np.exp(points[:, 1])
            plt.plot(nplot, tplot, ls="dotted", color=colors[p-1])
        # plt.scatter(ns, ts, marker="+", color=colors[p-1], label=r"$p=%d$"%p)
    plt.xlabel(r"Numero de malha $n$")
    plt.ylabel(r"Tempo $t$ (s)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.grid()
    plt.legend(loc="lower right")
    plt.savefig("Poisson/img/TempoLogXMalhaLog_" + codigodim + ".png")
    plt.close(fig)

def main2(nvals: Iterable[int]):
    """
    Plota gráficos com
        * numero de processadores
        * tempo nas ordenadas
    """
    fig = plt.figure()
    ax = plt.gca()
    pdisc = np.arange(1, 9)
    for i, n in enumerate(nvals):
        mask = (allns == n)
        ps = allps[mask]
        ts = allts[mask]
        tdisc = [np.mean(ts[ps==p]) for p in pdisc]
        plt.plot(pdisc, tdisc, color=colors[i], ls="dashed")
        plt.scatter(ps, ts, marker="+", color=colors[i], label=r"$n=%d$"%n)
    ax.set_yscale("log")
    ax.set_ylabel(r"Tempo $t$ (s)")
    ax.set_xlabel(r"Processadores $p$")
    plt.legend()
    plt.savefig("Poisson/img/TempoLogXProc_" + codigodim + "_n" + size + ".png")
    plt.close(fig)

def main3(nvals: Iterable[int]):
    """
    Plota gráficos com
        * numero de processadores
        * aceleracao
    """
    fig = plt.figure()
    ax = plt.gca()
    # fs = np.linspace(0, 0.2, 5)
    pplot = np.linspace(1, 8, 1025)
    pdisc = np.arange(2, 9)
    fs = [0, 0.01, 0.05, 0.1, 0.2]
    dottedlines = []
    solidlines = []
    psimax = 8
    for i, f in enumerate(fs):
        psi = 1/(f + (1-f)/pplot)
        dotline, = plt.plot(pplot, psi, ls="dotted", color=colorsdot[i], label=r"$f=%.2f$"%f)
        dottedlines.append(dotline)
    for i, n in enumerate(nvals):
        maskn = (allns == n)
        maskp1 = (allps == 1)
        maskpO = (allps > 1)
        tp1 = np.mean(allts[maskn * maskp1])
        ps = allps[maskn * maskpO]
        ts = allts[maskn * maskpO]
        psi = tp1/ts
        psimax = max(psimax, np.max(psi))
        psidisc = [np.mean(psi[ps==p]) for p in pdisc]
        plt.plot(pdisc, psidisc , color=colors[i], ls="dashed")
        solline = plt.scatter(ps, psi, color=colors[i], marker="+", label=r"$n=%d$"%n)
        solidlines.append(solline)
    first_legend = plt.legend(handles=dottedlines, loc='lower right')
    plt.gca().add_artist(first_legend)
    plt.legend(handles=solidlines, loc='upper left')
    plt.grid()
    plt.xlim(1.5, 8.5)
    plt.ylim(0, 1.1*psimax)
    ax.set_ylabel(r"Aceleracao $\psi$")
    ax.set_xlabel(r"Processadores $p$")
    plt.savefig("Poisson/img/AceleracaoXProc_" + codigodim + "_n" + size + ".png")
    plt.close(fig)
    
def main4(nvals: Iterable[int]):
    """
    Plota gráficos com
        * numero de processadores
        * eficiencia
    """
    ps = np.arange(1, 9)
    pplot = np.linspace(2, 8, 129)
    fig = plt.figure()
    ax = plt.gca()
    # fs = np.linspace(0, 0.2, 5)
    pdisc = np.arange(2, 9)
    fs = [0, 0.01, 0.05, 0.1, 0.2]
    dottedlines = []
    solidlines = []
    for i, f in enumerate(fs):
        psi = 1/(f + (1-f)/pplot)
        eps = psi/pplot
        dotline, = plt.plot(pplot, eps, color=colorsdot[i], ls="dotted", label=r"$f=%.2f$"%f)
        dottedlines.append(dotline)
    maxeps = 1
    for i, n in enumerate(nvals):
        maskn = (allns == n)
        maskp1 = (allps == 1)
        maskpO = (allps > 1)
        tp1 = np.mean(allts[maskn * maskp1])
        ps = allps[maskn * maskpO]
        ts = allts[maskn * maskpO]
        psi = tp1/ts
        eps = psi/ps
        maxeps = max(maxeps, np.max(eps))
        epsdisc = [np.mean(eps[ps==p]) for p in pdisc]
        plt.plot(pdisc, epsdisc , color=colors[i], ls="dashed")
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
    plt.savefig("Poisson/img/EficiXProc_" + codigodim + "_n" + size + ".png")
    plt.close(fig)

def main5(nvals: Iterable[int]):
    """
    Plota gráficos - Karpflat
        * numero de processadores
        * eficiencia
    """
    psdisc = np.arange(1, 9)
    pplot = np.linspace(2, 8, 129)
    fig = plt.figure()
    ax = plt.gca()
    # fs = np.linspace(0, 0.2, 5)
    # fs = [0.01, 0.05, 0.1, 0.2, 0.5, 1]
    dottedlines = []
    solidlines = []
    for i, n in enumerate(nvals):
        maskn = (allns == n)
        maskp1 = (allps == 1)
        maskpO = (allps > 1)
        tp1 = np.mean(allts[maskn * maskp1])
        ps = allps[maskn * maskpO]
        ts = allts[maskn * maskpO]
        psi = tp1/ts
        evals = (1/psi)-(1/ps)
        evals /= 1-(1/ps)
        print("i = ", i)
        evalsdisc = [np.mean(evals[ps==p]) for p in psdisc]
        plt.plot(psdisc, evalsdisc, ls="dashed", color=colors[i])
        solline = plt.scatter(ps, evals, color=colors[i], marker="+", label=r"$n=%d$"%n)
        solidlines.append(solline)
    # first_legend = plt.legend(handles=dottedlines, loc='lower right')
    # plt.gca().add_artist(first_legend)
    plt.legend(handles=solidlines, loc='upper left')
    plt.grid()
    plt.xlim(1.5, 8.5)
    # plt.ylim(0, 1.1*maxeps)
    ax.set_ylabel(r"Karp flat $\varepsilon$")
    ax.set_xlabel(r"Processadores $p$")
    # plt.show()
    plt.savefig("Poisson/img/KarpXProc_" + codigodim + "_n" + size + ".png")
    plt.close(fig)

def main6(listfilenames: Iterable[str], pfix: Optional[int] = None):
    """
    Com eixo X nas abssissas o numero de malha
    No eixo Y a razao r = (time evento)/tempo total
    apenas para os eventos que r > 0.02
    """
    allpoints = {}
    # eventstosave = ["VecMDot", "VecMAXPY", "MatMult", "MatSolve", "KSPSolve", "KSPGMRESOrthog", "PCApply"]
    # eventstosave = ["VecMAXPY", "KSPSolve", "KSPGMRESOrthog", "PCApply"]
    eventstosave = ["KSPSolve", "KSPGMRESOrthog"]
    for filename in listfilenames:
        p, n, t = get_pnt(filename)
        if t < 0:
            continue
        if pfix is not None:
            if p != pfix:
                continue
        table = get_logvieweventstable(filename)
        eventos = table["Event"]
        timemax = table["Time (sec) Max"]
        eventos = np.array(eventos)
        mask = np.array([eve in eventstosave for eve in eventos])
        razao = np.array(timemax)/t
        evs, ras = eventos[mask], razao[mask]
        # evs = np.array(evs.tolist() + ["Total"])
        # ras = np.array(ras.tolist() + [np.sum(razao)])
        for ev, ra in zip(evs, ras):
            if ev not in allpoints:
                allpoints[ev] = []
            allpoints[ev].append((n, ra))
    fig = plt.figure()
    for i, (ev, points) in enumerate(allpoints.items()):
        points = np.array(points)
        nvals = points[:, 0]
        rvals = points[:, 1]
        plt.scatter(nvals, rvals, color=colors[i], marker=".", label=ev)
        if doregressao:
            pointsregressao = regressao_spline(np.log(nvals), rvals)
            pointsregressao[:, 0] = np.exp(pointsregressao[:, 0])
            plt.plot(pointsregressao[:, 0], pointsregressao[:, 1], color=colors[i], ls="dotted") 
    plt.gca().set_xscale("log")
    plt.legend()
    plt.xlabel(r"Tamanho de malha $n$")
    if pfix is not None:
        plt.ylabel(r"Fração $\dfrac{T_{i}(n, %d)}{T(n, %d)}$"%(pfix, pfix))
    else:
        plt.ylabel(r"Fração $\dfrac{T_{i}(n, p)}{T(n, p)}$")
    plt.grid()
    plt.savefig("Poisson/img/RazaoTempoXMalha_" + codigodim + ".png")
    plt.close(fig)

def main7(listfilenames: Iterable[str], pfix: Optional[int] = None):
    """
    Esse aqui val plotar o grafico, 
    com eixo X nas abssissas o numero de malha
    No eixo Y a memoria consumida
    """
    allpoints = {}
    objectstosave = ["Vector", "Matrix", "Index Set", "Krylov Solver", "IS L to G Mapping", "Distributed Mesh"]
    for filename in listfilenames:
        p, n, t = get_pnt(filename)
        if t < 0:
            continue
        if pfix is not None:
            if p != pfix:
                continue
        table = get_logviewmemorytable(filename)
        objects = np.array([line[0] for line in table])
        memories = np.array([line[3] for line in table], dtype="float64")
        memories /= (2**30)  # Transformar bytes em GB
        mask = np.array([obj in objectstosave for obj in objects])
        # mask = np.ones(objects.shape) == 1
        objs, mems = objects[mask], memories[mask]
        objs = np.array(objs.tolist() + ["Total"])
        mems = np.array(mems.tolist() + [np.sum(memories)])
        for obj, mem in zip(objs, mems):
            if obj not in allpoints:
                allpoints[obj] = []
            allpoints[obj].append((n, mem))
    fig = plt.figure()
    for i, (obj, points) in enumerate(allpoints.items()):
        points = np.array(points)
        nvals = points[:, 0]
        mvals = points[:, 1]
        plt.scatter(nvals, mvals, color=colors[i], marker="+", label=obj)
        if doregressao:
            pointsregressao = np.exp(regressao_linear(np.log(nvals), np.log(mvals)))
            plt.plot(pointsregressao[:,0], pointsregressao[:,1], color=colors[i], ls="dotted") 
    plt.gca().set_xscale("log")
    plt.gca().set_yscale("log")
    plt.legend()
    plt.xlabel(r"Tamanho de malha $n$")
    plt.ylabel("Memória total consumida (GB)")
    plt.grid()
    plt.savefig("Poisson/img/MemoriaConsumidaXMalha_" + codigodim + ".png")
    plt.close(fig)
            
def main8(allfilenames: Iterable[str], nvals: Iterable[int]):
    """
    Plota da quantidade de mensagens
        * numero de processadores
        * quantidade de mensagens
    """
    psdisc = np.arange(1, 9)
    fig = plt.figure()
    ax = plt.gca()
    # fs = np.linspace(0, 0.2, 5)
    # fs = [0.01, 0.05, 0.1, 0.2, 0.5, 1]
    dottedlines = []
    solidlines = []
    allpoints = {}
    for n in nvals:
        allpoints[n] = []
    for i, filename in enumerate(allfilenames):
        p, n, t = get_pnt(filename)
        if t < 0:  # Nao pode ler corretamente
            continue
        if p == 1:  # Nao ha mensagens com apenas 1 processador
            continue
        if n not in nvals:
            continue
        table = get_logvieweventstable(filename)
        messages = table["Mess"]
        totalmessages = np.sum(messages)
        if totalmessages == 0:
            continue
        allpoints[n].append((p, totalmessages))
    fig = plt.figure()
    for i, n in enumerate(nvals):
        points = np.array(allpoints[n])
        solline = plt.scatter(points[:, 0], points[:, 1], marker="+", color=colors[i], label=r"$n=%d$"%n)
        solidlines.append(solline)
    # first_legend = plt.legend(handles=dottedlines, loc='lower right')
    # plt.gca().add_artist(first_legend)
    # plt.legend(handles=solidlines, loc='upper left')
    plt.legend()
    plt.grid()
    plt.xlim(1.5, 8.5)
    plt.ylim(ymin=1)
    plt.title("Main 8")
    # plt.ylim(0, 1.1*maxeps)
    ax.set_yscale("log")
    ax.set_xlabel(r"Processadores $p$")
    ax.set_ylabel(r"Numero de mensagens")
    # plt.show()
    plt.savefig("Poisson/img/QuantidadeMessageXProc_" + codigodim + "_n" + size + ".png")
    plt.close(fig)

# Descoberta nova: para grandes valores de n, a quantidade de mensagens não muda...
# https://petsc.org/release/docs/manualpages/Vec/VecMDot.html
# https://petsc.org/release/docs/manualpages/Vec/VecMAXPY.html
# Programação Paralela para o método de diferenças finitas para o problema de Poisson

def main9(listfilenames: Iterable[str]):
    """
    Plota nos eixos:
        numero de malhas
        memória consumida
    varias curvas de nivel, para diferentes processadores
    """
    allpoints = {}
    for p in range(1, 9):
        allpoints[p] = []
    for filename in listfilenames:
        p, n, t = get_pnt(filename)
        if t < 0:
            continue
        table = get_logviewmemorytable(filename)
        memories = np.array([line[3] for line in table], dtype="float64")
        memories /= (2**30)  # Transformar bytes em GB
        allpoints[p].append((n, np.sum(memories)))
    fig = plt.figure()
    for i, (p, points) in enumerate(allpoints.items()):
        points = np.array(points)
        nvals = points[:, 0]
        mvals = points[:, 1]
        plt.scatter(nvals, mvals, color=colors[i], marker="+", label="p=%d"%p)
        if doregressao:
            pointsregressao = np.exp(regressao_linear(np.log(nvals), np.log(mvals)))
            plt.plot(pointsregressao[:,0], pointsregressao[:,1], color=colors[i], ls="dotted") 
    plt.gca().set_xscale("log")
    plt.gca().set_yscale("log")
    plt.legend()
    plt.xlabel(r"Tamanho de malha $n$")
    plt.ylabel("Memória total consumida (GB)")
    # plt.title("Main 9")
    plt.grid()
    plt.savefig("Poisson/img/MemoriaTotalConsumidaXMalha_" + codigodim + ".png")
    plt.close(fig)
    

def main10(listfilenames: Iterable[str]):
    """
    Plota nos eixos:
        numero de malhas
        razao memória consumida: memoria paralela/memoria serial
    varias curvas de nivel, para diferentes processadores
    """
    allpoints = {}
    for filename in listfilenames:
        p, n, t = get_pnt(filename)
        if t < 0:
            continue
        table = get_logviewmemorytable(filename)
        memories = np.array([line[3] for line in table], dtype="float64")
        memories /= (2**30)  # Transformar bytes em GB
        if n not in allpoints:
            allpoints[n] = []
        allpoints[n].append((p, np.sum(memories)))
    fig = plt.figure()
    for i, (n, points) in enumerate(allpoints.items()):
        points = np.array(points)
        pvals = points[:, 0]
        mvals = points[:, 1]
        maskp1 = (pvals == 1)
        relativememory = mvals[~maskp1]/np.mean(mvals[maskp1])
        plt.scatter(pvals[~maskp1], relativememory, marker="+", color="r")    
    plt.legend()
    plt.xlim(1.5, 8.5)
    plt.xlabel(r"Tamanho de malha $n$")
    plt.ylabel("Razao de memória consumida paralela/serial")
    # plt.title("Main 10")
    plt.grid()
    plt.savefig("Poisson/img/RazaoMemoriaTotalXProc_" + codigodim + ".png")
    plt.close(fig)


def main11(listfilenames: Iterable[str]):
    """
    Eixo X: Numero de malha
    Eixo Y: Razao do tempo KSPSolve / Tempo do processo
    """
    allpoints = {}
    for p in range(1, 9):
        allpoints[p] = []
    for filename in listfilenames:
        p, n, t = get_pnt(filename)
        if t < 0:
            continue
        table = get_logvieweventstable(filename)
        eventos = np.array(table["Event"])
        timemax = np.array(table["Time (sec) Max"])
        mask = (eventos == "KSPSolve")
        razao = np.array(timemax)/t
        allpoints[p].append((n, float(razao[mask])))
    fig = plt.figure()
    for i, (p, points) in enumerate(allpoints.items()):
        points = np.array(points)
        nvals = points[:, 0]
        rvals = points[:, 1]
        plt.scatter(nvals, rvals, color=colors[i], marker=".", label="p=%d"%p)
        if doregressao:
            pointsregressao = regressao_spline(np.log(nvals), rvals)
            pointsregressao[:, 0] = np.exp(pointsregressao[:, 0])
            plt.plot(pointsregressao[:, 0], pointsregressao[:, 1], color=colors[i], ls="dotted")
    plt.gca().set_xscale("log")
    plt.legend()
    plt.xlabel(r"Tamanho de malha $n$")
    plt.ylabel(r"Fração Tempo do KSPSolve/$T(n,p)$")
    plt.grid()
    plt.savefig("Poisson/img/FracaoTempoKSPSolveXMalha_" + codigodim + ".png")
    plt.close(fig)

if __name__ == "__main__":
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "yellow"]
    colorsdot = ["k", "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "m"]
    currentfolder = "C:/Users/carlo/Documents/Git/GraduationProject/Poisson/"
    allfoldernames = [currentfolder + folder for folder in all_results_folders()]
    for codigodim in ["2D_ksp"]:
    # for codigodim in ["2D_ksp", "3D_ksp"]:
        allfilenames = get_listfiles_in_folders(allfoldernames)
        allfilenames = filter_files(allfilenames, codigodim)
        allps, allns, allts = get_pnt(allfilenames)
        main1()
        main6(allfilenames, pfix=4)
        main7(allfilenames, pfix=4)
        main9(allfilenames)
        main10(allfilenames)
        main11(allfilenames)
        for size in ["small", "med", "big"]:
            nvals = get_nvals(codigodim, size)
            main2(nvals)
            main3(nvals)
            main4(nvals)
            main5(nvals)
            main8(allfilenames, nvals)
    plt.show()