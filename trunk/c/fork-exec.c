#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int spawn ( char* program,char** arglist)
{
	pid_t child_pid;

	child_pid=fork();
	if(child_pid!=0)
	{
		printf("The parent id is %d.\n",(int) getpid());
		return child_pid;
	}
	else
	{
		execvp(program,arglist);
		fprintf(stderr,"There is an error in execvp.\n");
		abort();
	}
}

int main ()
{
	int child_status;
	
	char* arglist[]={
		"ls",
		"-l",
		"/",
		NULL
		};

	spawn("ls",arglist);

	wait(&child_status);
	if(WIFEXITED(child_status))
		printf("The child process exits with exit code:%d.\n",WEXITSTATUS(child_status));
	else
		printf("Child process exits abnormally.\n");

	printf("Done with the main program.\n");

	return 0;
}	
	
