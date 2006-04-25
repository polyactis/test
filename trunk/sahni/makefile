tg=test
cpptg=SeqSearch

.c.o:	
	-gcc -c $< -o $@

.cpp.o:	
	-g++ -c $< -o $@

all: 	$(tg) $(cpptg)

test:	test.o match.o
	-gcc $^ -o $@

$(cpptg):	%:	%.o
	-g++ $< -o $@

clean:	
	-rm *.o $(tg) $(cpptg) *~
