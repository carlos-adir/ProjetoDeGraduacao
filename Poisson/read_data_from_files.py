import re
from os import listdir
from os.path import isfile, join
from typing import List, Tuple

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
    with open(filename) as file:
        lines = file.readlines()
    return '\n'.join(lines)

def filter_files(listfilesnames: List[str], key: str):
    newlistfilesnames = []
    for filename in listfilesnames:
        if key in filename:
            newlistfilesnames.append(filename)
    return newlistfilesnames

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