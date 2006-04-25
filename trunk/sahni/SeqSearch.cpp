#include <iostream.h>

template <class T>

int SeqSearch(T a[],const T& x,int n)
{
  if(n<1)
    return -1;
  if(a[n-1]==x)
    return n-1;
  return SeqSearch(a,x,n-1);
}

int main(int argc,char** argv)
{
  int a[10000];
  int x;
  int i;

  cout<<"Please input the number to be searched:";
  cout<<endl;
  cin>>x;
  
  for(i=0;i<10000;i++)
    a[i]=i;

  SeqSearch(a,x,10000);

  return 0;
  
}
