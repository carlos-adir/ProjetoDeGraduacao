#!/bin/bash
.SILENT:
.DEFAULT_GOAL := all
HOME_DIR=${HOME}
GIT_DIR=${HOME_DIR}/Git
PETSC_DIR=${GIT_DIR}/petsc
# PETSC_ARCH=arch-linux-c-debug
PETSC_ARCH=arch-linux-c-opt
MPIEXEC=${PETSC_DIR}/${PETSC_ARCH}/bin/mpiexec
include ${PETSC_DIR}/lib/petsc/conf/variables
include ${PETSC_DIR}/lib/petsc/conf/rules
CFLAGS += -pedantic -std=c99
pmax := 8
FOLDER?=${shell pwd}/results

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
	for nx in 100 128 200 256 300 350 400 500 512 550 600 700 750 850 950 1000 1100 1250 1300 1400 1500 2000; do \
		for p in {1..${pmax}}; do \
			ny=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny}"; \
			filename="${FOLDER}/$${code}-p$${p}-mesh$${nx}x$${ny}.txt"; \
			if [ ! -e $${filename} ]; then \
				executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -log_view"; \
				command="${MPIEXEC} -prepend-rank -np $${p} $${executeone}"; \
				{ \
					$${command} | cat >> $${filename}; \
				} 2>> $${filename}; \
			fi ; \
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
	for nx in 10 20 40 50 64 65 75 100 128 129 150 180 200 230 250 300 320 350 400; do \
		for p in {1..${pmax}}; do \
			ny=$$nx; \
			nz=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny} x $${nz}"; \
			filename="${FOLDER}/$${code}-p$${p}-mesh$${nx}x$${ny}x$${nz}.txt"; \
			if [ ! -e $${filename} ]; then \
				executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -da_grid_z $${nz} -log_view"; \
				command="${MPIEXEC} -prepend-rank -np $${p} $${executeone}"; \
				{ \
					$${command} | cat >> $${filename}; \
				} 2>> $${filename}; \
			fi ; \
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
			filename="${FOLDER}/$${code}-p$${p}-mesh$${nx}x$${ny}.txt"; \
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
			filename="${FOLDER}/$${code}-p$${p}-mesh$${nx}x$${ny}x$${nz}.txt"; \
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
	echo HOME_DIR=${HOME_DIR}
	echo GIT_DIR=${GIT_DIR}
	echo PETSC_DIR=${PETSC_DIR}
	echo PETSC_ARCH=${PETSC_ARCH}
	echo MPIEXEC=${MPIEXEC}
	echo FOLDER=${FOLDER}
	if [ ! -d ${FOLDER} ]; then mkdir -p ${FOLDER}; fi


pythonrenamefolder:
	python renamefolder.py

run: createfolder run2Dksp pythorenamefolder

runcolab2D: createfolder run2dkspcolab

runcolab3D: createfolder run3dkspcolab

distclean:
	@rm -f *~ poisson *tmp
