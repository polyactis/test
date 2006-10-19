#test from Venables2002 page 145
test_contr = function()
{
	dat = data.frame(a=factor(rep(1:3,3)), y=rnorm(9, rep(2:4, 3), 0.1))
	obj = lm(y~a, dat)
	alf.star = coef(obj)
	print(alf.star)
	ca = contrasts(dat$a)
	cat("contrast matrix:\n")
	print(ca)
	drop(ca %*% alf.star[-1])
	dummy.coef(obj)
}
options(contrasts = c("contr.treatment", "contr.poly"))
test_contr()
options(contrasts = c("contr.sum", "contr.poly"))
test_contr()
options(contrasts = c("contr.helmert", "contr.poly"))
test_contr()
options(contrasts = c("contr.poly", "contr.poly"))
test_contr()

#question 1
test_contr2 = function()
{
	NN=factor(levels=c(0,1,2));
	contrasts(NN)
}
options(contrasts=c("contr.sum", "contr.sum"))
test_contr2()
options(contrasts = c("contr.treatment", "contr.poly"))
test_contr2()
options(contrasts = c("contr.helmert", "contr.poly"))
test_contr2()
options(contrasts = c("contr.poly", "contr.poly"))
test_contr2()

#question 2, just try the options above and run code from hw7

#question 3
library(rrcov)
#?lstReg
library(lattice)
data1 = read.csv("/usr/local/doc/statistical_sleuth/ASCII/ex0328.csv")
LOGIT = log(data1$REMOVED/(1-data1$REMOVED))
LOGDURATION = log(data1$DURATION)
data2 = cbind(data1, LOGIT, LOGDURATION)
histogram(~LOGIT|BEE, data=data2)
histogram(~LOGDURATION|BEE, data=data2)

postscript('~/script/test/math650/figures/math650_hw8_fig1.eps')
xyplot(LOGIT~LOGDURATION|BEE, data=data2)
dev.off()

linear_model_no_intr = function(data, fig_fname, alpha_value=0.8)
{
data_queen = data[data$BEE=="QUEEN",]
data_worker = data[data$BEE=="WORKER",]
reg_queen = ltsReg(data_queen$LOGDURATION, data_queen$LOGIT, alpha=alpha_value)
reg_worker = ltsReg(data_worker$LOGDURATION, data_worker$LOGIT, alpha=alpha_value)
print(reg_queen)
print(reg_worker)
postscript(fig_fname)
opar <- par(mfrow = c(2,2), oma = c(0, 0, 1.1, 0))
#plot(reg_queen)
qqnorm(resid(reg_queen), main='Normal Q-Q plot, queen')
qqline(resid(reg_queen))
plot(fitted(reg_queen), resid(reg_queen), main='Residuals vs Fitted, queen')
#plot(reg_worker)
qqnorm(resid(reg_worker), main='Normal Q-Q plot, worker')
qqline(resid(reg_worker))
plot(fitted(reg_worker), resid(reg_worker), main='Residuals vs Fitted, worker')
par(opar)
dev.off()
reg = list(reg_queen=reg_queen, reg_worker=reg_worker)
return(reg)
}

draw_data_no_intr = function(reg, data)
{
intercept_1 = coef(reg$reg_queen)[1]
slope_1 = coef(reg$reg_queen)[2]
intercept_2 = coef(reg$reg_worker)[1]
slope_2 = coef(reg$reg_worker)[2]
xyplot(LOGIT~LOGDURATION, data=data, main='Regression line, black=QUEEN, red=WORKER', auto.key = TRUE,
  panel=function(x,y,subscripts){
  one <- data[subscripts,]$BEE=="QUEEN"
  two <- data[subscripts,]$BEE=="WORKER"
  lpoints(x[one], y[one], col = 1)
  lpoints(x[two], y[two], col = 2)
  panel.abline(c(intercept_1, slope_1), col=1)
  panel.abline(c(intercept_2, slope_2), col=2)
  }
)
}
reg = linear_model_no_intr(data2, '~/script/test/math650/figures/math650_hw8_fig2_alpha0_9.eps', 0.9)
trellis.device(postscript, color=T, file='~/script/test/math650/figures/math650_hw8_fig3_alpha0_9.eps')
draw_data_no_intr(reg, data2)
dev.off()

reg = linear_model_no_intr(data2, '~/script/test/math650/figures/math650_hw8_fig2_alpha0_8.eps', 0.8)
trellis.device(postscript, color=T, file='~/script/test/math650/figures/math650_hw8_fig3_alpha0_8.eps')
draw_data_no_intr(reg, data2)
dev.off()

reg = linear_model_no_intr(data2, '~/script/test/math650/figures/math650_hw8_fig2_alpha0_6.eps', 0.6)
trellis.device(postscript, color=T, file='~/script/test/math650/figures/math650_hw8_fig3_alpha0_6.eps')
draw_data_no_intr(reg, data2)
dev.off()
