#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

sig_atomic_t sigusr1_count=0;

void handler(int signal_number)
{
	++sigusr1_count;
}

int main()
{
	struct sigaction sa;
	long i;
	pid_t pid=getpid();
	memset(&sa,0,sizeof(sa));
	sa.sa_handler=&handler;

	
	sigaction(SIGUSR1,&sa,NULL);
	for(i=0; i<4343;i++)
		kill(pid,SIGUSR1);
	printf("SIGUSR1 WAS received %d times.\n",sigusr1_count);
	return 0;

}	
