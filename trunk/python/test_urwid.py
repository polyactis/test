#!/usr/bin/env python
"""
12-23-05
"""

import urwid.curses_display
import urwid

ui = urwid.curses_display.Screen()

def run():
	cols, rows = ui.get_cols_rows()

	ask = urwid.Edit("What is your name?\n")
	fill = urwid.Filler( ask )
	reply = None

	while True:
		canvas = fill.render( (cols, rows), focus=True )
		ui.draw_screen( (cols, rows), canvas )

		keys = ui.get_input()
		for k in keys:
			if k == "window resize":
				cols, rows = ui.get_cols_rows()
				continue
			if reply is not None:
				return
			if k == "enter": 
				reply = urwid.Text( "Nice to meet you,\n"+
					ask.edit_text+"." )
				fill.body = reply
			if fill.selectable():
				fill.keypress( (cols, rows), k )

#ui.run_wrapper( run )

import time

class Conversation:
	def __init__(self):
		b = urwid.Button('button', self.button_on_press)
		self.items = [ urwid.AttrWrap(b, 'I say', 'footer'), self.new_question() ]
		self.listbox = urwid.ListBox( self.items )
		instruct = urwid.Text("Press Q to exit.")
		header = urwid.AttrWrap( instruct, 'header' )
		self.footer_text = urwid.Text("Testing by Yu Huang %s"%time.ctime())
		footer = urwid.AttrWrap(self.footer_text, 'footer')
		self.top = urwid.Frame(self.listbox, header, footer)
		
	def button_on_press(self, button_object):
		self.footer_text.set_text("button %s get pressed"%button_object.get_label())
		#button_object.set_label("button %s get pressed"%button_object.get_label())
	
	def main(self):
		self.ui = urwid.curses_display.Screen()
		self.ui.register_palette([
			('header', 'black', 'dark cyan', 'standout'),
			('footer', 'dark red', 'light gray', 'underline'),
			('I say', 'dark blue', 'default', 'bold'),
			])
		self.ui.run_wrapper( self.run )
	def run(self):
		size = self.ui.get_cols_rows()

		while True:
			self.draw_screen( size )
			keys = self.ui.get_input()
			if "Q" in keys: 
				break
			for k in keys:
				if k == "window resize":
					size = self.ui.get_cols_rows()
					continue
				self.keypress( size, k )
					
	def keypress(self, size, k):
		if k == "enter":
			widget, pos = self.listbox.get_focus()
			if not hasattr(widget,'get_edit_text'):
				return
			
			answer = self.new_answer( widget.get_edit_text() )
			
			if pos == len(self.items)-1:
				self.items.append( answer )
				self.items.append( self.new_question() )
			else:
				self.items[pos+1:pos+2] = [answer]

			self.listbox.set_focus( pos+2, coming_from='above' )
			widget, pos = self.listbox.get_focus()
			widget.set_edit_pos(0)
		else:
			self.top.keypress( size, k )

	def draw_screen(self, size):
		canvas = self.top.render( size, focus=True )
		self.ui.draw_screen( size, canvas )
	
	def new_question(self):
		return urwid.Edit(('I say',"What is your name?\n"))
	
	def new_answer(self, name):
		return urwid.Text(('I say',"Nice to meet you, "+name+"\n"))
			

Conversation().main()
