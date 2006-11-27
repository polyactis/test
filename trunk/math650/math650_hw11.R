data1 = read.csv("/usr/local/doc/statistical_sleuth/ASCII/case1402.csv")
data1$LOGWILLIAM = log(data1$WILLIAM)
data1$LOGFORREST = log(data1$FORREST)

#chap14, no9
data1.glm = glm(LOGWILLIAM~STRESS + SO2 + O3 + O3*STRESS, data=data1)
summary(data1.glm)

diff_of_ozone_slope = data1.glm$coefficients[5]
cat("difference between ozone slope parameters for stressed versus well-watered plots is", diff_of_ozone_slope, ".\n")
cat("in the scale of seed yield, well-watered is ", exp(diff_of_ozone_slope), " times better than stressed.\n")

sd_error_of_diff_of_ozone_slope = summary(data1.glm)$coefficients[5,2]	#got it from the output of summary()

upper_95_bound = diff_of_ozone_slope + qt(0.975, 25)*sd_error_of_diff_of_ozone_slope
lower_95_bound = diff_of_ozone_slope - qt(0.975, 25)*sd_error_of_diff_of_ozone_slope

cat("95% confidence interval in the scale of seed yield, from", exp(lower_95_bound), "to", exp(upper_95_bound), "\n")

#chap14, No10, treat SO2 also as categorical
data1$SO2 = factor(data1$SO2)
data1.glm_forrest = glm(LOGFORREST~O3 + SO2 + STRESS + O3*SO2 + 
	O3*STRESS + SO2*STRESS + O3*SO2*STRESS , data=data1)
data1.glm_william = glm(LOGWILLIAM~O3 + SO2 + STRESS + O3*SO2 + 
	O3*STRESS + SO2*STRESS + O3*SO2*STRESS, data=data1)
data1.glm_forrest.anova = anova(data1.glm_forrest)
print(data1.glm_forrest.anova)
data1.glm_william.anova = anova(data1.glm_william)
print(data1.glm_william.anova)

#the output of anova is 4-column. The 3rd and 4th columns are complimentary to
#1st and 2nd column. The 1st row is the null model with only one parameter(mean).
#Starting from the 2nd row, the 3rd and 4th column is the df and residual after
#including the parameters from this row and above.

print_anova_table = function(anova_result)
{
	no_of_rows = dim(anova_result)[1]
	no_of_columns = dim(anova_result)[2]
	rss_full_model = anova_result[no_of_rows, no_of_columns]/anova_result[no_of_rows, no_of_columns-1]
	#the 3rd and 4th column of last row is regarded as the full model
	cat("Source\tDf\tSum of squares\tMean square\tF-stat\tp-value\n")
	for (i in seq(2, no_of_rows))
	{
	mean_sq = anova_result[i, 2]/anova_result[i,1]
	f_stat = mean_sq/rss_full_model
	p_value = pf(f_stat, anova_result[i,1], anova_result[no_of_rows, no_of_columns-1], lower.tail=FALSE)
	source_name = row.names(anova_result)[i]
	cat(source_name, "\t", anova_result[i,1], "\t", anova_result[i, 2], "\t", mean_sq, "\t", f_stat, "\t", p_value, "\n")
	}
}

print_anova_table(data1.glm_forrest.anova)
print_anova_table(data1.glm_william.anova)

#chap14, no13
t.test(data1$WILLIAM, data1$FORREST, paired=TRUE)
wilcox.test(data1$WILLIAM, data1$FORREST, paired=TRUE)

data1$LOGRATIO = log(data1$FORREST/data1$WILLIAM)
data1.glm_logratio = glm(LOGRATIO~O3 + SO2 + STRESS + O3*SO2 + 
	O3*STRESS + SO2*STRESS + O3*SO2*STRESS, data=data1)
data1.glm_logratio.anova = anova(data1.glm_logratio)
print(data1.glm_logratio.anova)
print_anova_table(data1.glm_logratio.anova)
