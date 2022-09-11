import re
import os
import numpy as np
from os import listdir
from os.path import isfile, join
from typing import List, Tuple, Dict, Any, Iterable

def get_files(folder: str) -> List[str]:
    """
    Given a folder, it will return all the filenames inside it
    If "key" is given, it will filter these
    """
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    return onlyfiles
    
def fileexists(filename: str) -> bool:
    try:
        file = open(filename, "r")
        file.close()
        return True
    except Exception as e:
        return False

def readfile(filename: str) -> str:
    if not fileexists:
        raise ValueError(f"Tried to read {filename}, but doesn't exist")
    with open(filename, "r") as file:
        lines = file.readlines()
    return '\n'.join(lines)

def filter_files(listfilesnames: List[str], key: str):
    """
    given a list of filenames INPUT,
    it will return a list OUTPUT such
    every element in OUTPUT has the "key" inside
    """
    newlistfilesnames = []
    for filename in listfilesnames:
        if key in filename:
            newlistfilesnames.append(filename)
    return newlistfilesnames


def get_logviewperformancetable(filename: str) -> List[List[Any]]:
    """
    Receives something like that
        [0]                          Max       Max/Min     Avg       Total
        [0] Time (sec):           3.441e+02     1.000   3.441e+02
        [0] Objects:              6.900e+01     1.000   6.900e+01
        [0] Flops:                3.008e+11     1.000   3.008e+11  2.406e+12
        [0] Flops/sec:            8.741e+08     1.000   8.741e+08  6.993e+09
        [0] MPI Msg Count:        1.860e+03     1.000   1.860e+03  1.488e+04
        [0] MPI Msg Len (bytes):  4.546e+08     1.000   2.444e+05  3.637e+09
        [0] MPI Reductions:       1.329e+03     1.000
        [0] 
    And returns the table
        [['Time (sec)', 344.1, 1.0, 344.1, None],
         ['Objects', 69.0, 1.0, 69.0, None],
         ['Flops', 300800000000.0, 1.0, 300800000000.0, 2406000000000.0],
         ['Flops/sec', 874100000.0, 1.0, 874100000.0, 6993000000.0],
         ['MPI Msg Count', 1860, 1.0, 1860.0, 14880.0],
         ['MPI Msg Len (bytes)', 454600000.0, 1.0, 244400.0, 3637000000.0],
         ['MPI Reductions', 1329.0, 1.0, None, None]]
    """
    texto = readfile(filename)
    regexlinha = r"\[0\] ([a-zA-Z(\)\/\s]+):\s+([\d.e+-]+)\s+([\d.]+)\s*([\d.e+-]+)?\s*([\d.e+-]+)?"
    encontros = re.findall(regexlinha, texto)
    for i, e in enumerate(encontros):
        encontros[i] = list(e)
        while '' in encontros[i]:
            encontros[i].remove('')
        encontros[i][1] = float(encontros[i][1])
        encontros[i][2] = float(encontros[i][2])
        if len(encontros[i]) >= 4:
            encontros[i][3] = float(encontros[i][3])
        if len(encontros[i]) >= 5:
            encontros[i][4] = float(encontros[i][4])
        for j in range(len(encontros[i]), 5):
            encontros[i].append(None)
    return encontros

def get_logviewmemorytable(filename: str) -> List[List[Any]]:
    """
    Receives something like that
        [0] Memory usage is given in bytes:
        [0] 
        [0] Object Type          Creations   Destructions     Memory  Descendants' Mem.
        [0] Reports information only for process 0.
        [0] 
        [0] --- Event Stage 0: Main Stage
        [0]        Krylov Solver     2              2        20488     0.
        [0]      DMKSP interface     1              1          664     0.
        [0]               Matrix     5              5   1197576792     0.
        [0]     Distributed Mesh     1              1         5584     0.
        [0]            Index Set     7              7     86491320     0.
        [0]    IS L to G Mapping     1              1     21807784     0.
        [0]    Star Forest Graph     4              4         4832     0.
        [0]      Discrete System     1              1          968     0.
        [0]            Weak Form     1              1          624     0.
        [0]               Vector    43             43   1587185856     0.
        [0]       Preconditioner     2              2         1952     0.
        [0]               Viewer     1              0            0     0.
    And returns the table
        [['Krylov Solver', 2, 2, 20488, 0.],
         ['DMKSP interface', 1, 1, 664, 0.],
         ['Matrix', 5, 5, 1197576792, 0.],
         ['Distributed Mesh', 1, 1, 5584, 0.],
         ['Index Set', 7, 7, 86491320, 0.],
         ['IS L to G Mapping', 1, 1, 21807784, 0.],
         ['Star Forest Graph', 4, 4, 4832, 0.],
         ['Discrete System', 1, 1, 968, 0.],
         ['Weak Form', 1, 1, 624, 0.],
         ['Vector', 43, 43, 1587185856, 0.],
         ['Preconditioner', 2, 2, 1952, 0.],
         ['Viewer', 1, 0, 0, 0.]]
    """
    texto = readfile(filename)
    regexlinha = r"\[0\]\s+([a-zA-Z\s]+[a-zA-Z])\s{2,}(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)"
    encontros = re.findall(regexlinha, texto)
    for i, e in enumerate(encontros):
        encontros[i] = list(e)
        while '' in encontros[i]:
            encontros[i].remove('')
        encontros[i][1] = int(encontros[i][1])
        encontros[i][2] = int(encontros[i][2])
        encontros[i][3] = int(encontros[i][3])
    return encontros

def get_logvieweventstable(filename: str) -> Dict:
    """
    Returns the big table in the middle of file
    Receives the filename, reads it, which has inside:
        [0] BuildTwoSided          3 1.0 5.9373e-02183.7 0.00e+00 0.0 2.4e+01 4.0e+00 3.0e+00  0  0  0  0  0   0  0  0  0  0     0[0] 
        [0] BuildTwoSidedF         2 1.0 5.9017e-02676.9 0.00e+00 0.0 0.0e+00 0.0e+00 2.0e+00  0  0  0  0  0   0  0  0  0  0     0[0] 
    Returns a dict like
        {"Event": ['BuildTwoSided', 'BuildTwoSidedF'],
         "Count Max": [3, 2],
         "Count Ratio": [1.0, 1.0],
         ...
         "Stage %R": [0, 0],
         "Total Mflops": [0, 0]}
    """
    texto = readfile(filename)
    regexlinha = r"\[0\] ([a-zA-Z]+)\s+(\d+)\s+([\d.]+)\s(\d.\d{4}e[+|-]\d{2})\s?(\d+.\d) (\d.\d{2}e[+-]\d{2}) (\d.\d) (\d.\de[+-]\d{2}) (\d.\de[+-]\d{2}) (\d.\de[+-]\d{2})([\s\d]{3})([\s\d]{3})([\s\d]{3})([\s\d]{3})([\s\d]{3}) ([\s\d]{3})([\s\d]{3})([\s\d]{3})([\s\d]{3})([\s\d]{3})\s+(\d+)"
    encontros = re.findall(regexlinha, texto)
    headers = ["Event", "Count Max", "Count Ratio", "Time (sec) Max", "Time (sec) Ratio",
               "Flop Max", "Flop Ratio", "Mess", "AvgLen", "Reduct",
               "Global %T", "Global %F", "Global %M", "Global %L", "Global %R",
               "Stage %T", "Stage %F", "Stage %M", "Stage %L", "Stage %R", "Total Mflop/s"]
    table = {}
    for head in headers:
        table[head] = []
    for i, e in enumerate(encontros):
        encontros[i] = list(e)
        encontros[i][0] = str(e[0])
        encontros[i][1] = int(e[1])
        encontros[i][2] = float(e[2])
        encontros[i][3] = float(e[3])
        encontros[i][4] = float(e[4])
        encontros[i][5] = float(e[5])
        encontros[i][6] = float(e[6])
        encontros[i][7] = float(e[7])
        encontros[i][8] = float(e[8])
        encontros[i][9] = float(e[9])
        encontros[i][10] = int(e[10].replace(" ", ""))
        encontros[i][11] = int(e[11].replace(" ", ""))
        encontros[i][12] = int(e[12].replace(" ", ""))
        encontros[i][13] = int(e[13].replace(" ", ""))
        encontros[i][14] = int(e[14].replace(" ", ""))
        encontros[i][15] = int(e[15].replace(" ", ""))
        encontros[i][16] = int(e[16].replace(" ", ""))
        encontros[i][17] = int(e[17].replace(" ", ""))
        encontros[i][18] = int(e[18].replace(" ", ""))
        encontros[i][19] = int(e[19].replace(" ", ""))
        encontros[i][20] = int(e[20])
        for j, head in enumerate(headers):
            table[head].append(encontros[i][j])
    return table

def get_pnt_single(filename: str) -> Tuple[int, int, float]:
    """
    Receives a filename as input and returns 
    the p (number of processors), n (the mesh's size)
    and the t (total time in process) 
    """
    texto = readfile(filename)
    filename = filename.split("/")[-1]
    filename = filename.split("\\")[-1]
    p = int(filename.split("-p")[1].split("-mesh")[0])
    n = int(filename.split("mesh")[1].split("x")[0])
    try:
        t = float(re.findall(r"Processor 0 took ((\d+\.?\d*)|(\.\d+)) CPU seconds", texto)[0][0])
    except Exception as e:
        t = -1
    return p, n, t

def get_problem_files(listfilenames: List[str]) -> List[str]:
    """
    Receives a list of filenames as INPUT,
    and it will try read each file
    if something in the file has gone wrong (it could not read)
    it will add to the list OUTPUT 
    """
    problems = []
    for filename in listfilenames:
        p, n, t = get_pnt(filename)
        if t < 0:
            problems.append(filename)
    return problems

def get_pnt(listfilenames: Iterable[str], verbose=False) -> List[Tuple[int, int, float]]:
    """
    Given a folder, it makes a search in this folders, gets all the filenames
    Then it filters using the 'key':
        We search only in the files which has the 'key' inside it
    Then it returns a list with the data (p, n, t)
        p is the number os CPUs used
        n is the mesh size
        t is the time consumed by the algorithm
    """
    if isinstance(listfilenames, str):
        return get_pnt_single(listfilenames)
    ps, ns, ts = [], [], []
    for filename in listfilenames:
        p, n, t = get_pnt(filename)
        if t < 0:
            if verbose:
                print(f"For the file '{filename}', there was an error. Could not plot this value.")
            continue
        ps.append(p)
        ns.append(n)
        ts.append(t)
    ps = np.array(ps, dtype="int16")
    ns = np.array(ns, dtype="int32")
    ts = np.array(ts, dtype="float64")
    return ps, ns, ts


def test_logvieweventstable_allfiles(listfiles: List[str]):
    for filename in listfiles:
        table = get_logvieweventstable(filename)
        for key, item in table.items():
            if "p1" in filename and len(item) != 23:
                print("For file: ", filename)
                print("Error, it doesn't contain 23 elements, but %d" % len(item))
            elif "p1" not in filename and len(item) != 31:
                print("For file: ", filename)
                print("Error, it doesn't contain 31 elements, but %d" % len(item))
    # Para imprimir eventos que tem em p!=1, mas tem em p=2
    # events1 = []
    # events2 = []
    # for filename in listfiles:
    #     table = get_logviewtable(filename)
    #     if "p1" in filename:
    #         events1 = table["Event"]
    #     else:
    #         events2 = table["Event"]
    #     if len(events1) and len(events2):
    #         break
    # for event in events1:
    #     if event not in events2:
    #         print("Ha! ", event)
    # for event in events2:
    #     if event not in events1:
    #         print("Ho! ", event)

def test_logviewperformancetable_allfiles(listfiles: List[str]):
    for filename in listfiles:
        table = get_logviewperformancetable(filename)

def test_logviewmemorytable_allfiles(listfiles: List[str]):
    for filename in listfiles:
        table = get_logviewmemorytable(filename)

def all_results_folders():
    namefolders = ["results-e2highcpu8-01-09-2022",
                   "results-e2highcpu8-02-09-2022",
                   "results-e2highcpu8-13-08-2022",
                   "results-e2highcpu8-24-07-2022",
                   "results-e2highcpu8-30-08-2022",
                   "results-e2highmem8-06-09-2022",
                   "results-e2highmem8-08-09-2022",
                   "results-e2memory8-22-08-2022",
                   "results-e2memory8-23-08-2022",
                   "results-e2memory8-26-08-2022",
                   "results-e2standard8-12-08-2022",
                   "results-e2standard8-16-08-2022"]
    # namefolders = ["results-e2highcpu8-01-09-2022",
    #                "results-e2highcpu8-02-09-2022",
    #                "results-e2highcpu8-13-08-2022",
    #                "results-e2highcpu8-24-07-2022",
    #                "results-e2highcpu8-30-08-2022"]
    # namefolders = ["results-e2highmem8-06-09-2022",
    #                "results-e2highmem8-08-09-2022",
    #                "results-e2memory8-22-08-2022",
    #                "results-e2memory8-23-08-2022",
    #                "results-e2memory8-26-08-2022"]
    return namefolders

def get_listfiles_in_folders(folderslist: Iterable[str]):
    listallfilenames = []
    for foldername in folderslist:
        listfilenames = get_files(foldername)
        for filename in listfilenames:
            listallfilenames.append(foldername + "/" + filename)
    return listallfilenames

def main():
    """
    Para testar as funcoes
    """
    currentfolder = os.getcwd()
    currentfolder = currentfolder.replace("\\", "/")
    poissonfolder = currentfolder + "/Poisson/"
    folderslist = [poissonfolder + foldername for foldername in all_results_folders()]
    listallfilenames = get_listfiles_in_folders(folderslist)
    listallfilenames = filter_files(listallfilenames, "poisson2D")
    problemsfiles = get_problem_files(listallfilenames)
    listallgoodfilenames = []
    for filename in listallfilenames:
        if filename not in problemsfiles:
            listallgoodfilenames.append(filename)
    test_logvieweventstable_allfiles(listallgoodfilenames)
    test_logviewperformancetable_allfiles(listallgoodfilenames)
    test_logviewmemorytable_allfiles(listallgoodfilenames)


if __name__ == "__main__":
    main()