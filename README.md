This script uses Python/Tkinter to generate number sequences for mail merge apps like CorelDRAW.

The interface is really simple,

Starting Number = Number to start counting from
Ending Number = Number to end at
Brace Expansion = This one is a bit complicated and we'll get to it later
Padding = Amount of 0's to pad the number
Document Repeats = Amount of number's to use per "page"
Prefix = Add this string to the front of every number
Stackable = Should the numbers run sequentially, or "down". Mostly used by people printing books

Brace expansion is a lot similar to BASH's brace expansion, supplying a string like A{1..3}S will result in numbers A1S A2S A3S and so on. Very usefull for printing seating arrangement tickets.
