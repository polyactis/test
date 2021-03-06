#!/usr/bin/env python
#12-22-05
#mostly copied from popcorn.py in python-newt's examples directory

from snack import *

t = TextboxReflowed(25, "Some text which needs to be wrapped at a good place.")
li = Listbox(5, width = 20, returnExit = 1)
li.append("First", "f")
li.append("Second", "s")
li.insert("Another", "a", "f")
li.delete("a")
ct = CheckboxTree(5, scroll = 1)
ct.append("Colors")
ct.addItem("Red", (0, snackArgs['append']), "red item key")
ct.addItem("Yellow", (0, snackArgs['append']))
ct.addItem("Blue", (0, snackArgs['append']))
ct.append("Flavors")
ct.addItem("Vanilla", (1, snackArgs['append']))
ct.addItem("Chocolate", (1, snackArgs['append']))
ct.addItem("Stawberry", (1, snackArgs['append']))
ct.append("Numbers")
ct.addItem("1", (2, snackArgs['append']))
ct.addItem("2", (2, snackArgs['append']))
ct.addItem("3", (2, snackArgs['append']))
ct.append("Names")
ct.addItem("Matt", (3, snackArgs['append']))
ct.addItem("Shawn", (3, snackArgs['append']))
ct.addItem("Wilson", (3, snackArgs['append']))
ct.append("Months")
ct.addItem("February", (4, snackArgs['append']))
ct.addItem("August", (4, snackArgs['append']))
ct.addItem("September", (4, snackArgs['append']))
ct.append("Events")
ct.addItem("Christmas", (5, snackArgs['append']))
ct.addItem("Labor Day", (5, snackArgs['append']))
ct.addItem("My Vacation", (5, snackArgs['append']))
b = Button("Button")
e = Entry(15, "Entry")
l = Label("label")
cb = Checkbox("checkbox")
r1 = SingleRadioButton("Radio 1", None, 1)
r2 = SingleRadioButton("Radio 2", r1)

screen = SnackScreen()
tb = Textbox(35,5,'abc',scroll=1, wrap=1)
tb.setText('This is a test huge mateareal dfasdfsafd fdasf fdsa f dfajkljfafsjlfsa fjksafjsalfjslfjsl')

sg = GridForm(screen, "My Test", 2, 4)
sg.add(b, 0, 0, anchorLeft = 1)
sg.add(e, 1, 0, (1, 0, 0, 0), anchorLeft = 1, anchorTop = 1)
sg.add(li, 0, 1, (0, 1, 0, 0), anchorLeft = 1)
sg.add(cb, 1, 1, (1, 1, 0, 0), anchorLeft = 1)
sg.add(r1, 0, 2, (0, 0, 0, 0), anchorLeft = 1)
sg.add(r2, 1, 2, (1, 0, 0, 0), anchorLeft = 1)
sg.add(tb, 0, 3)

sg.runPopup()
screen.finish()
