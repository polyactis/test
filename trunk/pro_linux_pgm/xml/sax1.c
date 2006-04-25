#include <stdlib.h>
#include <stdio.h>

#include <parser.h>
#include <parserInternals.h>

int main()
{
  xmlParserCtxtPtr ctxt_ptr;
  
  ctxt_ptr=xmlCreateFileParserCtxt("schools.xml");
  if(!ctxt_ptr){
    fprintf(stderr,"Failed to create file parser\n");
    exit(EXIT_FAILURE);
  }

  xmlParseDocument(ctxt_ptr);

  if(!ctxt_ptr->wellFormed){
    fprintf(stderr,"Document not well formed\n");
  }

  xmlFreeParserCtxt(ctxt_ptr);

  printf("Parsing complete\n");
  exit(EXIT_SUCCESS);
}
