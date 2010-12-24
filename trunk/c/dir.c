#include <fcntl.h>
#include <stdio.h>

int main()
{
  char buffer[29];
  getwd(buffer,29);
  printf("The current working directory is %s.\n",buffer);
  unlink("/usr/local/code/test/dir.c~");
}
