import os
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import numpy as np
import matplotlib.ticker as mticker

# My axis should display 10⁻¹ but you can switch to e-notation 1.00e+01
def log10_tick_formatter(val, pos=None):
    return f"$10^{{{int(val)}}}$"  # remove int() if you don't use MaxNLocator
    # return f"{10**val:.2e}"      # e-Notation
def log2_tick_formatter(val, pos=None):
    return f"${2**int(val)}$" # remove int() if you don't use MaxNLocator
    # return f"{10**val:.2e}"      # e-Notation

def get_files(folder):
	onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
	return onlyfiles

def readfile(filename):
	with open(filename) as file:
		lines = file.readlines()
	return '\n'.join(lines)

def show2D_ksp():
	files = get_files(folder)
	files2D = []
	for file in files:
		if "2D_ksp" in file:
			files2D.append(file)
	# Plotaremos um grafico com 
	# eixo X: Numero de processadores (log)
	# eixo Y: Numero de pontos da malha (log)
	# eixo Z: Tempo necessário (log)
	fig = plt.figure(figsize=(4,4))
	ax = fig.add_subplot(111, projection='3d')
	pmax = 1
	nmin = 1e+6
	nmax = 1
	tmin = 1e+6
	tmax = 1
	for filename in files2D:
		try:
			p = int(filename.split("-p")[1].split("-mesh")[0])
			n = int(filename.split("mesh")[1].split("x")[0])
			texto = readfile(folder + "/" + filename)
			t = float(re.findall(r"<stdout>:Processor 0 took ((\d+\.?\d*)|(\.\d+)) CPU seconds", texto)[0][0])
			p = np.log2(p)
			n = np.log10(n)
			t = np.log10(t)
			if p > pmax:
				pmax = p
			if nmin > n:
				nmin = n
			if nmax < n:
				nmax = n
			if t > tmax:
				tmax = t
			if t < tmin:
				tmin = t

			ax.scatter(p,n,t, color="k") # plot the point (2,3,4) on the figure
		except Exception as e:
			print(f"For the file '{filename}', there was an error. Could not plot this value.")
			raise e
	print("Para o 2D:")
	print(f"    pmin, pmax = 1, {2**pmax}")
	print(f"    nmin, nmax = {int(10**nmin)}, {int(10**nmax)}")
	print(f"    tmin, tmax = %.2f %.2f" % (10**tmin, 10**tmax))
	ax.set_xlabel(r"Número de processadores $p$")
	ax.set_ylabel(r"Malha $n$")
	ax.set_zlabel(r"Tempo $t$ (s)")
	ax.set_xlim(0,pmax)
	ax.set_ylim(nmin,nmax)
	ax.set_zlim(tmin,tmax)
	ax.xaxis.set_major_formatter(mticker.FuncFormatter(log2_tick_formatter))
	ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
	ax.yaxis.set_major_formatter(mticker.FuncFormatter(log10_tick_formatter))
	ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
	ax.zaxis.set_major_formatter(mticker.FuncFormatter(log10_tick_formatter))
	ax.zaxis.set_major_locator(mticker.MaxNLocator(integer=True))
	plt.title("Resultados 2D - 2022 julho 04 - 11:02")
	plt.show()




def show3D_ksp():
	files = get_files(folder)
	files3D = []
	for file in files:
		if "3D_ksp" in file:
			files3D.append(file)
	fig = plt.figure(figsize=(4,4))
	ax = fig.add_subplot(111, projection='3d')
	pmax = 1
	nmin = 1e+6
	nmax = 1
	tmin = 1e+6
	tmax = 1
	for filename in files3D:
		try:
			p = int(filename.split("-p")[1].split("-mesh")[0])
			n = int(filename.split("mesh")[1].split("x")[0])
			texto = readfile(folder + "/" + filename)
			t = float(re.findall(r"<stdout>:Processor 0 took ((\d+\.?\d*)|(\.\d+)) CPU seconds", texto)[0][0])
			p = np.log2(p)
			n = np.log10(n)
			t = np.log10(t)
			if p > pmax:
				pmax = p
			if nmin > n:
				nmin = n
			if nmax < n:
				nmax = n
			if t > tmax:
				tmax = t
			if t < tmin:
				tmin = t
			ax.scatter(p,n,t, color="k") # plot the point (2,3,4) on the figure
		except Exception as e:
			print(f"For the file '{filename}', there was an error. Could not plot this value.")
			# raise e
	print("Para o 3D:")
	print(f"    pmin, pmax = 1, {2**pmax}")
	print(f"    nmin, nmax = {int(10**nmin)}, {int(10**nmax)}")
	print(f"    tmin, tmax = %.2f %.2f" % (10**tmin, 10**tmax))
	ax.set_xlabel(r"Número de processadores $p$")
	ax.set_ylabel(r"Malha $n$")
	ax.set_zlabel(r"Tempo $t$ (s)")
	ax.set_xlim(0,pmax)
	ax.set_ylim(nmin,nmax)
	ax.set_zlim(tmin,tmax)
	ax.xaxis.set_major_formatter(mticker.FuncFormatter(log2_tick_formatter))
	ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
	ax.yaxis.set_major_formatter(mticker.FuncFormatter(log10_tick_formatter))
	ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
	ax.zaxis.set_major_formatter(mticker.FuncFormatter(log10_tick_formatter))
	ax.zaxis.set_major_locator(mticker.MaxNLocator(integer=True))
	plt.title("Resultados 3D - 2022 julho 04 - 11:02")
	

if __name__ == "__main__":
	folder = "results_2022-07-04-11-02"
	show2D_ksp()
	show3D_ksp()
	plt.show()