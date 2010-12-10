      SUBROUTINE CONVEC(RE, UU, VV, NX, NY)
C
C     EVALUATES RIGHT-HAND SIDE OF THE
C     UNSTEADY HEAT CONDUCTION EQUATION
C
	IMPLICIT NONE
	REAL, DIMENSION(41,41) :: UU, VV, FU, FV
	REAL, INTENT(IN) :: RE
	INTEGER :: NXP, NYP, NXS, NX, NY, J, K
	REAL :: DX, DY
C      COMMON DX,DY,NX,NY,R,U,DU,V,DV,P,FU,FV,FUP,FVP,ALF,CCXA,CCYA,DVE

C
	NXP=NX-1
	NYP=NY-1
	NXS=NX+1
C
      DO J =2,NXP
      DO K = 2,NYP
      	FU(K,J) = 3./RE - UU(K,J)*(UU(K,J+1)-UU(K,J-1))/(2.*DX)
     1 - VV(K,J)*(UU(K+1,J)-UU(K-1,J))/(2.*DY) 
	FV(K,J) = 0. - UU(K,J)*(VV(K,J+1)-VV(K,J-1))/(2.*DX)
     1 - VV(K,J)*(VV(K+1,J)-VV(K-1,J))/(2.*DY)
      END DO
      END DO

	DO K =2,NYP
    	FU(K,NX) = 3./RE - UU(K,NX)*(UU(K,NXS)-UU(K,NXP))/(2.*DX)
    	END DO

      RETURN
      END

