IDIR=-I/usr/lib/g++-include

cobj=1hr-cf.o 2hr-cf.o 2w-cf.o
c++obj= 
ctg=1hr-cf 2hr-cf 2w-cf
c++tg= 

all:	$(ctg) $(c++tg) $(cobj) $(c++obj)  

$(cobj):	%.o:	%.c
	-gcc $(CFLAGS) -c $< -o $@

$(c++obj):	%.o:	%.cpp
	-g++ $(CFLAGS) $(IDIR) -c $< -o $@


$(c++tg): 	%:	%.o
	-g++ $(CFLAGS) $(IDIR) $< -o $@ 
 	
$(ctg):	%:	%.o
	-gcc $(CFLAGS)  $< -o $@
	
clean:	
	-rm *.o $(ctg) $(c++tg)
