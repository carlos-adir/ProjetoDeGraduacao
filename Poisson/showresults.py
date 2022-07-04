import os
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt


def get_files(folder):
	onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
	return onlyfiles

def show2D_ksp():
	files = get_files("results")
	files2D = []
	for file in files:
		if "2D_ksp" in file:
			files2D.append(file)
	print(files2D)

def show3D_ksp():
	files = get_files("results")
	files3D = []
	for file in files:
		if "3D_ksp" in file:
			files3D.append(file)
	print(files3D)

if __name__ == "__main__":
	show2D_ksp()
	show3D_ksp()