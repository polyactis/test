#include <pthread.h>
#include <stdio.h>

struct char_print_parameters
{
  char character;
  int count;
};

void* char_print(void* parameter)
{
  struct char_print_parameters* p=(struct char_print_parameters*) parameter;
  int i;
  for(i=0;i<p->count;i++)
    {
      fputc(p->character,stderr);
    }
  return NULL;
}

int main()
{
  pthread_t thread1_id;
  pthread_t thread2_id;

  pthread_attr_t attr1;
  pthread_attr_t attr2;

  struct char_print_parameters thread1_param;
  struct char_print_parameters thread2_param;

  thread1_param.character='x';
  thread1_param.count=10000;

  thread2_param.character='o';
  thread2_param.count=10000;

  pthread_attr_init(&attr1);
  pthread_attr_setdetachstate(&attr1,PTHREAD_CREATE_DETACHED);

  pthread_create(&thread1_id,&attr1,&char_print,&thread1_param);
  pthread_create(&thread2_id,NULL,&char_print,&thread2_param);

  pthread_join(thread2_id,NULL);
  pthread_attr_destroy(&attr1);

  return 0;
}
