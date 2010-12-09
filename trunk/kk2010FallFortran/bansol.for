
      SUBROUTINE BANSOL(R,X,B,N,INT)
C
C     USES L.U FACTORISATION TO SOLVE FOR X, GIVEN R
C
      DIMENSION R(65),X(65),B(5,65)
      IF(INT .EQ. 2)GOTO 3
C
C     INT = 1,  TRIDIAGONAL SYSTEM
C
      NP = N - 1
      DO 1 J = 1,NP
      JP = J + 1
    1 R(JP) = R(JP) - B(2,JP)*R(J)
      X(N) = R(N)/B(3,N)
      DO 2 J = 1,NP
      JA = N - J
      X(JA) = (R(JA) - B(4,JA)*X(JA+1))/B(3,JA)
    2 CONTINUE
      RETURN
C
C     INT = 2,  PENTADIAGONAL SYSTEM
C     ASSUMES FIRST EQUATION FORMED AT MIDSIDE NODE
C     SET IBC = 0 IF LAST EQUATION FORMED AT MIDSIDE NODE
C     SET IBC = 1 IF LAST EQUATION FORMED AT CORNER NODE
C
    3 IBC = 1
      NH = N/2
      IF(2*NH .EQ. N)R(N+1) = 0.
      IF(2*NH .EQ. N)B(2,N+1) = 0.
      DO 6 I = 1,2
      DO 5 J = 1,NH
      JA = 2*J
      DO 4 K = 1,I
      JB = JA - 1 + K
    4 R(JB) = R(JB) - B(I,JB)*R(JB-1)
    5 CONTINUE
    6 CONTINUE
      NEN = NH - IBC
      X(N) = R(N)/B(3,N)
      IF(IBC .EQ. 1)X(N-1) = (R(N-1) - B(4,N-1)*X(N))/B(3,N-1)
      DO 7 J = 1,NEN
      JA = N - 2*J + 1 - IBC
      X(JA) = (R(JA) - B(4,JA)*X(JA+1) - B(5,JA)*X(JA+2))/B(3,JA)
      X(JA-1) = (R(JA-1) - B(4,JA-1)*X(JA))/B(3,JA-1)
    7 CONTINUE
      RETURN
      END

