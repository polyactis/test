SUBDIRS = swig
.PHONY: clean_subdirs subdirs $(SUBDIRS)

GCOV=-ftest-coverage -fprofile-arcs -fbranch-probabilities
f_thread_tg=primes thread-create thread_create2

ctg=cdrom-eject select inet socket-inet socket-server socket-client shm listdir dir sigusr1 zombie fork-exec create-file getopt_long arglist temp_file openfile fork

c++tg=recip 

all:	$(ctg) $(c++tg) $(f_thread_tg)  reciprocal subdirs


subdirs:	$(SUBDIRS)
	$(MAKE) -C $<
	
clean_subdirs:	$(SUBDIRS)
	$(MAKE) -C $< clean
	
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

clean:	clean_subdirs
	-rm -f *~  *.bb *.bbg *.da *.gcov *.o reciprocal $(ctg) $(c++tg) $(f_thread_tg)
