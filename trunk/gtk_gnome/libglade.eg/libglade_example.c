#include <glade/glade.h>
#include <gnome.h>

#include "libglade_example.h"
#include "interface.h"
GladeXML *xml;

void
on_button1_clicked                     (GtkButton       *button,
                                        gpointer         user_data)
{
  GtkWidget * dialog1,*entry,*txt;
  const char *text;
  dialog1=create_dialog1();
  
  entry=glade_xml_get_widget(xml,"entry1");
  text=gtk_editable_get_chars(GTK_EDITABLE(entry),0,-1);
  
  txt=gtk_object_get_data(GTK_OBJECT(dialog1),"text1");
  gtk_text_insert((GtkText*)txt,NULL,NULL,NULL,text,strlen(text));
  gtk_widget_show(dialog1);

}


gboolean
on_window1_delete_event                (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data)
{
  gtk_main_quit();
  return FALSE;
}


gint main(gint argc,gchar** argv)
{
  GtkWidget* window1;
  gnome_init("libglade_example","0.1",argc,argv);
  glade_gnome_init();

  xml=glade_xml_new("libglade_example.glade",NULL);

  if(!xml)
  {
    g_warning("could not load interface\n");
    return 1;
  
  }

  //window1=glade_xml_get_widget(xml,"window1");
  //gtk_widget_show(window1);

  glade_xml_signal_autoconnect(xml);
  gtk_main();
  return 0;

}
  

