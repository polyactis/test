
      SUBROUTINE PRESS(A)
C
C     EVALUATES THE COEEFICIANT MATRIX OF THE PRUSSURE EQUATIONS
C	AND CONVERT MATRIX D(J,K) TO VECTOR DVE(M)
C
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
C
C     FOR INNER NODES
      DO 4 J = 2,NXP
	JM = J - 1
	DO 3 K = 2,NYP
	M = JM*NY + K
      A(M,M) =  2./(DX*DX) + 2./(DY*DY)
	A(M-1,M) = -1./(DY*DY)
	A(M+1,M) = -1./(DY*DY)
      A(M-NY,M) = -1./(DX*DX)
	A(M+NY,M) = -1./(DX*DX)
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
	A((NX-1)*NY+1,(NX-1)*NY+1) = 2.
	A((NX-1)*NY+2,(NX-1)*NY+1) = -1.
	A((NX-2)*NY+1,(NX-1)*NY+1) = -1.

C	FOR (NX,NY) NODE
      A(NXY,NXY) = 1.

C	LEFT BOUNDARY NODES
	DO 5 K= 2,NYP
	A(K,K) = 2./(DX*DX) + 2./(DY*DY)
	A(K-1,K) = -1./(DY*DY)
	A(K+1,K) = -1./(DY*DY)
	A(K+NY,K) = -2./(DX*DX)
    5	CONTINUE

C	LOWER BOUNDARY NODES
	DO 6 J=2,NXP
	A((J-1)*NY+1,(J-1)*NY+1) = 2./(DX*DX) + 2./(DY*DY)
	A((J-1)*NY+2,(J-1)*NY+1) = -2./(DY*DY)
	A(J*NY+1,(J-1)*NY+1) = -1./(DX*DX)
	A((J-2)*NY+2,(J-1)*NY+1) = -1./(DX*DX)
    6	CONTINUE

C	RIGHT BOUNDARY NODES
	DO 7 K= 2,NYP
 	A((NX-1)*NY+K,(NX-1)*NY+K) = 2./(DX*DX) + 2./(DY*DY)
	A((NX-1)*NY+K-1,(NX-1)*NY+K) = -1./(DY*DY)
	A((NX-1)*NY+K+1,(NX-1)*NY+K) = -1./(DY*DY)
	A((NX-2)*NY+K,(NX-1)*NY+K) = -2./(DX*DX)
    7	CONTINUE

C	UPPER BOUNDARY NODES
	DO 8 J= 2,NXP
 	A(J*NY,J*NY) = 2./(DX*DX) + 2./(DY*DY)
	A(J*NY-1,J*NY) = -2./(DY*DY)
	A((J-1)*NY,J*NY) = -1./(DX*DX)
	A((J+1)*NY,J*NY) = -1./(DX*DX)
    8	CONTINUE

C	CONVERT D(J,K) TO DVE(M)

C	DO 10 J = 1,NX
C	DO 9 K = 1,NY
C	DVE((J-1)*NY+K) = D(K,J)
C    9	CONTINUE
C   10	CONTINUE
C
      RETURN
      END

