
      SUBROUTINE BANFAC(B,N,INT)
C
C     FACTORISES BAND MATRIX ARISING FROM LINEAR OR QUADRATIC ELEMENTS
C     INTO L.U
C
      DIMENSION B(5,65)
      IF(INT .EQ. 2)GOTO 2
C
C     INT = 1,	LINEAR ELEMENTS = TRIDIAGONAL SYSTEM
C
      NP = N - 1
      DO 1 J = 1,NP
      JP = J + 1
      B(2,JP) = B(2,JP)/B(3,J)
      B(3,JP) = B(3,JP) - B(2,JP)*B(4,J)
    1 CONTINUE
      RETURN
C
C     INT = 2,	QUADRATIC ELEMENTS = PENTADIAGONAL SYSTEM
C     ASSUMES FIRST EQUATION FORMED AT MIDSIDE NODE
C
    2 NH = N/2
      DO 5 I = 1,2
      JS = 3 - I
      DO 4 J = JS,NH
      JA = 2*(J-1)
      IF(I .EQ. 2)GOTO 3
C
C     I = 1,  FIRST PASS, REDUCE TO TRIDIAGONAL
C
      JB = JA + 2
      B(1,JB) = B(1,JB)/B(2,JB-1)
      B(2,JB) = B(2,JB) - B(1,JB)*B(3,JB-1)
      B(3,JB) = B(3,JB) - B(1,JB)*B(4,JB-1)
      GOTO 4
C
C     I = 2,  SECOND PASS, REDUCE TO UPPER TRIANGULAR
C
    3 JB = JA + 3
      B(2,JB-1) = B(2,JB-1)/B(3,JB-2)
      B(3,JB-1) = B(3,JB-1) - B(2,JB-1)*B(4,JB-2)
      IF(JB .GT. N)GOTO 4
      B(2,JB) = B(2,JB)/B(3,JB-1)
      B(3,JB) = B(3,JB) - B(2,JB)*B(4,JB-1)
      B(4,JB) = B(4,JB) - B(2,JB)*B(5,JB-1)
    4 CONTINUE
    5 CONTINUE
      RETURN
      END

