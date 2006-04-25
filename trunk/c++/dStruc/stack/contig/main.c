#include "common.h"
#include "stack.h"


void Visit(StackEntry entry)
{
	if(entry)
		printf("entry:%c\n",entry);
}


void main()
{
	Stack s;
	StackEntry item;
	CreateStack(&s);
	if(StackEmpty(&s))
		printf("Stack empty\n");
	Push('c',&s);
	if(StackEmpty(&s))
		printf("Stack empty\n");
	Push('h',&s);
	TraverseStack(&s,Visit);
	Pop(&item,&s);
	printf("%c\n",item);
	TraverseStack(&s,Visit);
	Pop(&item,&s);
	printf("%c\n",item);
	if(StackEmpty(&s))
		printf("Stack empty\n");

}

