tg=selp1 upd1 selp2
.SUFFIXES: .pgc .c

all:	$(tg) 

.pgc.c:
	-ecpg -t -I /usr/include/pgsql $<
.c.o:	
	-gcc -g -I/usr/include/pgsql -c $< -o $@

$(tg):	%:	%.o
	-gcc -g -lpq -lecpg $< -o $@

clean:
	-rm *.o $(tg) *~
