include ${PETSC_DIR}/lib/petsc/conf/variables
include ${PETSC_DIR}/lib/petsc/conf/rules
FORTRAN = gfortran
CFLAGS += -pedantic -std=c99

echopetsc:
	@echo ${PETSC_DIR}
	@echo ${PETSC_LIB}
	@echo ${FLINKER}
	@echo ${RM}



helloworld: compilehelloworld runhelloworld

# compilehelloworld: 
#     ${FORTRAN} helloworld.f90 -o helloworld

# runhelloworld:
#     ./helloworld

compute_euler: compute_euler.o
	-${CLINKER} -o compute_euler compute_euler.o ${PETSC_LIB}
	${RM} compute_euler.o

hello: hello.o 
	${FLINKER} -o hello hello.o  ${PETSC_LIB}
	${RM} hello.o

# matriz: matriz.o chkopts
#   -${FLINKER} -o matriz matriz.o  ${PETSC_LIB}
#   ${RM} matriz.o

# all:
#   matriz