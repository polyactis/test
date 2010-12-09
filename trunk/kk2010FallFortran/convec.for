      SUBROUTINE CONVEC(RE,UU,VV)
C
C     EVALUATES RIGHT-HAND SIDE OF THE
C     UNSTEADY HEAT CONDUCTION EQUATION
C
	DIMENSION UU(41,41),VV(41,41),FU(41,41),FV(41,41)
      COMMON DX,DY,NX,NY,R,U,DU,V,DV,P,FU,FV,FUP,FVP,ALF,CCXA,CCYA,DVE

C
	NXP=NX-1
	NYP=NY-1
	NXS=NX+1
C
      DO 5 J =2,NXP
      DO 4 K = 2,NYP
      FU(K,J) = 3./RE - UU(K,J)*(UU(K,J+1)-UU(K,J-1))/(2.*DX)
     1 - VV(K,J)*(UU(K+1,J)-UU(K-1,J))/(2.*DY) 
	FV(K,J) = 0. - UU(K,J)*(VV(K,J+1)-VV(K,J-1))/(2.*DX)
     1 - VV(K,J)*(VV(K+1,J)-VV(K-1,J))/(2.*DY)
    4	CONTINUE
    5 CONTINUE

	DO 6 K =2,NYP
    	FU(K,NX) = 3./RE - UU(K,NX)*(UU(K,NXS)-UU(K,NXP))/(2.*DX)
    6	CONTINUE

      RETURN
      END

