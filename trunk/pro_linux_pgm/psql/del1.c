#include <stdlib.h>
#include <stdio.h>
#include <libpq-fe.h>

int main()
{
  PGconn* conn;
  PGresult* result;
  const char* connection_str="host=localhost dbname=mydb";

  conn=PQconnectdb(connection_str);
  if(PQstatus(conn)==CONNECTION_BAD)
    {
      fprintf(stderr,"connection to %s failed, %s",connection_str,PQerrorMessage(conn));
    }
  else
    {
      printf("Connected OK\n");
    }
  
  result=PQexec(conn,"insert into weather (city,temp_lo,temp_hi,prcp,date) values ('New York',30,35,0.27,'18/12/1994')");
  
  if(!result)
    {
      printf("PQexec command failed, no error code.\n");
    }
  else
    {
      switch(PQresultStatus(result))
	{
	case PGRES_COMMAND_OK:
	  printf("Command executed ok,%s rows affected\n",PQcmdTuples(result));
	  break;
	case PGRES_TUPLES_OK:
        printf("Query may have returned data\n");
	break;
	default:
	  printf("Command failed with code %s,error message %s\n",
		 PQresStatus(PQresultStatus(result)),PQresultErrorMessage(result));
	  break;
	}
      PQclear(result);
    }
  PQfinish(conn);
  return EXIT_SUCCESS;
}    
