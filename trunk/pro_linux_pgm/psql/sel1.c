#include <stdlib.h>
#include <stdio.h>
#include <libpq-fe.h>

PGconn *conn=NULL;
void tidyup_and_exit();
FILE* output_stream;
PQprintOpt print_options;

int main()
{

  PGresult* result;
  const char* connection_str="host=localhost dbname=mydb";

  conn=PQconnectdb(connection_str);
  if(PQstatus(conn)==CONNECTION_BAD)
    {
      fprintf(stderr,"connection to %s failed, %s",connection_str,PQerrorMessage(conn));
      tidyup_and_exit();
    }
  else
    {
      printf("Connected OK\n");
    }
  
  result=PQexec(conn,"select city,prcp from weather where prcp>0.25 ");
  
  if(!result)
    {
      printf("PQexec command failed, no error code.\n");
      tidyup_and_exit();
    }
  else
    {
      switch(PQresultStatus(result))
	{
	case PGRES_COMMAND_OK:
	  printf("Command executed ok,%s rows affected\n",PQcmdTuples(result));
	  break;
	case PGRES_TUPLES_OK:
        printf("Query may have returned data\n,%d rows returned\n",PQntuples(result));
	break;
	default:
	  printf("Command failed with code %s,error message %s\n",
		 PQresStatus(PQresultStatus(result)),
		 PQresultErrorMessage(result));
	  PQclear(result);
	  tidyup_and_exit();
	  break;
	}
      
    }

  output_stream=fopen("/dev/tty","w");
  if(output_stream==NULL)
    {
      PQclear(result);
      tidyup_and_exit();
    }
  memset(&print_options,'\0',sizeof(print_options));
  print_options.header=1;
  print_options.align=1;
  print_options.html3=1;
  print_options.fieldSep="|";
  print_options.fieldName=NULL;
  PQprint(output_stream,result,&print_options);

  if(result)
    PQclear(result);
  PQfinish(conn);
  return EXIT_SUCCESS;
}    

void tidyup_and_exit()
{

  if(conn!=NULL)
    PQfinish(conn);
  exit(EXIT_FAILURE);
}
