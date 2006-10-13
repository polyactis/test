library(MASS)
hills.lm  = lm(time~dist+climb, data=hills)

#frame(); par(fig=c(0, 0.6, 0, 0.55))
postscript('~/script/test/math650/figures/math650_hw7_fig1.eps')
hills.fitted = fitted(hills.lm)
hills.studres = studres(hills.lm)
plot(hills.fitted, hills.studres, xlim=c(0,200), ylim=c(-2,8))
abline(h=0, lty=2)
#label the influential points
text(hills.fitted[18], hills.studres[18], row.names(hills[18,]), pos=4)
text(hills.fitted[7], hills.studres[7], row.names(hills[7,]), pos=4)
#identify(hills.fitted, hills.studres, row.names(hills))
dev.off()

#par(fig=c(0.6, 1, 0, 0.55), pty='s')
qqnorm(studres(hills.lm))
qqline(studres(hills.lm))
hills.hat = lm.influence(hills.lm)$hat
cbind(hills, lev=hills.hat)[hills.hat>3/35,]
cbind(hills, pred=predict(hills.lm))["Knock Hill",]

hills1.lm = update(hills.lm, subset=-18)

update(hills.lm, subset = -c(7,18))

summary(hills1.lm)

summary(update(hills1.lm, weights=1/dist^2))


#chap_11_no_10
library(lattice)
data1 = read.csv("/usr/local/doc/statistical_sleuth/ASCII/ex0328.csv")
LOGIT = data1$REMOVED/(1-data1$REMOVED)
LOGDURATION = log(data1$DURATION)
data2 = cbind(data1, LOGIT, LOGDURATION)
histogram(~LOGIT|BEE, data=data2)
histogram(~LOGDURATION|BEE, data=data2)

postscript('~/script/test/math650/figures/math650_hw7_fig2.eps')
xyplot(LOGIT~LOGDURATION|BEE, data=data2)
dev.off()

linear_model_interaction = function(data, fig_fname)
{
reg = lm(LOGIT~LOGDURATION+BEE+LOGDURATION*BEE, data=data)
print(summary(reg))
postscript(fig_fname)
opar <- par(mfrow = c(2,2), oma = c(0, 0, 1.1, 0))
plot(reg)
par(opar)
dev.off()
return(reg)
}

draw_data_interaction = function(reg, data)
{
intercept_1 = coef(reg)[1]
slope_1 = coef(reg)[2]
intercept_2 = coef(reg)[1] + coef(reg)[3]
slope_2 = coef(reg)[2]+coef(reg)[4]
xyplot(LOGIT~LOGDURATION, data=data, panel=function(x,y,subscripts){
  one <- data[subscripts,]$BEE=="QUEEN"
  two <- data[subscripts,]$BEE=="WORKER"
  lpoints(x[one], y[one], col = 1)
  lpoints(x[two], y[two], col = 2)
  panel.abline(c(intercept_1, slope_1), col=1)
  panel.abline(c(intercept_2, slope_2), col=2)
  }
)
}

reg = linear_model_interaction(data2, '~/script/test/math650/figures/math650_hw7_fig3.eps')
#2006-10-12, very weird, trellis.device() can't be run within draw_data(). It'll give null graphic output.

trellis.device(postscript, color=T, file='~/script/test/math650/figures/math650_hw7_fig4.eps')
draw_data_interaction(reg, data2)
dev.off()

#remove outlier #41
reg = linear_model_interaction(data2[-41,], '~/script/test/math650/figures/math650_hw7_fig5.eps')
#2006-10-12, very weird, trellis.device() can't be run within draw_data(). It'll give null graphic output.

trellis.device(postscript, color=T, file='~/script/test/math650/figures/math650_hw7_fig6.eps')
draw_data_interaction(reg, data2[-41,])
dev.off()

linear_model_no_intr = function(data, fig_fname)
{
reg = lm(LOGIT~LOGDURATION+BEE, data=data)
print(summary(reg))
postscript(fig_fname)
opar <- par(mfrow = c(2,2), oma = c(0, 0, 1.1, 0))
plot(reg)
par(opar)
dev.off()
return(reg)
}

draw_data_no_intr = function(reg, data)
{
intercept_1 = coef(reg)[1]
slope_1 = coef(reg)[2]
intercept_2 = coef(reg)[1] + coef(reg)[3]
slope_2 = coef(reg)[2]
xyplot(LOGIT~LOGDURATION, data=data, panel=function(x,y,subscripts){
  one <- data[subscripts,]$BEE=="QUEEN"
  two <- data[subscripts,]$BEE=="WORKER"
  lpoints(x[one], y[one], col = 1)
  lpoints(x[two], y[two], col = 2)
  panel.abline(c(intercept_1, slope_1), col=1)
  panel.abline(c(intercept_2, slope_2), col=2)
  }
)
}
#remove outlier #41
reg = linear_model_no_intr(data2[-41,], '~/script/test/math650/figures/math650_hw7_fig7.eps')
#2006-10-12, very weird, trellis.device() can't be run within draw_data(). It'll give null graphic output.

trellis.device(postscript, color=T, file='~/script/test/math650/figures/math650_hw7_fig8.eps')
draw_data_no_intr(reg, data2[-41,])
dev.off()















panel.special <- function(x,y,subscripts)
{
  one <- data2[subscripts,]$BEE=="QUEEN"
  two <- data2[subscripts,]$BEE=="WORKER"
  lpoints(x[one], y[one], col = 1)
  lpoints(x[two], y[two], col = 2)
  panel.abline(c(intercept_1, slope_1), col=1)
  panel.abline(c(intercept_2, slope_2), col=2)
}
xyplot(LOGIT~LOGDURATION, data=data2, panel=panel.special)

reg = lm(LOGIT~LOGDURATION+BEE+LOGDURATION*BEE, data=data2)
summary(reg)
opar <- par(mfrow = c(4,1), oma = c(0, 0, 1.1, 0))
plot(reg)
par(opar)
plot(resid(reg))

xyplot(LOGIT~LOGDURATION, data=data2, panel=function(x,y,subscripts){
  one <- data2[subscripts,]$BEE=="QUEEN"
  two <- data2[subscripts,]$BEE=="WORKER"
  lpoints(x[one], y[one], col = 1)
  lpoints(x[two], y[two], col = 2)
  panel.abline(c(intercept_1, slope_1), col=1)
  panel.abline(c(intercept_2, slope_2), col=2)
  }
)
