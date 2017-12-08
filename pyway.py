import sys
from time import sleep
import os
import curses
import signal

def signal_handler(signal, frame):
	curses.endwin()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def print_matrix(matrix):
	for i in range(0, len(matrix)+2):
		win.addch("#")

	for row in matrix:
		win.addch("#")
		for field in row:
			win.addch(field)
		win.addch("#")
	win.refresh()

	try:
		for i in range(0, len(matrix)+2):
			win.refresh()
			win.addch("#")
	except curses.error as e:
		pass

	win.refresh()


def collect_neighbours(matrix, row_index, field_index, x, y):
	neighbours = 0
	# get orthogonal neighbours
	if field_index - 1 >= 0 and matrix[row_index][field_index - 1] == "*": neighbours += 1
	if field_index + 1 < x and matrix[row_index][field_index + 1] == "*": neighbours += 1
	if row_index - 1 >= 0 and matrix[row_index - 1][field_index] == "*": neighbours += 1
	if row_index + 1 < y and matrix[row_index + 1][field_index] == "*": neighbours += 1

	# get the rest
	if field_index - 1 >= 0 and row_index - 1 >= 0 and matrix[row_index - 1][field_index - 1] == "*": neighbours += 1
	if field_index + 1 < x and row_index - 1 >= 0 and matrix[row_index - 1][field_index + 1] == "*": neighbours += 1
	if field_index - 1 >= 0 and row_index + 1 < y and matrix[row_index + 1][field_index - 1] == "*": neighbours += 1
	if field_index + 1 < x and row_index + 1 < y and matrix[row_index + 1][field_index + 1] == "*": neighbours += 1

	return neighbours


def calculate_turn(matrix, x, y):
	tmp = [[None for _ in range(0, x)] for _ in range(0, y)]
	for row_index, row in enumerate(matrix):
		for field_index, field in enumerate(row):
			neighbours = collect_neighbours(matrix, row_index, field_index, x, y)
			if field == "*":
				tmp[row_index][field_index] = "*" if neighbours == 2 or neighbours == 3 else " "
			else:
				tmp[row_index][field_index] = "*" if neighbours == 3 else " "
	return tmp


def insert_5_block(matrix, x, y):
	for i in range(0,5):
		matrix[y-i][x] = "*"
		print_matrix(matrix)


stdscr = curses.initscr()
stdscr.clear()

curses.echo()
curses.nocbreak()
stdscr.keypad(False)

while True:
	stdscr.addstr("Enter x-length: ")
	stdscr.refresh()
	x = stdscr.getstr().decode(encoding="utf-8")
	if x.isnumeric():
		x = int(x)
		break


while True:
	stdscr.addstr("Enter y-length: ")
	stdscr.refresh()
	y = stdscr.getstr().decode(encoding="utf-8")
	if y.isnumeric():
		y = int(y)
		break

matrix = [[" " for _ in range(0, x)] for _ in range(0, y)]
stdscr.clear()
stdscr.refresh()

win = curses.newwin(y+2, x+2, 0, 0)
print_matrix(matrix)

curses.noecho()
curses.cbreak()
win.keypad(True)

current_y = 0
current_x = 0
win.move(current_y, current_x)

while 1:
	c = win.getch()
	try:
		if c == curses.KEY_UP:
			win.move(current_y - 1, current_x)
			current_y, current_x = win.getyx()
		elif c == curses.KEY_DOWN:
			win.move(current_y + 1, current_x)
			current_y, current_x = win.getyx()
		elif c == curses.KEY_LEFT:
			win.move(current_y, current_x - 1)
			current_y, current_x = win.getyx()
		elif c == curses.KEY_RIGHT:
			win.move(current_y, current_x + 1)
			current_y, current_x = win.getyx()
		elif c == ord(" "):
			if 0 < current_x <= x and 0 < current_y <= y:
				if matrix[current_y - 1][current_x - 1] == " ":
					matrix[current_y - 1][current_x - 1] = "*"
				else:
					matrix[current_y - 1][current_x - 1] = " "
				current_y, current_x = win.getyx()
				win.clear()
				print_matrix(matrix)
				win.move(current_y, current_x)
		elif c == ord("\n"):
			break
	except curses.error as e:
		pass

while True:
	win.clear()
	matrix = calculate_turn(matrix, x, y)
	print_matrix(matrix)
	some_left = False
	for row in matrix:
		for field in row:
			if field == "*": some_left = True
	if not some_left:
		break
	sleep(1)

win.clear()
stdscr.clear()
print("\nEveryone is dead!")