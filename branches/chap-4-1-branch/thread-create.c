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
  //pthread_attr_t attr;

  //pthread_attr_init(&attr);
  //pthread_attr_setdetachstate(&attr,PTHREAD_CREATE_DETACHED);
  
  pthread_create (&thread_id,NULL,&print_x,NULL);

  //pthread_attr_destroy(&attr);
  pthread_join(thread_id,NULL);
  
  for(i=0;i<100;i++)
    fputc('0',stderr);

  return 0;
}
