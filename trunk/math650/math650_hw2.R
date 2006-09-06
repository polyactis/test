norm_randm_list = rnorm(24, 2, 4)
X = matrix(norm_random_list, 4,6)
apply(X, 2, mean)
sd(apply(X, 2, mean))
