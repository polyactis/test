#include <pthread.h>
#include <stdio.h>

void* print_x(void* noneed)
{
  int i;
  for (i=0;i<100000;i++)
    fputc('x',stderr);

  return NULL;
}


int main()
{
  int i;
  pthread_t thread_id;

  pthread_create (&thread_id,NULL,&print_x,NULL);

  for(i=0;i<1000000;i++)
    fputc('0',stderr);

  return 0;
}
