#include <petsc.h>

/* To compile and execute, use

*/

int main(int argc, char **argv){
	PetscErrorCode ierr;
	PetscMPIInt rank;
	PetscInt i;
	PetscReal localval, globalsum;

	PetscInitialize(&argc, &argv, NULL, "Compute e in parallel with PETSc.\n\n");
	ierr = MPI_Comm_rank(PETSC_COMM_WORLD, &rank); CHKERRQ(ierr);

	localval = 1.0;
	for (i = 2; i < rank + 1; i++)
		localval /= i;

	ierr = MPI_Allreduce(&localval, &globalsum, 1, MPIU_REAL, MPIU_SUM, PETSC_COMM_WORLD);
	CHKERRQ(ierr);

	ierr = PetscPrintf(PETSC_COMM_WORLD, "e is about %17.15f\n", globalsum);
	CHKERRQ(ierr);

	ierr = PetscPrintf(PETSC_COMM_SELF, "rank %d did %d flops\n", rank, rank ? rank-1 : 0);
	CHKERRQ(ierr);





	return PetscFinalize();
}		
