data1 = read.csv("/usr/local/doc/statistical_sleuth/ASCII/case1301.csv")
cover_perc = 0.01*data1$COVER
LOGIT_COVER = log(cover_perc/(1- cover_perc))
data1$LOGIT_COVER = LOGIT_COVER

#13.12 (a)
rss_treatment = 0
mean_ls = c()
for (i in levels(data1$TREAT))
	mean_ls = c(mean_ls, mean(data1[data1$TREAT==i,]$LOGIT_COVER))
	rss_treatment = rss_treatment + var(data1[data1$TREAT==i,]$LOGIT_COVER)
msq_treatment = var(mean_ls)*16	#16 is dim(data1[data1$TREAT==i,])[1]
cat("mean square of treatment is ", msq_treatment, "\n")

#13.12(b)
block_mean_ls = c()
for (i in levels(data1$BLOCK))
	block_mean_ls = c(block_mean_ls, mean(data1[data1$BLOCK==i,]$LOGIT_COVER))
msq_block = var(block_mean_ls)*12	#12 is dim(data1[data1$BLOCK==i,])[1]
cat("mean square of block is ", msq_block, "\n")

#13.12(c)
group_mean_ls = c()
for (i in levels(data1$BLOCK))
{
	for (j in levels(data1$TREAT))
	{
	group_mean_ls = c(group_mean_ls, mean(data1[data1$BLOCK==i & data1$TREAT==j,]$LOGIT_COVER))
	}
	}
msq_between_groups = var(group_mean_ls)*2	#2 is number of replicates in each plot
cat("mean square between groups is ", msq_between_groups, "\n")

#13.12(d)
rss_interaction = msq_between_groups*47 - msq_treatment*5 - msq_block*7
cat("Interactions Sum of Squares is ", rss_interaction, "\n")
