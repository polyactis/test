#define VER 3 
#define HOR 2 
#define Z 3 


float a[VER][HOR][Z]={2,1,1, 3,3,4, 4,5,4, 5,6,5, 7,7,8, 10,9,10};
/*{3.28,3.09, 3.52,3.48, 2.88,2.80, 2.46,2.44, 1.87,1.92, 2.19,2.19, 2.77,2.66, 3.74,3.44, 2.55,2.55, 3.78,3.87, 4.07,4.12, 3.31,3.31};
{2,1,1, 3,3,4, 4,5,4, 5,6,5, 7,7,8, 10,9,10};
{{55,39,61,35,50},{29,27,20,39,45},{5,25,11,31,33},{8,12,19,24,12}};
{{9,4,12,8,11,10},{3,2,6,4,9,6}};
{{6,2,9,3},{4,10,4,6},{9,12,8,11}};
{{6,2,9,3,6,2,9,3},{4,10,4,6,4,10,4,6},{9,12,8,11,9,12,8,11}};
 {2,1,1, 3,3,4, 4,5,4, 5,6,5, 7,7,8, 10,9,10};*/

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

  float aa,bb,bb2,cc,tmp=0;
  int i,j,k,dfw,dfb,dfh,dft;

  float b[VER][HOR]={};
  float b2[VER]={};
  float *c=a;
  float ssqw,ssqb,ssqh,ssqt,sh2,sb2,sw2;
  
      
  for(i=0;i<VER;i++)
    for(j=0;j<HOR;j++)
      for(k=0;k<Z;k++)
        b[i][j]+=a[i][j][k];
 
  
  for(i=0;i<VER;i++)
    for(j=0;j<HOR;j++)
      for(k=0;k<Z;k++)
        b2[i]+=a[i][j][k];
 
  aa=sum(c,1,HOR*VER*Z);

  for(i=0;i<VER;i++)
    bb+=sum(b[i],Z,HOR);

  bb2=sum(b2,HOR*Z,VER);

  for(i=0;i<HOR*VER*Z;i++)
    tmp+=c[i];
  cc=(tmp*tmp)/(VER*HOR*Z);

  dfw=VER*HOR*(Z-1);
  dfb=VER*(HOR-1);
  dfh=VER-1;
  dft=VER*HOR*Z-1;

  ssqw=aa-bb;
  ssqb=bb-bb2;
  ssqh=bb2-cc;
  ssqt=aa-cc;

  sh2=ssqh/dfh;
  sb2=ssqb/dfb;
  sw2=ssqw/dfw;

  printf("A=%f\n B1=%f\n B2=%f\n C=%f\n",aa,bb,bb2,cc);
  printf("dfh=%d\n dfb=%d\n dfw=%d\n",dfh,dfb,dfw);
  printf("ssqh=%f\n ssqb=%f\n ssqw=%f\n ssqt=%f\n",ssqh,ssqb,ssqw,ssqt);
  printf("sh2=%f\n sb2=%f\n sw2=%f\n",sh2,sb2,sw2);
  printf("Fhb=%f\n Fbw=%f\n",sh2/sb2,sb2/sw2);

} 
  
