#04-04-05, a good panel function to differentiate the points by color.

panel.special <- function(x,y,subscripts)
{
  one <- da[subscripts,]$y==1
  two <- da[subscripts,]$y==2
  three <- da[subscripts,]$y==3
  lpoints(x[one], y[one], col = 1)
  lpoints(x[two], y[two], col = 2)
  lpoints(x[three],y[three],col=3)
}
