#include "match.h"


int flink[];

int main()
{
  char t[]="chinese medimedicine college";
  char p[]="medimedicine";
  int i;
  faillink(p,flink,strlen(p));
  
  for(i=0;i<strlen(p);i++)
    printf("flink[%d]=%d\n",i,flink[i]);

  printf("%d\n",kmp_match(t,p,flink,strlen(t),strlen(p)));
  
  return 0;
}
