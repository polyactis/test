#ifdef HAVE_CONFIG_H
#  include <config.h>
#endif

#include <gnome.h>

#include "callbacks.h"
#include "interface.h"
#include "support.h"


void
on_button1_clicked                     (GtkButton       *button,
                                        gpointer         user_data)
{
  GtkWidget * dialog1,*entry,*txt;
  const char *text;
  int i;
  dialog1=create_dialog1();
  
  entry=lookup_widget(GTK_WIDGET(button),"entry1");
  text=gtk_editable_get_chars(GTK_EDITABLE(entry),0,-1);

  do{
    txt=gtk_object_get_data(GTK_OBJECT(dialog1),"text1");
    gtk_text_insert((GtkText*)txt,NULL,NULL,NULL,text,strlen(text));

    gtk_widget_show(dialog1);
    while(gtk_events_pending())
      gtk_main_iteration();
  }while(1);
}


gboolean
on_window1_delete_event                (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data)
{
  gtk_main_quit();
  return FALSE;
}




