#!/usr/bin/env python

import curses,sys,termios,tty

stdscr = curses.initscr()
curses.start_color()
begin_x = 20
begin_y = 7
height = 3
width = 40
win = curses.newwin(height, width, begin_y, begin_x)
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
stdscr.box(0,0)
if curses.has_colors():
	termname = curses.termname()
	stdscr.addstr('%s Color available\n'%termname)
while 1:
	c = stdscr.getch()
	if c == ord('p'):
		try:
			stdscr.addstr(23,1,'Current mode: Typing mode',curses.color_pair(1))
		except:
			sys.stderr.write('error occured\n')
			break
	elif c == ord('c'):
		stdscr.clear()
	elif c == ord('q'):
		break  # Exit the while()
	elif c == curses.KEY_HOME: x = y = 0
	
curses.nocbreak();
stdscr.keypad(0)
curses.echo()
curses.endwin()

def getpass(prompt = "Password: "):
    fd = sys.stdout.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    #new[1] = new[1] & termios.ICANON
    #new[1] = new[1] & termios.OFDEL
    new[1] = new[1] & termios.OLCUC
    #new[1] = new[1] & ~termios.CEOL          # lflags
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        for i in range(10):
          sys.stdout.write('avD\n')
        passwd = raw_input(prompt)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return passwd

passwd = getpass()
print passwd
