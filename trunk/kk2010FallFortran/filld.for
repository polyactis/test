      SUBROUTINE FILLD(NX, NY, U, V, D, DX, DY, DTIM, DVE)
C
C     EVALUATES RIGHT-HAND SIDE OF THE
C     UNSTEADY HEAT CONDUCTION EQUATION
C
	IMPLICIT NONE
	REAL, DIMENSION (41,41) :: D, U, V
	REAL, DIMENSION (1600), INTENT(OUT) :: DVE
	REAL, INTENT(IN) :: DX, DY, DTIM
	INTEGER, INTENT(IN) :: NX, NY
	INTEGER :: K, J
C     COMPUTE D(K,J)
	DO 20 K=1,NY
	DO 19 J=1,NX
	D(K,J) = 0.
   19	CONTINUE
   20 CONTINUE
     
      DO 22 K=2,NY
	DO 21 J=2,NX 
	D(K,J) = (U(K,J) - U(K,J-1))/DX
   	D(K,J) = D(K,J) + (V(K,J) - V(K-1,J))/DY
   	D(K,J) = -1.*D(K,J)/DTIM
   21	CONTINUE
   22 CONTINUE

	DO 23 J=1,NX
		D(1,J) = 0.
		D(NY,J) =0.
   23	CONTINUE
   
   	DO 24 K=1,NY
	D(K,1) = 0.
   24	D(K,NX) =0.

	D(NY-1,NX) = D(NY-1,NX) + 1./(DY*DY)
	D(NY,NX-1) = D(NY,NX-1) + 1./(DX*DX)
	D(NY,NX) = 1.

C	CONVERT D(J,K) TO DVE(M)

C	DO 10 J = 1,NX
C	DO 9 K = 1,NY
C	DVE((J-1)*NY+K) = D(K,J)
C     9	CONTINUE
C    10	CONTINUE
	D = TRANSPOSE(D)
      RETURN
      END SUBROUTINE FILLD
