#include <stdio.h>

int main(int argc,char* argv[])
{
	printf("the name of the program is '%s' \n",argv[0]);
	printf("the program has invoked %d arguments.\n",argc-1);
	
	if(argc>1){
		int i;
		printf("the arguments are : \n");
		for(i=1;i<argc;i++)
			printf(" %s\n",argv[i]);
	}
	
	return 0;
}
