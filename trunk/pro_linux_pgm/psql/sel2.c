#include <stdlib.h>
#include <stdio.h>
#include <libpq-fe.h>

PGconn *conn=NULL;
void tidyup_and_exit();
int execute_one_statement(const char* stmt_to_exec,PGresult **result);

//void show_column_info(
int main()
{

  PGresult* result;
  int stmt_ok; 
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
  
  stmt_ok=execute_one_statement("BEGIN WORK",&result);
  if(stmt_ok)
    {
      PQclear(result);
      stmt_ok=execute_one_statement("DECLARE city_cursor CURSOR FOR SELECT city,prcp from weather where prcp>0.25 ",&result);
      if(stmt_ok)
	{
	  PQclear(result);
	  stmt_ok=execute_one_statement("FETCH 1 IN city_cursor ",&result);
	  while(stmt_ok&&PQntuples(result)>0)
	    {
	      PQclear(result);
	      stmt_ok=execute_one_statement("FETCH NExt in city_cursor",&result);
	    } 
	  if(stmt_ok)
	    {
	      PQclear(result);
	      stmt_ok=execute_one_statement("COMMIT WORK",&result);
	    }
	}
    }

  if(stmt_ok)
    PQclear(result);
  PQfinish(conn);
  return EXIT_SUCCESS;
}  
 
int execute_one_statement(const char* stmt_to_exec,PGresult** res_ptr) 
{
  int retcode=1;
 
  PGresult* local_result;
  const char* str_res=NULL;
  printf("about to execute %s\n",stmt_to_exec);
  local_result=PQexec(conn,stmt_to_exec);
  *res_ptr=local_result;

if(!local_result)
    {
      printf("PQexec command failed, no error code.\n");
      retcode=0;
    }
  else
    {
      switch(PQresultStatus(local_result))
	{
	case PGRES_COMMAND_OK:
	  str_res=PQcmdTuples(local_result);
	  printf("Command executed ok,%s rows affected\n",str_res);
	  break;
	case PGRES_TUPLES_OK:
        printf("Query may have returned data,%d rows returned\n",PQntuples(local_result));
	break;
	default:
	  printf("Command failed with code %s,error message %s\n",
		 PQresStatus(PQresultStatus(local_result)),
		 PQresultErrorMessage(local_result));
	  PQclear(local_result);
	  retcode=0;
	  break;
	}
    }  
    
 return retcode;
}

 
void tidyup_and_exit()
{

  if(conn!=NULL)
    PQfinish(conn);
  exit(EXIT_FAILURE);
}
