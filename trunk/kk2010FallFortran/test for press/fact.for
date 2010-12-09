      SUBROUTINE FACT(N,A,JPVT)
C
C     FACTORISES A INTO PERMUTED L.U SO THAT PERM*A = L*U
C     JPVT(K) GIVES INDEX OF KTH PIVOT ROW
C     SETS JPVT(N) = -1 IF ZERO PIVOT OCCURS
C
      DIMENSION A(1600,1600),JPVT(1600)
      NM = N - 1
C
C     GAUSS ELIMINATION WITH PARTIAL PIVOTING
C
      DO 5 K = 1,NM
      KP = K + 1
C
C     SELECT PIVOT
C
      L = K
      DO 1 I = KP,N
      IF(ABS(A(I,K)) .GT. ABS(A(L,K)))L = I
    1 CONTINUE
      JPVT(K) = L
      S = A(L,K)
      A(L,K) = A(K,K)
      A(K,K) = S
C
C     CHECK FOR ZERO PIVOT
C
      IF(ABS(S) .LT. 1.0E-15)GOTO 6
C
C     CALCULATE MULTIPLIERS
C
      DO 2 I = KP,N
      A(I,K) = -A(I,K)/S
    2 CONTINUE
C
C     INTERCHANGE AND ELIMINATE BY COLUMNS
C
      DO 4 J = KP,N
      S = A(L,J)
      A(L,J) = A(K,J)
      A(K,J) = S
      IF(ABS(S) .LT. 1.0E-15)GOTO 4
      DO 3 I = KP,N
      A(I,J) = A(I,J) + A(I,K)*S
    3 CONTINUE
    4 CONTINUE
    5 CONTINUE
      RETURN
    6 JPVT(N) = -1
      RETURN
      END

