c++obj=hello.o Numconv.o Fillvector.o
c++tg=hello Numconv Fillvector

all:	$(c++obj) $(c++tg)

$(c++obj):	%.o:	%.cpp
	-g++ $(CFLAGS) -c $< -o $@

$(c++tg):	%:	%.o
	-g++ $(CFLAGS) $< -o $@

clean:	
	-rm *~ *.o $(c++tg)

