all:	test

.o:	.c

test:	main.o stack.o
	-gcc  $^ -o $@

clean: 
	-rm *.o test
