#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
	int status;
	pid_t child_pid;
	child_pid=fork();
	
	wait(&status);
	if(child_pid>0)
	{
		printf("Father id %d.\n",(int) getpid());
		sleep(60);
	}	
	
	else
	{
	        printf("This is the child process, with id %d.\n",(int) getpid());
		exit(0);
	}	
	
return 0;		
}
