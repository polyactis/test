#include <pthread.h>
#include <stdlib.h>


void *thread_function(void *arg)
{
	int i;
	for (i=0; i<20; i++)
	{

		printf("Thread says hi!,%d\n",i);
		sleep(1);
	}
	return NULL;
}


int main(void)
{

  pthread_t mythread;
  if(pthread_create(&mythread, NULL,thread_function,NULL))
    {
      printf("error creating thread.\n");
      abort();
    }
  
  if (pthread_join(mythread,NULL))
    {
      printf("error joining thread.\n");
      abort();
    }
  exit(0);
}
