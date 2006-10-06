#2006-10-04

linear_model_func = function(data, output_fname)
{
	result = lm(MORTALITY ~ WINE, data)
	print(summary(result))
	#hist(resid(result))
	#qqnorm(resid(result))
	postscript(output_fname)
	opar <- par(mfrow = c(3,2), oma = c(0, 0, 1.1, 0))
	#'oma' A vector of the form 'c(bottom, left, top, right)' giving the size of the outer margins in lines of text.
	plot(result)
	
	#par(opar)
	#dev.off()
	#postscript(output_fname)
	#opar <- par(mfrow = c(1,2), oma = c(0, 0, 1.1, 0))
	
	#plot(fitted(result), resid(result), main='fitted value vs residual')
	plot(data$WINE, data$MORTALITY, main='MORTALITY vs WINE', xlab='WINE', ylab='MORTALITY')
	abline(result, col=4)
	par(opar)
	dev.off()
}

data = read.csv("/usr/local/doc/statistical_sleuth/ASCII/ex0823.csv")
output_fname = '~/script/test/math650/figures/hw6_fig1.eps'
linear_model_func(data, output_fname)
new_data = data
new_data$WINE = log(new_data$WINE)
output_fname2 = '~/script/test/math650/figures/hw6_fig2.eps'
linear_model_func(new_data, output_fname2)
