#IDIR=-I/usr/lib/g++-include

f_thread_obj=primes.o thread-create.o thread_create2.o

f_thread_tg=primes thread-create thread_create2

cobj=zombie.o sigusr1.o fork-exec.o main.o create-file.o getopt_long.o arglist.o temp_file.o openfile.o fork.o 

#c++obj=reciprocal.o recip.o 

ctg=sigusr1 zombie fork-exec create-file getopt_long arglist temp_file openfile fork

#c++tg=recip 

all:	$(ctg) $(cobj) $(f_thread_tg) $(f_thread_tg) 
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

$(f_thread_obj):	%.o:	%.c
	-gcc $(CFLAGS) -o $@ -c $<

$(f_thread_tg):	%:	%.o
	-gcc $(CFLAGS) -lpthread -o $@ $<
clean:	
	-rm *.o $(ctg) $(f_thread_tg)
#	-rm *.o reciprocal $(ctg) $(c++tg)
