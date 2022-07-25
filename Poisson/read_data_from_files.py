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

def getdata_2Dksp(folder: str) -> List[Tuple[int, int, float]]:
    files = get_files(folder)
    files2D = filter_files(files, "2D_ksp")
    results = []
    for filename in files2D:
        try:
            p, n, t = get_pnt(folder + "/" + filename)
            results.append((p, n, t))
        except Exception as e:
            print(f"For the file '{filename}', there was an error. Could not plot this value.")
    return results


def getdata_3Dksp(folder: str) -> List[Tuple[int, int, float]]:
    files = get_files(folder)
    files3D = filter_files(files, "3D_ksp")
    results = []
    for filename in files3D:
        try:
            p, n, t = get_pnt(folder + "/" + filename)
            results.append((p, n, t))
        except Exception as e:
            print(f"For the file '{filename}', there was an error. Could not plot this value.")
    return results
