# include <fcntl.h>
# include <errno.h>
# include <stdio.h>
# include <string.h>


int main (int argc, char * argv[])
{
	/*char* filename=argv[1];*/
	size_t red;
	char buffer[50];
	int fd=open(argv[1],O_RDONLY);
	if (fd==-1){
		fprintf(stderr,"erro opening file :%s\n",strerror(errno));
		exit(1);
	}
	
	do{
		red=read(fd,buffer,sizeof(buffer));
		write(1,buffer,red);
	}while(red>0);
	/*system ("ps -ef");*/
	return 0;
}
