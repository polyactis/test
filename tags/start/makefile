#IDIR=-I/usr/lib/g++-include

cobj=thread_create2.o thread-create.o zombie.o sigusr1.o fork-exec.o main.o create-file.o getopt_long.o arglist.o temp_file.o openfile.o fork.o 
#c++obj=reciprocal.o recip.o 
ctg=thread_create2 thread-create sigusr1 zombie fork-exec create-file getopt_long arglist temp_file openfile fork
#c++tg=recip 

all:	$(ctg) $(cobj)
#all:	$(ctg) $(c++tg) $(cobj) $(c++obj) reciprocal 

$(cobj):	%.o:	%.c
	-gcc $(CFLAGS) -c $< -o $@

#$(c++obj):	%.o:	%.cpp
#	-g++ $(CFLAGS) $(IDIR) -c $< -o $@

#reciprocal:	main.o reciprocal.o
#	-gcc $(CFLAGS) -o $@ $^

#$(c++tg): 	%:	%.o
#	-g++ $(CFLAGS) $(IDIR) $< -o $@ 
 	
$(ctg):	%:	%.o
	-gcc $(CFLAGS)  $< -o $@
	
clean:	
	-rm *.o $(ctg)
#	-rm *.o reciprocal $(ctg) $(c++tg)
