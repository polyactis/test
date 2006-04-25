obj=hello.o
tg=hello

all:	$(obj) $(tg)

$(obj):	%.o:	%.s
	-nasm -f elf -o $@ $<

$(tg):	%:	%.o
	-ld $< -o $@

clean:	
	-rm *~ $(obj) $(tg)

