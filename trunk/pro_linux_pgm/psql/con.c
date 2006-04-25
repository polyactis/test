#include <libpq-fe.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
  PGconn* conn;
  const char* connection_str="host=localhost dbname=mydb user=hy password=br53xui";
  conn=PQconnectdb(connection_str);
  if(PQstatus(conn)==CONNECTION_BAD){
    fprintf(stderr,"Connection to %s failed:%s\n",connection_str,PQerrorMessage(conn));
  }
  else
    printf("Connection OK\n");

  PQfinish(conn);
  return EXIT_SUCCESS;
}
