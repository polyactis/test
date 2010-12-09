      SUBROUTINE REDIF(AA,DTIM,NXN,NYN,T)
C
C     EVALUATES RIGHT-HAND SIDE OF THE
C     STEADY FLOW EQUATION IN BOTH X AND Y DIRECTIONS
C
      DIMENSION DMX(3,3),DMY(3,3),EMX(3),EMY(3),R(41,41),T(41,41)
      COMMON DX,DY,NX,NY,R,U,DU,V,DV,P,FU,FV,FUP,FVP,ALF,CCXA,CCYA,DVE
	CCX = AA/DX/DX
      CCY = AA/DY/DY
	EMX(1) = 0.
	EMX(2) = 1.
	EMX(3) = 0.
	EMY(1) = 0.
 	EMY(2) = 1.
	EMY(3) = 0.
	

      DO 1 I = 1,3
      DMX(I,1) = CCX*EMY(I)
      DMX(I,2) = -2.*DMX(I,1)
      DMX(I,3) = DMX(I,1)
      DMY(1,I) = CCY*EMX(I)
      DMY(2,I) = -2.*DMY(1,I)
    1 DMY(3,I) = DMY(1,I)
C
      DO 5 J =2,NXN
      DO 4 K = 2,NYN
      RTD = 0.
      DO 3 M = 1,3
      MJ = J - 2 + M
      DO 2 N = 1,3
      NK = K - 2 + N
    2 RTD = RTD + (DMX(N,M)+DMY(N,M))*T(NK,MJ)*DTIM
    3 CONTINUE
    4 R(K,J) = RTD
    5 CONTINUE
      RETURN
      END

