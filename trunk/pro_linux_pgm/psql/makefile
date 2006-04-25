tg=con del1 sel1 sel2 sel3
all:	$(tg) 

.c.o:	
	-gcc -I/usr/include/pgsql -c $< -o $@

$(tg):	%:	%.o
	-gcc -lpq $< -o $@

clean:
	-rm *.o $(tg) *~
