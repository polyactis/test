#06-28-05	a file to store handy R functions

#06-28-05	read in the table and do a multiple_panel drawing
draw_multiple_panel <- function(filename)
{
	library(lattice)
	data = read.table(filename,header=TRUE)
	xyplot(acc1~recurrence|p_value,data=data)
	data
}
