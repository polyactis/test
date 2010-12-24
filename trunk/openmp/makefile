target = helloworld_c
cpp_target = helloworld_cpp

CFLAGS = -fopenmp

all: $(target) $(cpp_target)

.c.o:
	-gcc $(CFLAGS) -c $< -o $@ 

.cpp.o:
	-g++ $(CFLAGS) -c $< -o $@

$(target):	%:	%.o
	-gcc $(CFLAGS) $< -o $@

$(cpp_target):	%:	%.o
	-g++ $(CFLAGS) $< -o $@

clean:
	-rm *.o *~ $(target) $(cpp_target)
