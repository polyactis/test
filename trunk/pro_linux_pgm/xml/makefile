tg=sax1
all:	$(tg) 

.c.o:	
	-gcc -I/usr/include/gnome-xml  -c $< -o $@

$(tg):	%:	%.o
	-gcc -lxml -lz $< -o $@

clean:
	-rm *.o $(tg) *~
