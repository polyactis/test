      SUBROUTINE SOLVE(N,A,JPVT,BB)
C
C     SOLVES LINEAR SYSTEM, A*X = B
C     ASSUMES A IS FACTORISED INTO L.U FORM (BY FACT)
C     RETURNS SOLUTION, X, IN B
C
      DIMENSION A(1600,1600),JPVT(1600),BB(1600)
C
C     FORWARD ELIMINATION
C
      NM = N - 1
      DO 2 K = 1,NM
      KP = K + 1
      L = JPVT(K)
      S = BB(L)
      BB(L) = BB(K)
      BB(K) = S
      DO 1 I = KP,N
      BB(I) = BB(I) + A(I,K)*S
    1 CONTINUE
    2 CONTINUE
C
C     BACK SUBSTITUTION
C
      DO 4 KA = 1,NM
      KM = N - KA
      K = KM + 1
      BB(K) = BB(K)/A(K,K)
      S = - BB(K)
      DO 3 I = 1,KM
      BB(I) = BB(I) + A(I,K)*S
    3 CONTINUE
    4 CONTINUE
      BB(1) = BB(1)/A(1,1)
      RETURN
      END

