#include <stdio.h>
#include <unistd.h>

typedef int temp_file_handle;

temp_file_handle write_temp_file(char* buffer,size_t length)
{
	char temp_filename[]="/tmp/temp_file.XXXXXX";
	int fd=mkstemp(temp_filename);

	unlink(temp_filename);
	write(fd,&length,sizeof(length));
	write(fd,buffer,length);

	return fd;
}

char* read_temp_file(temp_file_handle temp_file,size_t* length)
{
	char* buffer;
	int fd=temp_file;
	lseek(fd,0,SEEK_SET);
	read(fd,length,sizeof(*length));
	buffer=(char*) malloc(*length);
	read(fd,buffer,length);
	close(fd);
	return buffer;

}

int main()
{
	int fd;
	char* buffer_w="where are you";
	char* buffer_r;
	size_t length=13;
	size_t* len;
	fd=write_temp_file(buffer_w,length);	
	buffer_r=read_temp_file(fd,len);
	printf("buffer_w is %s\n",buffer_w);
	printf("buffer_r is %s\n",buffer_r);
}
