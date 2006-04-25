#include "server.h"


int server_read (int client_socket)
{
  while (1) {
    int length;
    char* text;
    
    /* First, read the length of the text message from the socket.  If
       read returns zero, the client closed the connection.  */
    if (read (client_socket, &length, sizeof (length)) == 0)
      return 0;
    /* Allocate a buffer to hold the text.  */
    text = (char*) malloc (length);
    /* Read the text itself, and print it.  */
    
    read (client_socket, text, length);
    //printf("%s\n",text);
    /* Free the buffer.  */
    free (text);
    if(!strcmp(text,"quit"))
      return 1;
  }
 
}



void* server()
{
 
  struct sockaddr_in name;
  struct hostent* hostinfo;
  int client_sent_quit_message;

  socket_fd=socket(PF_INET,SOCK_STREAM,0);
  name.sin_family=AF_INET;
  hostinfo=gethostbyname("192.168.0.1");

  if(hostinfo==NULL)
    return NULL;
  else
    name.sin_addr=*((struct in_addr*)hostinfo->h_addr);

  name.sin_port=htons(2002);

  bind(socket_fd,&name,sizeof(struct sockaddr_in));
  listen(socket_fd,5);

  //close(socket_fd);
  return NULL;
}
