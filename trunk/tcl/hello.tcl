#!/usr/bin/wish  
frame .a;
button .a/b -text "exit" -command exit;
button .a/c -text "ls" -command !ls;
text .a/d;
puts "hello world";
pack .a;
pack .a/d;
pack .a/b;
pack .a/c;
