#include <pthread.h>
#include <stdio.h>

void* compute_primes(void* arg)
{
  int CANDIDATE=2;
  int n=*((int*) arg);

  while(1){
    int factor;
    int is_prime=1;

    for(factor=2;factor<CANDIDATE;factor++)
      if(CANDIDATE%factor ==0){
	is_prime=0;
	break;
      }

    if(is_prime){
      if(--n==0)
	return (void*) CANDIDATE;
    }
    ++CANDIDATE;
  }

  return NULL;
}

int main()
{
  pthread_t thread;
  int which_prime;
  int prime;

  printf("Tell me which prime you want:");
  scanf("%d",&which_prime);
  pthread_create(&thread,NULL,&compute_primes,&which_prime);
  pthread_join(thread,(void*) &prime);

  printf("The %dth prime is %d.\n",which_prime,prime);

  return 0;
}
