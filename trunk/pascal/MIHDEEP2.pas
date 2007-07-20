program  Hoptiln ;       {Maximum likelihood estimate of recent outcrossing rate t0 and tp}
                          {assuming that -there is no linkage disequilibrium between markers }
                          {              -there is no allelic frequency variation over time  }
                          {see Enjalbert and David 2000, Genetics, dec, 154(4) }
{$E+}
{$N+}

{uses  Dos,Crt;}	{2007-07-19 yh: comment it out under linux}

const     npopm=5; nindivm= 2500; nlocm=300; alm=20;  {wich may be modified}

type      matpop   = array [1..npopm] of integer;
          matal    = array [1..nlocm,1..alm] of real;
          matind   = array [1..nlocm] of integer;
          matins   = array [1..nlocm] of real;
          gigo     = array [1..nindivm] of integer;
          giga     = array [1..nindivm,1..nlocm,1..2] of byte;
          

var       base                                   : giga;
          popn,nmax                              : matpop;
          alef                                   : matal;
          ind,ndiplo,htzou,nalleff,nall,totn     : matind;
          panhtz, Fcloc                          : matins;
         

          apop                                   : array [1..npopm] of string[20];
          aloc                                   : array [1..nlocm] of string[6]; {2007-07-19 yh: snpid is 6-digit}
          alec                                   : array [1..nlocm,1..alm] of integer;
          input,nomfreq,nomprob,a,b              : string[20];
          npop,nloc,fin,repeq,repz               : byte;
          signi,tzini,teqini,seuildeltavrais     : real;
          file1                                  : text;
          response                               : char;
          cpop,loc,maille                        : byte;
          nbhtz                                  : gigo;
          prodt,valtz,valteq,probpop             : array[0..21] of real; {probpop >=[1..maille]}
          optiz,optieq                           : array[0..20,0..1] of real;
          nbindivserie                           : array[1..100] of integer;
          jj, nbserie, l, m                      : integer;

function POWER(x:extended;n:integer):extended;
var  shmurf: extended;
 begin
   if x = 0 then POWER := 0
   else if n = 0 then POWER:=1
        else POWER:= exp(n*Ln(x));
   
  end;



(**********************************************************************)
(************** Initialisation courante   *****************************)
(**********************************************************************)

Procedure INIT;

var all                    :integer;
    popi,loci              :integer;


begin
     for loci:=1 to nlocm do begin
         ind[loci]:=0;
         ndiplo[loci]:=0;
         totn[loci]:=0;
         htzou[loci]:=0;
         for all:=1 to alm do begin
             alef[loci,all]:=0;
             alec[loci,all]:=0;
         end;
     end;
end;

(**********************************************************************)
(****   Lecture du fichier de donn�es : remplissage de 'base' *********)
(**********************************************************************)

procedure LECTUREDEB;

var  indi,pop,loc,i,j,k,l,m,cpt       :integer;

begin
     assign (file1,input);
     reset  (file1);
     readln (file1,tzini);	{2007-07-19 yh: tzini, teqini use two readln()}
     readln (file1,teqini);
     {lecture du nombre de pop et du nombre de locus}
     readln (file1,npop,nloc);writeln(npop,' pops,',nloc, ' loci.');
     {lecture des noms de populations et du nb d'ind/population}
     for pop:=1 to npop do
     begin
          readln (file1,apop[pop]);
          readln (file1,nmax[pop]);
	  writeln(apop[pop]);
	  writeln(nmax[pop]);
          {writeln (apop[pop],' : ',nmax[pop]);}
     end;
     {lecture des noms des locus et du nb d'all�les/locus}
     for loc:=1 to nloc do
         begin
          readln (file1,aloc[loc],nall[loc]);
         writeln  (aloc[loc],': ',nall[loc])
     end;
end;

(**********************************************************************)
(****   Lecture du fichier de donn�es : remplissage de 'base' *********)
(**********************************************************************)

procedure LECTUREPOP;

var  indi,loc,i,j,k,l,m,cpt       :integer;
var	mychar	:char;	{2007-07-19 yh: used to read the end character of line}

begin

      {lecture des g�notypes par pop,locus et couple d'all�les}
      
      for indi:=1 to nmax[cpop] do begin
          for loc:=1 to nloc do begin
              read (file1,base[indi,loc,1],base[indi,loc,2]);
              write(base[indi,loc,1],base[indi,loc,2]);
	  read(file1, mychar);	{2007-07-19 yh: read the end character of line}
          end;
          writeln;
      end;
      writeln;
end;

(******************************************************************)
(**** Calcul des fr�q. all�liques pop/pop et comptage des htz *****)
(******************************************************************)

procedure ALEFA;

var   indi,loc            : integer;
      pp,ll,ip            : integer;
      all,a1,a2,a3        : integer;
      jpp,jcc,jal,poin    : integer;
      pi2                 : real;
begin
     for indi:=1 to nmax[cpop] do begin
         nbhtz[indi]:=0;
         for loc:=1 to nloc do
         begin
              a1:=base[indi,loc,1];
              a2:=base[indi,loc,2];
              if a1<>0 then begin
                 alec[loc,a1]:= 1 + alec[loc,a1];
                 ind[loc]:= 1 + ind[loc]; {attention: comptage 2n!}
                 if a2<>0 then begin
                    alec[loc,a2]:=1+ alec[loc,a2];
                    ind[loc]:=1+ind[loc];
                    ndiplo[loc]:=1+ndiplo[loc];   {comptage 1n!}
                    if a1<>a2 then begin              {comptage heterozygues}
                       nbhtz[indi]:= 1 + nbhtz[indi];  {nb loc Htz}
                       htzou[loc] := htzou[loc] + 1;     {nb htz du loc}
                    end;
                 end
              end;
         end; {boucle loc}
     if nloc=0 then write('!!!!!!',indi,loc);
     end;{boucle indi}
 

  {calcul du nb total d'individus/locus, toutes pops cumul�es}
    for loc:=1 to nloc do begin
        totn[loc]:=totn[loc]+ind[loc];
    end;

    {calcul des freq. all�liques et idem pond�r�es}
    
      for loc:=1 to nloc do begin
        pi2:=0;
        for all:=1 to nall[loc] do begin
          if ind[loc]<>0 then begin
            alef[loc,all]:=alec[loc,all]/(ind[loc]);
            pi2:=pi2+(alef[loc,all]*alef[loc,all]);    
            write(all,': ',alef[loc,all],' ');
          end;
        end;
        panhtz[loc]:=2*ind[loc]/((2*ind[loc])-1)*(1-pi2);               {he unbiased}
        writeln('htzpan:',panhtz[loc]);
      end;
    
end;

(******************************************************************)
(***********           Calcul du produit des t           **********)
(******************************************************************)
procedure PRODUIT(tz,teq:real);

var i                                :byte;
    res                              :real;

begin
     prodt[0]:=tz;
     prodt[1]:=(1-tz)*teq;
     res:=1-tz-prodt[1];
     for i:= 2 to fin do begin
         prodt[i] := (1-teq)*prodt[i-1];
         res:=res-prodt[i]
     end;
     prodt[fin+1]:= res;
end;
         




(******************************************************************)
(*********** Calcul des probas d'apparition du g�notype  **********)
(******************************************************************)
procedure PROBINDIV(indiv:integer;tz,teq:real;var proba:real);

var n,loc,a1,a2                                     :byte;
    prodinvar,prodapprox,prodinter,puhtz,prodeb     :extended;
    
begin
 prodapprox:=1; prodinvar:=1; proba:=1;
 puhtz:= POWER(2,nbhtz[indiv]);

 if ((teq=0) and (tz=0)) then 
    if nbhtz[indiv] <> 0 then proba:=-1E30
    else proba:=0
 else (*if ((teq=0) and (nbhtz[indiv]=0)) then proba:=1-tz
      else*)
      begin
          prodeb:=0;
          for n:=0 to fin do begin
              prodinter:=1;
              for loc:= 1 to nloc do begin
                  a1:=base[indiv,loc,1];
                  a2:=base[indiv,loc,2];
                  if ((a1<>0) and (a2<>0)) then
                     if a1 = a2 then
                    {   Calcul du produit sur les premieres generations d'allof}
                    prodinter:= prodinter*(1-(panhtz[loc]/POWER(2,n)));
              end;
              prodeb := prodeb+(prodinter * prodt[n] / POWER(puhtz,n));
          end;
          if nbhtz[indiv]=0 then prodapprox:=prodt[fin+1] else prodapprox:=0;
          proba:= Ln (prodeb + prodapprox);
      end;
end;



(******************************************************************)
(***********  Calcul des produits de proba sur la pop   ***********)
(******************************************************************)

procedure PROBAPOP(tz,teq:real);

var   indi             : integer;
      probind          : real;


begin
     PRODUIT(tz,teq);
     probpop[repeq]:= 0 ;
     for indi:=1 to nmax[cpop] do begin
         PROBINDIV(indi,tz,teq,probind);
         probpop[repeq]:=probpop[repeq] + probind;
     end;
end;
 
(******************************************************************)
(***********        Recherche optimum de t              ***********)
(******************************************************************)

procedure OPTIZONIONS;
var  tz,teq                     : real;
     tiltz,tilteq,repaq       : byte;
     deltaz,deltaeq,oldopti     : real;
     testilteq,testiltz         : boolean;
     tempeq                     : array[0..12,0..1] of real;
begin
     optiz[1,0]:=0;optiz[2,0]:=1;
     optiz[3,0]:=0;optiz[4,0]:=1;
     optiz[1,1]:=0;optiz[2,1]:=1;
     tempeq[1,1]:=0;tempeq[2,1]:=1;

     optieq[1,0]:=0;optieq[2,0]:=1;
     optieq[3,0]:=0;optieq[4,0]:=1;
     deltaeq:=12;
     optieq[1,1]:=0;optieq[2,1]:=1;
     
     While deltaeq>seuildeltavrais do
           begin
           testiltz:=false; optieq[0,0]:=-1E35;
           oldopti:=-1E36; repaq:=1; probpop[0]:=-1E35;
           for repz:=0 to maille do begin
               tz:=(((optiz[2,1]-optiz[1,1])/maille)*repz) + optiz[1,1] ;
               valtz[repz]:=tz;
               testilteq:=false;
               if oldopti>probpop[repaq-1] then repz:=maille;
               oldopti:=probpop[repaq-1];
               for repeq:=0 to maille do begin
                   teq:=(((optieq[2,1]-optieq[1,1])/maille)*repeq) + optieq[1,1] ;
                   valteq[repeq]:=teq;
                   PROBAPOP(tz,teq);
                  
                   if optieq[0,0] <= probpop[repeq] then begin
                      optieq[0,0] := probpop[repeq]; optieq[0,1]:=valteq[repeq]; 
                      optiz[0,1]:=valtz[repz];tilteq:=repeq;tiltz:=repz;
                      testiltz:=true;testilteq:=true;
                   end;
                   repaq:=repeq;
                   if repeq >0 then if probpop[repeq-1]>probpop[repeq]
                                       then begin repaq:=repeq;repeq:=maille;end;

                   if tz=1 then begin repaq:=repeq;repeq:=maille;
                                      valteq[0]:=0;valteq[1]:=1;end;
               end;
               if testilteq then
               if tilteq=0 then begin
                  tempeq[1,0]:=probpop[0]; tempeq[2,0]:=probpop[1];
                  tempeq[1,1]:= valteq[0]; tempeq[2,1]:= valteq[1];
               end
               else if tilteq = maille then begin
                    tempeq[1,0]:=probpop[maille-1]; tempeq[2,0]:=probpop[maille];
                    tempeq[1,1]:= valteq[maille-1]; tempeq[2,1]:= 2*valteq[maille]-valteq[maille-1];
                    if tempeq[2,1]>1 then tempeq[2,1]:=1;
               end
               else begin
                    tempeq[1,0]:=probpop[tilteq-1]; tempeq[2,0]:=probpop[tilteq+1];
                    tempeq[1,1]:= valteq[tilteq-1]; tempeq[2,1]:= valteq[tilteq+1];
               end;
               
           end;
           if testiltz then if tiltz=0 then begin
              optiz[1,1]:= valtz[0];  optiz[2,1]:= valtz[1];
           end
           else if tiltz=maille then begin
                optiz[1,1]:= valtz[maille-1];
                optiz[2,1]:= 2*valtz[maille]-valtz[maille-2];
                if optiz[2,1] > 1 then optiz[2,1] := 1;
           end
                else begin
                     optiz[1,1]:= valtz[tiltz-1];  optiz[2,1]:= valtz[tiltz+1];
                end;
           optieq[1,0]:=tempeq[1,0]; optieq[2,0]:=tempeq[2,0];
           optieq[1,1]:=tempeq[1,1]; optieq[2,1]:=tempeq[2,1];
           writeln( 'tz:',optiz[0,1],'  teq:',optieq[0,1],'v:',optieq[0,0]);
           
           
           if optieq[0,0]=0 then deltaeq := (optieq[1,0]+optieq[2,0])/optieq[2,0]
           else deltaeq:=(optieq[1,0]+optieq[2,0])/2/optieq[0,0];

     end;
end;

(********************************************************************)
(*********** Ouverture fichier  des fr�quences all�liques ***********)
(********************************************************************)

procedure OUVRFREQ(outfreq : string);

var   file4               :text;
      


begin

 assign  (file4,outfreq);
 rewrite (file4);

 writeln (file4);
 writeln(file4,'        ALLELIC FREQUENCIES IN THE POPULATIONS        ');
 writeln (file4); writeln (file4);
 close (file4);
end; 

  
(********************************************************************)
(******** Remplissage du tableau des fr�quences all�liques **********)
(********************************************************************)

procedure PRINTFREQ(outfreq : string);

var   file4               :text;
      all,loc,i,j         :integer;


begin
 assign (file4,outfreq);
 append (file4);
 Writeln(file4,'population n� ', cpop,' :  ',apop[cpop]);
 for loc:=1 to nloc do begin
     write(file4,'Locus : ',aloc[loc]);
     for all:=1 to nall[loc] do
         write(file4,'      ',alef[loc,all]:5:3,'  ');     {freq all�liques}
     write(file4,'     heterozygote number:',htzou[loc],'He:',panhtz[loc]:5:3);
     writeln(file4);
 end;

 close (file4);
end;



(******************************************************************)
(***********            Cr�ation de fichier             ***********)
(******************************************************************)

FUNCTION LeadingZero(w : WORD) : STRING;
VAR
  s : STRING;
BEGIN
  Str(w:0,s);
  IF Length(s) = 1 THEN
    s := '0' + s;
  LeadingZero := s;
END;


(******************************************************************)
(***********            Edition fichier des probas      ***********)
(******************************************************************)

procedure OUVRPROB(fich : string);

CONST
  jours : ARRAY [0..6] OF STRING[8] =
    ('Sunday','Monday','Tusday',
     'Wenesday','Thursday','Friday',
     'Saturday');
  mois  : ARRAY[0..11] OF STRING[9] =
     ('January','F�bruary','March','April','May','June','July',
      'August','September','October','November','December');
VAR
  a, m, j, js            : WORD;
  h, min, s, hund          : WORD;
  file2                  :text;
  cpt                    :byte;
      
begin
 assign (file2,fich);
 rewrite(file2);
 {GetDate(a,m,j,js);
 GetTime(h,min,s,hund);

 WriteLn(file2,fich,',', jours[js],' the',j:0,' ',mois[m],' ', a:0,
          ' � ',LeadingZero(h),'h',LeadingZero(min),'mn.');
 }
 Writeln(file2,'Maximum Likelihood estimate of To and Tp, the last outcrossing rate');
 Writeln(file2, 'and the mean of previous ones respectively.');
 Writeln(file2,' Data file used: ', input);
 writeln;
 writeln(file2,'pop. nb ind.  t0-test    tp-test  -> likelihood-test    t0 est.   tp est. ->  Max.likelihood*');

 close(file2);
end;


(******************************************************************)
(***********            Edition fichier des probas      ***********)
(******************************************************************)

procedure PRINTPROB(fich : string);


VAR
  file3                  :text;
      
begin
 assign (file3,fich);
 append(file3);

 repeq:=0;PROBAPOP(tzini,teqini);
 write(file3,apop[cpop],'  ', nmax[cpop] ,'  ', tzini:12, ' ',teqini:12,' ',probpop[0]:18 );
 writeln(file3,' ', optiz[0,1]:12 ,' ', optieq[0,1]:12 ,' ', optieq[0,0]:18);

 close(file3);
end;








(******************************************************************)
(*********************** affichage de messages a l"ecran***********)
(******************************************************************)

procedure SCREEN1;

var  aa          :integer;
begin
  
  for aa:=1 to 3 do
     writeln;
  writeln ('               COMPUTING ALLELIC FREQUENCIES ...');
end;

(******************************************************************)

procedure SCREEN2;

Var   aa       :integer;

begin
  for aa:=1 to 3 do writeln;
  writeln ('                        COMPUTING PROBABILITIES');
end;



(******************************************************************)
(*********************  Programme principal  **********************)
(******************************************************************)


BEGIN

      
      {writeln ('Input data file, Populations names,loci names and');
      write ('Genotypes coding: '); readln (input);
      }
      input := ParamStr(1); {2007-07-19 yh: use the command line arguments}
      fin:=10; maille:=7; seuildeltavrais:=1.000001;

              nomfreq := input + '.fr';
              nomprob := input + '.ph';
              writeln('input file: ',input);
	      writeln('freq output: ', nomfreq);
	      writeln('proba output: ', nomprob);
              LECTUREDEB;
              OUVRPROB(nomprob);
              OUVRFREQ(nomfreq);
                  for cpop:= 1 to npop do begin
                      INIT;
                      LECTUREPOP;
                      SCREEN1; ALEFA;  
                      PRINTFREQ(nomfreq);
                      SCREEN2;
                      OPTIZONIONS;
                      PRINTPROB(nomprob);
                  end;
              close(file1);
         

END.
