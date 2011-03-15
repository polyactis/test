/* Jacek Radajewski jacek@usq.edu.au */
/* 21/08/1998 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main (void) {

  double result = 0.0;
  double number = 0.0;
  char string[80];
  

  while (scanf("%s", string) != EOF) {

    number = atof(string);
    result = result + number;
  }
    
  printf("%lf\n", result);
  
  return 0;
  
}
