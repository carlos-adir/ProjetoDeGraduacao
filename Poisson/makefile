#!/bin/bash
.SILENT:
.DEFAULT_GOAL := all
PETSC_DIR=/home/carlosadir/Git/petsc/
PETSC_ARCH=arch-linux-c-debug
# PETSC_ARCH=arch-linux-c-opt
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

run2Dksp: compilepoisson2D_ksp
	{ \
	set -e ;\
	code="poisson2D_ksp";\
	echo "For code $${code}";\
	for p in {1..${pmax}}; do \
		for nx in 200; do \
			ny=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny}"; \
			filename="${folder}/$${code}-p$${p}-mesh$${nx}x$${ny}.txt"; \
			if [ -e $${filename} ]; then rm $${filename} ; fi ; \
			executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -log_view"; \
			command="mpiexec --tag-output -np $${p} time -p $${executeone}"; \
			{ \
				$${command} | cat >> $${filename}; \
			} 2>> $${filename}; \
		done \
	done \
	}


run2Dsnes: compilepoisson2D_snes
	echo "Ham"

run3Dksp: compilepoisson3D_ksp
	{ \
	set -e ;\
	code="poisson3D_ksp";\
	echo "For code $${code}";\
	for p in {1..${pmax}}; do \
		for nx in 10; do \
			ny=$$nx; \
			nz=$$nx; \
			echo "    With $${p} processors and mesh $${nx} x $${ny} x $${nz}"; \
			filename="${folder}/$${code}-p$${p}-mesh$${nx}x$${ny}x$${nz}.txt"; \
			if [ -e $${filename} ]; then rm $${filename} ; fi ; \
			executeone="./$${code} -da_grid_x $${nx} -da_grid_y $${ny} -da_grid_z $${nz} -log_view -start_in_debugger"; \
			command="mpiexec --tag-output -np $${p} time -p $${executeone}"; \
			{ \
				$${command} | cat >> $${filename}; \
			} 2>> $${filename}; \
		done \
	done \
	}

createfolder:
	if [ ! -d ${folder} ]; then mkdir -p ${folder}; fi

run: createfolder run3Dksp

distclean:
	@rm -f *~ poisson *tmp
