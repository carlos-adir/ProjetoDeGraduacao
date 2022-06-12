.DEFAULT_GOAL := all
include ${PETSC_DIR}/lib/petsc/conf/variables
include ${PETSC_DIR}/lib/petsc/conf/rules
CFLAGS += -pedantic -std=c99

all: run distclean

poisson2D_ksp: poisson2D_ksp.o
	-${CLINKER} -o poisson2D_ksp poisson2D_ksp.o ${PETSC_LIB}
	${RM} poisson2D_ksp.o

poisson2D_snes: poisson2D_snes.o
	-${CLINKER} -o poisson2D_snes poisson2D_snes.o ${PETSC_LIB}
	${RM} poisson2D_snes.o

poisson3D_ksp: poisson3D_ksp.o
	-${CLINKER} -o poisson3D_ksp poisson3D_ksp.o ${PETSC_LIB}
	${RM} poisson3D_ksp.o

run: poisson2D_ksp poisson2D_snes poisson3D_ksp
	python run.py

distclean:
	@rm -f *~ poisson *tmp
