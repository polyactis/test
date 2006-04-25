GCOV=-ftest-coverage -fprofile-arcs -fbranch-probabilities
f_thread_tg=

ctg=p58-1-2

c++tg=

all:	$(ctg) $(c++tg) $(f_thread_tg)  

.c.o:
	-gcc $(CFLAGS) -c $< -o $@

.cpp.o:
	-g++ $(CFLAGS) -c $< -o $@

reciprocal:	main.o reciprocal.o
	-gcc $(CFLAGS) -o $@ $^

$(c++tg): 	%:	%.o
	-g++ $(CFLAGS) $(IDIR) $< -o $@ 

$(ctg):	%:	%.o
	-gcc $(CFLAGS)  $< -o $@


$(f_thread_tg):	%:	%.o
	-gcc $(CFLAGS) -lpthread -o $@ $<
clean:	
	-rm *~  *.o $(ctg) $(c++tg) $(f_thread_tg)
