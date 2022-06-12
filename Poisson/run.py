import os

if __name__ == "__main__":
	
	Pmax = 16
	codes = ["poisson2D_ksp", "poisson2D_snes", "poisson3D_ksp"]
	os.system("mkdir results")
	for code in codes:
		for p in range(1, Pmax+1):
			command = "mpiexec -n %d ./%s"% (p, code)
			if "2D" in code:
				nx = 2048 + 1
				ny = 2048 + 1
				nz = 2048 + 1
				command += " -da_grid_x %d -da_grid_y %d" % (nx, ny)
			if "3D" in code:
				nx = 512 + 1
				ny = 512 + 1
				nz = 512 + 1
				command += " -da_grid_x %d -da_grid_y %d -da_grid_z %s" % (nx, ny, nz)
			filename = "results/%s-%d.txt" % (code, p)
			os.system("{ time %s; } 2>&1 |  cat > %s" % (newcommand, filename))

