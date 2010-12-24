#include <stdlib.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

void get_home_page(int socket_fd)
{
  char buffer[10000];
  int char_read;

  sprintf(buffer,"GET /\n");
  write(socket_fd,buffer,strlen(buffer));

  while(1){
    char_read=read(socket_fd,buffer,10000);

    if(char_read==0)
      return ;
    fwrite(buffer,sizeof(char),char_read,stdout);
    
  }
}


int main(int argc,char*  argv[])
{
  int socket_fd;
  struct sockaddr_in name;
  struct hostent* hostinfo;

  socket_fd=socket(PF_INET,SOCK_STREAM,0);

  name.sin_family=AF_INET;

  hostinfo=gethostbyname(argv[1]);

  if(hostinfo==NULL)
    return 1;
  else
    name.sin_addr=*((struct in_addr *) hostinfo->h_addr);

  name.sin_port=htons(80);

  if(connect(socket_fd,&name,sizeof(struct sockaddr_in))==-1)
  {
    perror("connect");
    return 1;
  }
     
     
  get_home_page(socket_fd);
  return 0; 
}

