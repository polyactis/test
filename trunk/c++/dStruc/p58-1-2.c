#include <stdio.h>

#define MAXSIZE 100

int list[MAXSIZE];
int n=0;

int sq_fill(int sq_list[], int sq_n);
int sq_invert( int sq_list[]);
int sq_print( int sq_list[]);

int main()
{
	sq_fill(list,70);
	sq_print(list);
	sq_invert(list);
	sq_print(list);
	return 0;
}

int sq_fill(int sq_list[], int sq_n)
{
	int i;
	for(i=0;i<sq_n;i++)
	{
		sq_list[i]=i;
		n++;
	}
	return 0;
}

int sq_invert(int sq_list[])
{
	int i,tmp;
	for(i=0;i<(n/2-1);i++)
	{
		tmp=sq_list[i];
		sq_list[i]=sq_list[n-i-1];
		sq_list[n-i-1]=tmp;
	}
	return 0;
}


int sq_print(int sq_list[])
{
	int i;
	printf("\nContents of the list:\n");
	for(i=0;i<n;i++)
		printf("%d\t",sq_list[i]);
	return 0;
}
