import os

if __name__ == "__main__":
	nx = 248 + 1
	ny = 248 + 1
	Pmax = 16
	codes = ["poisson2D_ksp", "poisson2D_snes", "poisson3D_ksp"]
	command = "mpiexec -n %d ./%s -da_grid_x %d -da_grid_y %d"
	os.system("mkdir results")
	for code in codes:
		for p in range(1, Pmax+1):
			filename = "results/%s-%d.txt" % (code, p)
			newcommand = command % (p, code, nx, ny)
			os.system("{ time %s; } 2>&1 |  cat > %s" % (newcommand, filename))

