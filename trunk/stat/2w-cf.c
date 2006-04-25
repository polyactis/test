
#define VER 5 
#define HOR 4 
#define Z 1 

float aa[VER][HOR][Z]={4.9,3.7,4.1,3.8, 5.8,4.3,4.4,4.6, 6.1,5.0,5.6,5.1, 6.4,5.2,5.7,5.2, 6.9,6.0,6.2,6.4};
/*{8.53,17.53,39.14,32.00, 20.53,21.07,26.20,23.80, 12.53,20.80,31.33,28.87, 14.00,17.33,45.80,25.06, 10.80,20.07,40.20,29.33};
{57,49, 53,56, 65,70, 40,35, 43,48, 61,65, 28,33, 33,37, 53,48};
{8,8, 8,7, 7,8, 37,38, 32,31, 9,9, 44,45, 40,41, 83,82, 65,63, 72,73, 10,8, 55,53, 35,36, 44,45, 39,37, 83,81, 13,11, 43,41, 68,67, 81,82, 90,91, 53,51, 30,29, 5,6, 10,8, 44,45, 20,21, 13,11, 12,9};
{1.375,1.033, 1.407,1.217, 1.068,0.984, 1.752,1.615, 1.773,1.693, 1.201,0.673, 0.779,0.840, 1.042,0.842, 1.223,1.253, 1.633,1.217};
{{6,2,9,3,6,2,9,3},{4,10,4,6,4,10,4,6},{9,12,8,11,9,12,8,11}};
{{55,39,61,35,50},{29,27,20,39,45},{5,25,11,31,33},{8,12,19,24,12}};
{{9,4,12,8,11,10},{3,2,6,4,9,6}};
{{6,2,9,3},{4,10,4,6},{9,12,8,11}};*/

float sum(float *pi,int weight,int num)
{
  int k;
  float total=0;
  for(k=0;k<num;k++)
    total+=pi[k]*pi[k]/weight;

  return total;
}

main()
{

  float A,B,R,K,C;
  float tmp=0;
  int i,j,n,dfr,dfk,dfrk,dfe,dft,dfT;

  float r[VER]={};
  float k[HOR]={};
  float a[VER][HOR]={},c[HOR*VER],*cc=aa;
  float ssqT,ssqt,ssqr,ssqk,ssqrk,ssqe,msqr,msqk,msqrk,msqe,Fre,Fke,Frke;
  
  for(i=0;i<VER;i++)
    for(j=0;j<HOR;j++)
      for(n=0;n<Z;n++)
        a[i][j]+=aa[i][j][n];

  dfr=VER-1;
  dfk=HOR-1;
  dfrk=(VER-1)*(HOR-1);
  dfe=VER*HOR*(Z-1);
  dft=VER*HOR-1;
  dfT=VER*HOR*Z-1;
  
  for(i=0;i<HOR;i++)
    for(j=0;j<VER;j++)
      k[i]+=a[j][i];
  
  for(i=0;i<VER;i++)
    for(j=0;j<HOR;j++)
      c[i*HOR+j]=a[i][j];
      
  for(i=0;i<VER;i++)
    for(j=0;j<HOR;j++)
      r[i]+=a[i][j];
  
  A=sum(cc,1,HOR*VER*Z);
  B=sum(c,Z,HOR*VER);
  R=sum(r,HOR*Z,VER);
  K=sum(k,VER*Z,HOR);
  for(i=0;i<HOR*VER;i++)
    tmp+=c[i];
  C=(tmp*tmp)/(VER*HOR*Z);

  ssqr=R-C;
  ssqk=K-C;
  ssqrk=B-R-K+C;
  ssqt=B-C;
  ssqe=A-B;
  ssqT=A-C;

  msqr=ssqr/dfr;
  msqk=ssqk/dfk;
  msqe=ssqe/dfe;
  msqrk=ssqrk/dfrk;
  
  
  Fre=msqr/msqe;
  Fke=msqk/msqe;
  Frke=msqrk/msqe;
  
  printf("A=%f\n B=%f\n R=%f\n K=%f\n C=%f\n",A,B,R,K,C);
  printf("dfr=%d\n dfk=%d\n dfrk=%d\n dfe=%d\n dft=%d\n dfT=%d\n",dfr,dfk,dfrk,dfe,dft,dfT);
  printf("ssqr=%f\n ssqk=%f\n ssqrk=%f\n ssqe=%f\n ssqt=%f\n ssqT=%f\n",ssqr,ssqk,ssqrk,ssqe,ssqt,ssqT);
  printf("msqr=%f\n msqk=%f\n msqrk=%f\n msqe=%f\n",msqr,msqk,msqrk,msqe);
  printf("Fre=%f\n Fke=%f\n Frke=%f\n",Fre,Fke,Frke);
  
} 
  
