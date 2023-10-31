data1 = read.csv("/usr/local/doc/statistical_sleuth/ASCII/case1102.csv")
data1$SEX = as.factor(data1$SEX)
LOG_AB_RATIO = log(data1$BRAIN/data1$LIVER)
data = cbind(data1, LOG_AB_RATIO)


lm_full = lm(LOG_AB_RATIO~DAYS+TUMOR+LOSS+WEIGHT+SEX, data=data)
lm_reduced =  lm(LOG_AB_RATIO~DAYS+TUMOR+LOSS+SEX, data=data)
rss_full = sum(lm_full$residuals^2)
rss_reduced = sum(lm_reduced$residuals^2)
F_stat = (rss_reduced-rss_full)/(rss_full/lm_full$df.residual)
cat("F_stat=", F_stat, "\n")

design_matrix = cbind(data1$DAYS, data1$TUMOR, data1$LOSS, data1$WEIGHT, data1$SEX)
design_matrix = as.matrix(design_matrix)
coeff_weight = lm_full$coefficients[5]	#5 because 1 is Intercept
S = sqrt(rss_full/lm_full$df.residual)
t_stat = coeff_weight/(S*(ginv(t(design_matrix) %*% design_matrix)[4,4])^(1/2))
cat("t_stat^2 = ", t_stat^2, "\n")

#
backward_regression_step = function(reduced_formula, data, lm_full)
{
	lm_reduced =  lm(reduced_formula, data=data)
	rss_full = sum(lm_full$residuals^2)
	rss_reduced = sum(lm_reduced$residuals^2)
	rss_delta = rss_reduced-rss_full
	F_stat = rss_delta/(rss_full/lm_full$df.residual)
	result = data.frame(rss_reduced=rss_reduced, rss_delta=rss_delta, F_stat=F_stat)
	return(result)
}

full_formula = LOG_AB_RATIO~DAYS+TUMOR+LOSS+WEIGHT+SEX
#
#variable_factor_list = factor(c("DAYS", "TUMOR", "LOSS", "WEIGHT", "SEX"))
#for (i in seq(5:9))
#{
#	reduced_formula = update.formula(full_formula, ~.-names(data)[i])
#	print(reduced_formula)
#	backward_regression_step(reduced_formula, data, lm_full)
#}
#

reduced_formula1 = update.formula(full_formula, ~.-DAYS)
reduced_formula2 = update.formula(full_formula, ~.-TUMOR)
reduced_formula3 = update.formula(full_formula, ~.-LOSS)
reduced_formula4 = update.formula(full_formula, ~.-WEIGHT)
reduced_formula5 = update.formula(full_formula, ~.-SEX)

for (i in c(reduced_formula1, reduced_formula2, reduced_formula3, reduced_formula4, reduced_formula5))
{
	print(i)
	print(backward_regression_step(i, data, lm_full))
}

step(lm_full, steps=1)
library(MASS)
stepAIC(lm_full, steps=1)

back_result = stepAIC(lm_full)
lm_mean = lm(LOG_AB_RATIO~1, data=data)
#forward and both seem not to work.
forward_result = stepAIC(lm_mean, direction="forward")
both_result = stepAIC(lm_mean, direction="both")


#ssh almaak.usc.edu, Splus version 6.1.2.  7.0 doesn't work due to license problem.
#splus, no "_" in variable name in splus for '='.
#If '_', use '<-', i.e. LOG_AB_RATIO <- log(data1$BRAIN/data1$LIVER); print(LOG_AB_RATIO)
#directly typing 'LOG_AB_RATIO' outputs nothing
data1 = importData("./MySwork/case1102.csv", type="ASCII")
data1$SEX = as.factor(data1$SEX)
LOGABRATIO = log(data1$BRAIN/data1$LIVER)
data = cbind(data1, LOG_AB_RATIO)
dtrix = cbind(data1$DAYS, data1$TUMOR, data1$LOSS, data1$WEIGHT, data1$SEX)
stepwise(dtrix, LOGABRATIO, method="forward", f.crit=4.0)
stepwise(dtrix, LOGABRATIO, method="backward", f.crit=c(4.0,4.0))
stepwise(dtrix, LOGABRATIO, method="efroymson")
stepwise(dtrix, LOGABRATIO, method="exhaustive")
