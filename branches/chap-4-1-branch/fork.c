#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main ()
{
	pid_t child_pid;

	printf("the main process id is %d\n",(int) getpid());

	child_pid=fork();

	if(child_pid!=0)
	{
		printf("This is the parent process, with id %d\n",(int) getpid());
		printf("The child id is %d\n",child_pid);
	}
	else
	{
		printf("This is the child process,with id %d\n",(int) getpid());
		printf("Child's father is %d \n",(int) getppid());
	}
	
return 0;

}
