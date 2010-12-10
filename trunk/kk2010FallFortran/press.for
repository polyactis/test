
      SUBROUTINE PRESS(A)
C
C     EVALUATES THE COEEFICIANT MATRIX OF THE PRUSSURE EQUATIONS
C	AND CONVERT MATRIX D(J,K) TO VECTOR DVE(M)
C
	REAL*8 aa,b,c,dd,e
	DIMENSION D(41,41),DVE(1600),A(1600,1600)			  
	COMMON DX,DY,NX,NY,R,U,DU,V,DV,P,FU,FV,FUP,FVP,ALF,CCXA,CCYA,DVE
C

	NXP=NX-1
	NYP=NY-1
      NXY = NX*NY
      DO 2 M = 1,NXY
C	DVE(M) = 0.
      DO 1 N = 1,NXY
    1 A(N,M) = 0.
    2 CONTINUE
	
	aa = -1./(DX*DX)
	b = -1./(DY*DY)
	c = 2./(DX*DX) + 2./(DY*DY)
	dd = -1./(DY*DY)
	e = -1./(DX*DX)
C
C     FOR INNER NODES
      DO 4 J = 2,NXP
	JM = J - 1
	DO 3 K = 2,NYP
	M = JM*NY + K
	A(JM*NY+K, M) = c
	A((JM-1)*NY+K, M) = aa
	A(JM*NY+K-1, M) = b
	A((JM+1)*NY+K, M) = dd
	A(JM*NY+K+1, M) = e
    3 CONTINUE
    4 CONTINUE

C	FOR (1,1) NODE
	A(1,1) = 2.
	A(2,1) = -1.
	A(NY+1,1) = -1.

C     FOR (1,NY) NODE
	A(NY,NY) = 2.
	A(NY-1,NY) = -1. 
	A(NY+NY,NY) = -1.

C     FOR (NX,1) NODE
	A((NX-1)*NY+1, (NX-1)*NY+1) = 2.
	A((NX-2)*NY+1, (NX-1)*NY+1) = -1.
	A((NX-1)*NY+2, (NX-1)*NY+1) = -1.

C	FOR (NX,NY) NODE
      A(NXY,NXY) = 1.

C	LEFT BOUNDARY NODES
	DO 5 K= 2,NYP
	M = K
	A(K-1, M) = aa
	A(K, M) = c
	A(K+1, M) = dd
	A(K+NY, M) = aa + e
    5	CONTINUE

C	LOWER BOUNDARY NODES
	DO 6 J=2,NXP
	M = (J-1)*NY+1
	A((J-2)*NY+1, M) = aa
	A((J-1)*NY+1, M) = c
	A((J-1)*NY+2, M) = b+dd
	A(J*NY+1, M) = e
    6	CONTINUE

C	RIGHT BOUNDARY NODES
	DO 7 K= 2,NYP
	M = (NX-1)*NY + K
	A((NX-2)*NY+K, M) = aa+e
	A((NX-1)*NY+K-1, M) = b
 	A((NX-1)*NY+K, M) = c
	A((NX-1)*NY+K+1, M) = dd
    7	CONTINUE

C	UPPER BOUNDARY NODES
	DO 8 J= 2,NXP
 	M = (J-1)*NY + NY
	A((J-2)*NY+NY, M) = aa
	A((J-1)*NY+NY-1, M) = b+dd
	A((J-1)*NY+NY, M) = c
	A((J+1-1)*NY+NY, M) = e
    8	CONTINUE

	A = TRANSPOSE(A)
      RETURN
      END

