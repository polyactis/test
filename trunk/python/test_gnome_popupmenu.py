#!/usr/bin/env python
"""
2008-11-03
	an example from  
	http://www.nabble.com/popup-menu-in-gtk.statusicon-under-windows-td19518682.html
	
	author description:
		a script that create a gtk.statusicon, and create a menu that pops up upon right click.
		
		In this menu, there is a submenu, which contain a second menuitem.
	
		The callback of this second menuitem is not called under windows, but it
		is under linux. Is it a bug in windows ? 
"""
import gtk, gobject
import pygtk

def quit_cb(widget, data = None):
	if data:
		data.set_visible(False)
	gtk.main_quit()

def cb(widget, data=None):
	print 'cb'

def popup_menu_cb(widget, button, time, data = None):
	if button == 3:
		if data:
			data.show_all()
			data.popup(None, None, None, 3, time)

def combo_box_changed(combobox, user_param1=None,):
	"""
	2010-4-27
	"""
	print combobox.get_active()
	print combobox.get_active_text()
	

statusIcon = gtk.StatusIcon()

menu = gtk.Menu()
menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
menuItem.connect('activate', quit_cb, statusIcon)
menu.append(menuItem)

sm = gtk.Menu()
menuItem = gtk.MenuItem('asd')
menuItem.set_submenu(sm)
menuItem2 = gtk.MenuItem('asdf')
menuItem2.connect('activate', cb)
sm.append(menuItem2)
menu.append(menuItem)

statusIcon.set_from_stock(gtk.STOCK_HOME)
statusIcon.set_tooltip("StatusIcon test")
statusIcon.connect('popup-menu', popup_menu_cb, menu)
statusIcon.set_visible(True)

## 2010-4-27 testing the combo_box_entry
w = gtk.Window()
w.connect("delete_event", gtk.main_quit)
w.connect("destroy_event", gtk.main_quit)

vbox = gtk.VBox()
w.add(vbox)
w.set_position(gtk.WIN_POS_CENTER)

combo_box_entry =  gtk.ComboBoxEntry()
combo_box_entry.connect("changed", combo_box_changed)
vbox.pack_start(combo_box_entry)

liststore = gtk.ListStore(str)	# str=gobject.TYPE_STRING
combo_box_entry.set_model(liststore)
combo_box_entry.set_text_column(0)	# must. default is -1, which would render later text-appending invisible.
combo_box_entry.append_text("423")
combo_box_entry.append_text("dumbass")

w.show_all()

gtk.main()
