#include <pthread.h>

typdedef struct data_control
{
	pthread_mutex_t mutex;
	pthread_cond_t cond;
	int percent;
} data_control;


int run(data_control *dc)
{
	if(pthread_mutex_lock(&(dc->mutex)))
		return 0;
	dc->percent=0;
	for (i=0;i<20;i++)
	{
		if((i%2)==0)
		{
			dc->percent=i*5;	
			pthread_mutex_unlock(&(dc->mutex));
			pthread_cond_broadcast(&(dc->cond));
			pthread_mutex_lock(&(dc->mutex));
		}
	}
	pthread_mutex_unlock(&(dc->mutex));
	return 1;
}



