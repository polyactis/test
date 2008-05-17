#06-28-05	a file to store handy R functions

#06-28-05	read in the table and do a multiple_panel drawing
draw_multiple_panel <- function(filename)
{
	library(lattice)
	data = read.table(filename,header=TRUE)
	xyplot(acc1~recurrence|p_value,data=data)
	data
}

#06-29-05
trellis_set_background <- function(color)
{
	library(lattice)
	background=trellis.par.get("background")
	background$col=color
	trellis.par.set("background",background)
}

draw_multiple_panel <- function(filename)
{
	library(lattice)
	data = read.table(filename,header=TRUE)
	xyplot(acc1~parameter,data=data, col="black")
}

draw_multiple_panel2 <- function(filename)
{
	library(lattice)
	data = read.table(filename,header=TRUE)
	xyplot(acc1~parameter2|parameter1,data=data, col="black")
}

#11-10-05 rpart
library(rpart)
fit = rpart(is_correct~p_value+recurrence+connectivity+cluster_size+gradient, data=data, method="class",
	control=rpart.control(cp=.00001),parms=list(prior=c(.58,.42))	)

#2008-05-17 string operation
fname = paste('/tmp/other_output/164_mprobe_mean.rda','fda', sep="")
cat(fname, '\n')
#String manipulation with 'as.character', 'substr', 'nchar', 'strsplit'; further, 'cat' which concatenates and writes to a file, and 'sprintf' for C like string construction.