import re
import os
from os import listdir
from os.path import isfile, join
from typing import List, Tuple, Dict

def get_files(folder: str) -> List[str]:
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
    newlistfilesnames = []
    for filename in listfilesnames:
        if key in filename:
            newlistfilesnames.append(filename)
    return newlistfilesnames

def get_logview_table(filename: str) -> Dict:
    texto = readfile(filename)
    regexlinha = r"\[0\] ([a-zA-Z]+) \s+([0-9\s.e+-]+)\[0\] ?\n"
    encontros = re.findall(regexlinha, texto)
    for i, e in enumerate(encontros):
        nome = e[0]
        numeros = e[1].split(" ")
        while '' in numeros:
            numeros.remove('')
        for j, n in enumerate(numeros):
            try:
                numeros[j] = float(n)
            except ValueError:
                indexe = n.index("e")
                numeros[j] = float(n[:indexe+3])
        print("nome = ", nome)
        # print("numeros = ", numeros)
        print("len(numeros) = ", len(numeros))

def get_pnt(filename: str) -> Tuple[int, int, float]:
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
    t = float(re.findall(r"Processor 0 took ((\d+\.?\d*)|(\.\d+)) CPU seconds", texto)[0][0])
    return p, n, t

def get_problem_files(folder: str) -> List[str]:
    filenames = get_files(folder)
    problems = []
    for filename in filenames:
        try:
            p, n, t = get_pnt(folder + "/" + filename)
        except Exception as e:
            problems.append(filename)
    return problems

def getdata_pnt(folder: str, key: str) -> List[Tuple[int, int, float]]:
    """
    Given a folder, it makes a search in this folders, gets all the filenames
    Then it filters using the 'key':
        We search only in the files which has the 'key' inside it
    Then it returns a list with the data (p, n, t)
        p is the number os CPUs used
        n is the mesh size
        t is the time consumed by the algorithm
    """
    allfiles = get_files(folder)
    filenames = filter_files(allfiles, key)
    results = []
    for filename in filenames:
        try:
            p, n, t = get_pnt(folder + "/" + filename)
            results.append((p, n, t))
        except Exception as e:
            print(f"For the file '{filename}', there was an error. Could not plot this value.")
    return results




def main():
    """
    Para testar as funcoes
    """
    currentfolder = os.getcwd()
    currentfolder = currentfolder.replace("\\", "/")
    foldername = "Poisson/results-e2highcpu8-13-08-2022"
    filename = "poisson2D_ksp-p6-mesh129x129.txt"
    completefilename = currentfolder + "/" + foldername + "/" + filename
    get_logview_table(completefilename)



if __name__ == "__main__":
    main()