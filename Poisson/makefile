#!/bin/bash
.SILENT:
.DEFAULT_GOAL := all
PETSC_DIR=/home/carlosadir/Git/petsc/
# PETSC_ARCH=arch-linux-c-debug
PETSC_ARCH=arch-linux-c-opt
MPIEXEC=${PETSC_DIR}/${PETSC_ARCH}/bin/mpiexec
include ${PETSC_DIR}/lib/petsc/conf/variables
include ${PETSC_DIR}/lib/petsc/conf/rules
CFLAGS += -pedantic -std=c99
pmax := 2
folder := "results"

all: run distclean

compilepoisson2D_ksp: poisson2D_ksp.o
	-${CLINKER} -o poisson2D_ksp poisson2D_ksp.o ${PETSC_LIB}
	${RM} poisson2D_ksp.o

compilepoisson2D_snes: poisson2D_snes.o
	-${CLINKER} -o poisson2D_snes poisson2D_snes.o ${PETSC_LIB}
	${RM} poisson2D_snes.o

compilepoisson3D_ksp: poisson3D_ksp.o
	-${CLINKER} -o poisson3D_ksp poisson3D_ksp.o ${PETSC_LIB}
	${RM} poisson3D_ksp.o

run2Dksp: createfolder compilepoisson2D_ksp
	{ \
	set -e ;\
	code="poisson2D_ksp";\
	echo "For code $${code}";\
	for p in {1..${pmax}}; do \
		for nx in 100 128 200 256 300 350 400 500 512 550 600 700 750 850 950 1000 1100 1250 1300 1400 1500 2000; do \
			ny=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny}"; \
			filename="${folder}/$${code}-p$${p}-mesh$${nx}x$${ny}.txt"; \
			if [ -e $${filename} ]; then rm $${filename} ; fi ; \
			executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -log_view"; \
			command="${MPIEXEC} -prepend-rank -np $${p} time -p $${executeone}"; \
			{ \
				$${command} | cat >> $${filename}; \
			} 2>> $${filename}; \
		done \
	done \
	}


run2Dsnes: createfolder compilepoisson2D_snes
	echo "Ham"

run3Dksp: createfolder compilepoisson3D_ksp
	{ \
	set -e ;\
	code="poisson3D_ksp";\
	echo "For code $${code}";\
	for p in {1..${pmax}}; do \
		for nx in 10 20 40 50 64 65 75 100 128 129 150 180 200 230 250 300 320 350 400; do \
			ny=$$nx; \
			nz=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny} x $${nz}"; \
			filename="${folder}/$${code}-p$${p}-mesh$${nx}x$${ny}x$${nz}.txt"; \
			if [ -e $${filename} ]; then rm $${filename} ; fi ; \
			executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -da_grid_z $${nz} -log_view"; \
			command="${MPIEXEC} -prepend-rank -np $${p} time -p $${executeone}"; \
			{ \
				$${command} | cat >> $${filename}; \
			} 2>> $${filename}; \
		done \
	done \
	}



run2Dkspcolab: createfolder compilepoisson2D_ksp
	{ \
	set -e ;\
	code="poisson2D_ksp";\
	echo "For code $${code}";\
	for p in {1..${pmax}}; do \
		for nx in 100 128 200 256 300 350 400 500 512 550 600 700 750 850 950 1000; do \
			ny=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny}"; \
			filename="${folder}/$${code}-p$${p}-mesh$${nx}x$${ny}.txt"; \
			if [ -e $${filename} ]; then rm $${filename} ; fi ; \
			executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -log_view"; \
			command="${MPIEXEC} -prepend-rank -np $${p} $${executeone}"; \
			{ \
				$${command} | cat >> $${filename}; \
			} 2>> $${filename}; \
		done \
	done \
	}


run3Dkspcolab: createfolder compilepoisson3D_ksp
	{ \
	set -e ;\
	code="poisson3D_ksp";\
	echo "For code $${code}";\
	for p in {1..${pmax}}; do \
		for nx in 10 20 40 50 64 65 75 100 128 129 150 180 200; do \
			ny=$$nx; \
			nz=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny} x $${nz}"; \
			filename="${folder}/$${code}-p$${p}-mesh$${nx}x$${ny}x$${nz}.txt"; \
			if [ -e $${filename} ]; then rm $${filename} ; fi ; \
			executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -da_grid_z $${nz} -log_view"; \
			command="${MPIEXEC} -prepend-rank -np $${p} $${executeone}"; \
			{ \
				$${command} | cat >> $${filename}; \
			} 2>> $${filename}; \
		done \
	done \
	}

createfolder:
	if [ ! -d ${folder} ]; then mkdir -p ${folder}; fi
	echo PETSC_DIR=${PETSC_DIR}
	echo PETSC_ARCH=${PETSC_ARCH}
	echo MPIEXEC=${MPIEXEC}


pythonrenamefolder:
	python renamefolder.py

run: createfolder run2Dksp run3Dksp pythonrenamefolder

runcolab2D: createfolder run2dkspcolab

runcolab3D: createfolder run3dkspcolab

distclean:
	@rm -f *~ poisson *tmp
