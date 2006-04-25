
#define MAXSTACK 10


typedef char StackEntry;
typedef struct stack{
	int top;
	StackEntry entry[MAXSTACK];
}Stack;

void CreateStack(Stack *s);
Boolean StackEmpty(Stack *s);
Boolean StackFull(Stack *s);
void Push(StackEntry item,Stack* s);
void Pop(StackEntry *item, Stack* s);
void ClearStack(Stack *s);
int StackSize(Stack* s);
void StackTop(StackEntry* item, Stack* s);
void TraverseStack(Stack* s,void (*Visit)());
