
#define HOR 1
#define VER 8


float a[VER][HOR]={126,266,60,207,-125,-79,79,-54};
/*{42,48,63,69,70,76,87,84,70,63,72,78,67,66,88,92,89,83};
{-3.2,-3.8,-1.7,-2.1,-4.5, -3.0,-4.4,-1.8,5.3,-0.7, -3.3,-2.3,-2.4,-2.6,-5.7, -1.8,1.3,-1.4,-1.2,-7.9, 4.5,1.0,7.2,4.7,1.0, -2.9,-1.6,0.9,0.6,-1.9, 5.7,-0.7,3.0,18.6,-0.3, -3.6,-4.8,-0.6,2.1,1.8, 2.0,3.4,7.0,2.4,0.5};
{8.53,17.53,39.14,32.00, 20.53,21.07,26.20,23.80, 12.53,20.80,31.33,28.87, 14.00,17.33,45.80,25.06, 10.80,20.07,40.20,29.33};
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

  float aa;
  float bb;
  float cc;
  float tmp;
  int i,j;

  float b[VER];
  float c[HOR*VER];
  float sb2,sw2;
  for(i=0;i<VER;i++)
    b[i]=0;
  
  for(i=0;i<VER;i++)
    for(j=0;j<HOR;j++)
      c[i*HOR+j]=a[i][j];
      
  for(i=0;i<VER;i++)
    for(j=0;j<HOR;j++)
      b[i]+=a[i][j];
  
  aa=sum(c,1,HOR*VER);
  bb=sum(b,HOR,VER);
  for(i=0;i<HOR*VER;i++)
    tmp+=c[i];
  cc=(tmp*tmp)/(VER*HOR);
  sb2=(bb-cc)/(VER-1);
  sw2=(aa-bb)/(HOR*VER-VER);
  printf("A=%f\n B=%f\n C=%f\n",aa,bb,cc);
  printf("df of numerator=%d\n df of denom=%d\n",VER-1,HOR*VER-VER);
  printf("ssqb=%f\n ssqw=%f\n ssqt=%f\n",bb-cc,aa-bb,aa-cc);
  printf("sb2=%f\n sw2=%f\nF=%f\n",sb2,sw2,sb2/sw2);
} 
  
