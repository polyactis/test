target = thread1 thread2 thread3 test

#CFLAGS = -lpthread

all: $(target)

*.o:	*.c

$(target):	%:	%.o
	-gcc $< -o $@ -lpthread


clean:
	-rm *.o *~ $(target)
