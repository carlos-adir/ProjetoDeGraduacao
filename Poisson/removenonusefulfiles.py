import os
from os import listdir
from os.path import isfile, join
import re
import numpy as np

def get_files(folder):
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    return onlyfiles

def readfile(filename):
    with open(filename) as file:
        lines = file.readlines()
    return '\n'.join(lines)

def delete_command(filename: str):
    return "rm " + filename

def data2Dksp(folder):
    files = get_files(folder)
    files2D = []
    for file in files:
        if "2D_ksp" in file:
            files2D.append(file)
    for filename in files2D:
        try:
            p = int(filename.split("-p")[1].split("-mesh")[0])
            n = int(filename.split("mesh")[1].split("x")[0])
            texto = readfile(folder + "/" + filename)
            t = float(re.findall(r"Processor 0 took ((\d+\.?\d*)|(\.\d+)) CPU seconds", texto)[0][0])
        except Exception as e:
            command = delete_command(folder + "/" + filename)
            os.system(command)

def data3Dksp(folder):
    print(f"folder = {folder}")
    files = get_files(folder)
    files3D = []
    for file in files:
        if "3D_ksp" in file:
            print("file = ", file)
            files3D.append(file)
    for filename in files3D:
        try:
            p = int(filename.split("-p")[1].split("-mesh")[0])
            n = int(filename.split("mesh")[1].split("x")[0])
            texto = readfile(folder + "/" + filename)
            t = float(re.findall(r"Processor 0 took ((\d+\.?\d*)|(\.\d+)) CPU seconds", texto)[0][0])
        except Exception as e:
            command = delete_command(folder + "/" + filename)
            os.system(command)


if __name__ == "__main__":
    import sys
    mainfolder = (sys.argv[0]).replace("removenonusefulfiles.py", "")
    folder = mainfolder + "results_googlecloud8-2022-07-24"
    data2Dksp(folder)
    data3Dksp(folder)
