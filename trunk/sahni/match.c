#define MAXN 100
#define MAXM 30

int simple_match(char t[],char p[],int n,int m)
{
  int i,j,k;
  for(i=0;i<=n-m;i++)
    {
      for(j=0,k=i;j<m&&t[k]==p[j];k++,j++);
      if(j==m)
	return i;
    }
  return -1;
}


void faillink(char p[],int flink[],int m)
{
  int j,k;
  flink[0]=-1;
  j=1;
  while(j<m)
    {
      k=flink[j-1];
      while(k!=-1&&p[k]!=p[j-1])
	k=flink[k];
      flink[j]=k+1;
      j++;
    }
}


int kmp_match(char t[],char p[],int flink[],int n,int m)
{
  int i,j;
  i=0;
  j=0;
  while(j<n)
    {
      while(j!=-1&&p[j]!=t[i])
	j=flink[j];
      if(j==m-1)
	return i-m+1;
      i++;
      j++;
    }
  return -1;
}
