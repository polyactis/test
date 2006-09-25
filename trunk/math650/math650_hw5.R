#2006-09-24 case 2 of chapter 4
data2 = read.csv("/usr/local/doc/statistical_sleuth/ASCII/case0402.csv")
data2_c = data2[data2$TREATMT=="CONVENTIONAL",]$TIME
data2_m = data2[data2$TREATMT=="MODIFIED",]$TIME
wilcox.test(data2_m, data2_c, conf.int=TRUE)


#2006-09-24, chapter 4, question 31
data = read.csv("/usr/local/doc/statistical_sleuth/ASCII/ex0431.csv")
wilcox.test(SURVIVAL~GROUP, data=data, conf.int=TRUE)

control_d = data[data$GROUP=="CONTROL",]$SURVIVAL
therapy_d = data[data$GROUP=="THERAPY",]$SURVIVAL

wilcox.test(control_d, therapy_d, conf.int=TRUE)
w_result = wilcox.test(therapy_d, control_d, conf.int=TRUE)
cat("wilcox test p-value:", w_result$p.value, "\n")
cat("wilcox test confidence interval:", w_result$conf.int, "\n")

#calculate the z_stat
rank_l = rank(c(control_d, therapy_d))
no_of_controls = length(control_d)
no_of_therapies = length(therapy_d)

w = sum(rank_l[(no_of_controls+1):(no_of_controls+no_of_therapies)])
avg_rank = mean(rank_l)
sd_rank = sd(rank_l)
z_stat = (w-avg_rank*no_of_therapies)/(sd_rank*sqrt(no_of_controls*no_of_therapies/(no_of_controls+no_of_therapies)))

#through z_stat's normal approx. to manually calculate wilcoxon test p-value
z_stat_normal_p_value = pnorm(z_stat, lower.tail=FALSE)*2
cat("z_stat_normal_p_value:", z_stat_normal_p_value, "\n")

permutation_test = function(input_data, no_of_controls, no_of_samplings=10000)
{
	stat_list = rep(1, no_of_samplings)
	no_of_data = length(input_data)
	for (i in seq(no_of_samplings))
	{
	sampled_data = sample(input_data)
	rank_l = rank(sampled_data)
	w = sum(rank_l[(no_of_controls+1):no_of_data])
	stat_list[i] = w
	}
	return (stat_list)
}

#get the p-value from permutation
no_of_samplings = 1e4
stat_list = permutation_test(data$SURVIVAL, no_of_controls, no_of_samplings)
perm_p_value= sum(stat_list>=w)/no_of_samplings
cat("permutation p-value:", perm_p_value, "\n")
