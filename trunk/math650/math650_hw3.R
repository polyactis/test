#2006-09-11

t_test_func = function(sample_data1, sample_data2)
{
	len_f = length(sample_data1)
	len_r = length(sample_data2)
	
	mean_f = mean(sample_data1)
	cat("mean_f:", mean_f, "\n")
	mean_r = mean(sample_data2)
	cat("mean_r:", mean_r, "\n")
	cat("mean difference:", mean_f-mean_r, "\n")
	
	sd_f = sd(sample_data1)
	cat("sd_f:", sd_f, "\n")
	sd_r = sd(sample_data2)
	cat("sd_r:", sd_r, "\n")
	
	degrees_of_freedom_of_pooled_sd = len_f + len_r -2
	cat("degrees_of_freedom_of_pooled_sd:", degrees_of_freedom_of_pooled_sd, "\n")
	
	pooled_sd = sqrt( ( (len_f-1)*sd_f^2 + (len_r-1)*sd_r^2  )/degrees_of_freedom_of_pooled_sd )
	cat("pooled_sd:", pooled_sd, "\n")
	
	standard_error_for_the_difference = pooled_sd * sqrt(1/len_f + 1/len_r)
	cat("standard_error_for_the_difference:", standard_error_for_the_difference, "\n")
	
	#by looking up a table with 12=degrees_of_freedom_of_pooled_sd (only for 1st part of hw3)
	percentile_97_5th = 2.179
	cat("percentile_97_5th, df=12:", percentile_97_5th, "\n")
	conf_interv_of_difference_of_mu_lower = mean_f-mean_r- percentile_97_5th*standard_error_for_the_difference
	conf_interv_of_difference_of_mu_upper = mean_f-mean_r + percentile_97_5th*standard_error_for_the_difference
	cat("conf_interv_of_difference_of_mu_lower, df=12:", conf_interv_of_difference_of_mu_lower, "\n")
	cat("conf_interv_of_difference_of_mu_upper, df=12:", conf_interv_of_difference_of_mu_upper, "\n")
	
	t_stat = (mean_f - mean_r - 0)/standard_error_for_the_difference
	cat("t_stat:", t_stat, "\n")
	
	#by looking up a table with degrees_of_freedom_of_pooled_sd=12
	#p_value = 1-0.995 = 0.005 corresponding to t_stat=3.055, actual p_value should be less than this value
	
	
	#below is getting confidence interval and p_value through R
	
	percentile_97_5th = qt(0.025, degrees_of_freedom_of_pooled_sd, lower.tail=FALSE)
	cat("percentile_97_5th:", percentile_97_5th, "\n")
	
	conf_interv_of_difference_of_mu_lower = mean_f-mean_r- percentile_97_5th*standard_error_for_the_difference
	conf_interv_of_difference_of_mu_upper = mean_f-mean_r + percentile_97_5th*standard_error_for_the_difference
	cat("conf_interv_of_difference_of_mu_lower:", conf_interv_of_difference_of_mu_lower, "\n")
	cat("conf_interv_of_difference_of_mu_upper:", conf_interv_of_difference_of_mu_upper, "\n")
	p_value = pt(t_stat, degrees_of_freedom_of_pooled_sd, lower.tail=FALSE)
	cat("p-value of t_stat", p_value, "\n")

}

#chap2 No13, No14

data = read.csv("/usr/local/doc/statistical_sleuth/ASCII/ex0112.csv")
sample_data1 = data[data$DIET=="fishoil",]$BP
sample_data2 = data[data$DIET=="regularoil",]$BP
t_test_func(sample_data1, sample_data2)

#chap 2, No23
data = read.csv("/usr/local/doc/statistical_sleuth/ASCII/ex0223.csv")
sample_data1 = data[data$INCREASe=="Yes",]$FATALITIESCHANGE
sample_data2 = data[data$INCREASe=="No",]$FATALITIESCHANGE
t_test_func(sample_data1, sample_data2)
