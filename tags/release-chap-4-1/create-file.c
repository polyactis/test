#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main (int argc,char* argv[])
{
	char * path=argv[1];
	char * path1=argv[2];
	char  buffer[8];
	size_t written,red;
	mode_t mode =S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH;
	int fd=open(path,O_WRONLY|O_CREAT|O_APPEND,mode);
	int fd1=open(path1,O_RDONLY);
	red=read(fd1,buffer,sizeof(buffer));
	/*if(red=-1)
	  return -1;*/
	if(fd==-1){
	  perror("open");
	  return 1;
         }
        written=write(fd,buffer,8);
        if(written=-1)
          return -1;
return 0;
}
