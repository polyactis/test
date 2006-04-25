GNOME_LIBDIR=-L/usr/lib
GNOME_INCLUDEDIR=-I/usr/include -DNEED_GNOMESUPPORT_H -I/usr/lib/gnome-libs/include -I/usr/lib/glib/include -I/usr/X11R6/include
GNOME_LIBS=-lgnome -lgnomeui -lgnomecanvaspixbuf -lgdk_pixbuf -lgdk -lgnomesupport -L/usr/lib -lesd -laudiofile -lm -L/usr/lib -laudiofile -lm -ldb1 -L/usr/lib -lglib -ldl
GNOMEUI_LIBS=-lgnomeui -lart_lgpl -L/usr/lib -lgdk_imlib -L/usr/lib -L/usr/X11R6/lib -lgtk -lgdk -rdynamic -lgmodule -lglib -ldl -lXi -lXext -lX11 -lm -lSM -lICE -L/usr/lib -L/usr/X11R6/lib -lgtk -lgdk -rdynamic -lgmodule -lglib -ldl -lXi -lXext -lX11 -lm -lgnome -lgnomesupport -L/usr/lib -lesd -laudiofile -lm -L/usr/lib -laudiofile -lm -ldb1 -L/usr/lib -lglib -ldl
GTKXMHTML_LIBS=-lgtkxmhtml -lXpm -ljpeg -lpng -lz -lz -lSM -lICE -L/usr/lib -L/usr/X11R6/lib -lgtk -lgdk -rdynamic -lgmodule -lglib -ldl -lXi -lXext -lX11 -lm

CC = gcc


all:	libglade_example	

.c.o:
	-$(CC) $(GNOME_INCLUDEDIR)  -c $< -o $@

libglade_example:	libglade_example.o interface.o
	-$(CC)  $(GNOME_LIBS) `gtk-config --libs` -lglade-gnome -lglade  $^ -o $@


clean:
	-rm *.o *~ libglade_example 
