#include <stdio.h>
#include <sys/types.h>
#include <sys/time.h>
#include <unistd.h>

int main(void)
{
  fd_set rfds;
  struct timeval tv;
  int retval;
  FD_ZERO(&rfds);
  FD_SET(0,&rfds);
  tv.tv_sec=5;
  tv.tv_usec=1;
  retval=select(1,&rfds,NULL,NULL,&tv);

  if(retval)
    printf("Data is available on the stdin.\n");
  else
    printf("No data within 5 secs.\n");

  exit(0);
} 
