
CC	=	g++
# use the following cflags for old versions of g++ with sets.old.H
#OLD_CFLAGS	=	-g -Wall -pedantic -fguiding-decls
# use the following for new versions of g++/egcs with sets.H
CFLAGS	=	-O3 -std=c++0x	#-g -pedantic
LINK	=	g++
LFLAGS	=	${CFLAGS} -ldl -ltcl -lefence
OBJECTS = interval_tree.o RedBlackTree.o test.o

.PHONY: test clean 

all:	test
#test: test.exe
#	./test.exe tree_test.tcl

%.o : %.cc
	$(CC) $(CFLAGS) -c $< -o $@

test : $(OBJECTS)
	${LINK} ${LFLAGS} $(OBJECTS) -o test
	./test tree_test.tcl

clean:
	rm -f test *.o *~ MANIFEST
