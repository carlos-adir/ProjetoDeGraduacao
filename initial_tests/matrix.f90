%%writefile matriz.F90
       program matriz
#include <petsc/finclude/petscvec.h>
#include <petsc/finclude/petscmat.h>
      use petscvec
      use petscmat

      PetscInt:: j(4)=(/0,1,2,3/)
      PetscScalar:: vb(4)=(/1.,3.,4.,1./)
      PetscScalar:: ma(4,4)
      Vec         b
      Mat         A

      ma(1,:)=(/1.,3.,4.,1./)
      ma(2,:)=(/9.,3.,2.,1./)
      ma(3,:)=(/1.,6.,5.,9./)
      ma(4,:)=(/3.,4.,4.,3./)      
    
      call PetscInitialize(PETSC_NULL_CHARACTER,ierr)
      if (ierr .ne. 0) then
        print*,'Unable to initialize PETSc'
        stop
      endif


!  Create a parallel vector

      call VecCreateMPI(PETSC_COMM_WORLD,PETSC_DECIDE,4,b,ierr)
      call VecSetFromOptions(b,ierr)
      call VecSetValues(b,4,j,vb,INSERT_VALUES,ierr)
      call VecAssemblyBegin(b,ierr)
      call VecAssemblyEnd(b,ierr)

!  Create a parallel matrix    
      call MatCreate(PETSC_COMM_WORLD,A,ierr)
      call MatSetSizes(A,PETSC_DECIDE,PETSC_DECIDE,4,4,ierr)
      call MatSetFromOptions(A,ierr)
      call MatSetUp(A,ierr)
      do i=0,3
          call MatSetValues(A,1,i,4,j,ma(i+1,:),INSERT_VALUES,ierr)
      end do
      call MatAssemblyBegin(A,MAT_FINAL_ASSEMBLY,ierr)
      call MatAssemblyEnd(A,MAT_FINAL_ASSEMBLY,ierr)
      call MatView(A,PETSC_VIEWER_STDOUT_WORLD,ierr)
      call MatDestroy(A,ierr)
      call VecDestroy(b,ierr)
      call PetscFinalize(ierr)
      end program matriz