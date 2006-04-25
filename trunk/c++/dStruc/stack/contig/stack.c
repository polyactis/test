#include "common.h"
#include "stack.h"


void Error(char* s)
{
	fprintf(stderr,"%s\n",s);
	exit(1);
}


void CreateStack(Stack* s)
{
	s->top=0;
}

Boolean StackEmpty(Stack* s)
{
	if(s->top==0)
		return TRUE;
	return FALSE;
}

Boolean StackFull(Stack* s)
{
	if(s->top==MAXSTACK)
		return TRUE;
	return FALSE;
}

void Push(StackEntry item,Stack* s)
{
	if(StackFull(s))
		Error("Stack is full.");
	else
		s->entry[s->top++]=item;
}

void Pop(StackEntry* item, Stack* s)
{
	if(StackEmpty(s))
		Error("Stack is Empty.");
	else 
		*item=s->entry[--s->top];
	
}


void ClearStack(Stack* s)
{
	s->top=0;
}


int StackSize(Stack* s)
{
	return s->top;
}

void StackTop(StackEntry* item, Stack* s)
{
	if(StackEmpty(s))
		Error("Stack is empty.");
	else
		*item=s->entry[s->top];
}



void TraverseStack(Stack* s, void (*Visit)())
{
	int i;
	for(i=0;i<s->top;i++)
		(*Visit)(s->entry[i]);
	
}

