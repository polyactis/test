#include <fcntl.h>
#include <sys/types.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>

const char* get_file_type(const char* path)
{
  struct stat st;
  lstat(path,&st);
  if(S_ISLNK(st.st_mode))
    return "symbolic file";
  else if(S_ISDIR(st.st_mode))
    return "directory";
  else if(S_ISCHR(st.st_mode))
    return "character device"; 
  else if (S_ISBLK (st.st_mode))
    return "block device";
  else if (S_ISFIFO (st.st_mode))
    return "fifo";
  else if (S_ISSOCK (st.st_mode))
    return "socket";
  else if (S_ISREG (st.st_mode))
    return "regular file";
  else
    /* Unexpected.  Each entry should be one of the types above.  */
    assert (0);
}

int main(int argc,char* argv[])
{
  char* dir_path;
  DIR* dir;
  struct dirent* entry;
  char entry_path[PATH_MAX+1];
  size_t path_len;

  if(argc>=2)
    dir_path=argv[1];
  else
    dir_path=".";
  strncpy(entry_path,dir_path,sizeof(entry_path));

  path_len=strlen(dir_path);

  if(entry_path[path_len-1]!='/'){
    entry_path[path_len]='/';
    entry_path[path_len+1]='\0';
    ++path_len;
  }

  dir=opendir(dir_path);
  while((entry=readdir(dir))!=NULL){
    const char* type;
    strncpy (entry_path+path_len,entry->d_name,sizeof(entry_path)-path_len);
    type=get_file_type(entry_path);
    printf("%-18s:%s\n",type,entry_path);
  }
  closedir(dir);
  return 0;
}


