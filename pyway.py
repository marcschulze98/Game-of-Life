import sys
from time import sleep
import os


def print_matrix(matrix):
	for i in range(0, len(matrix)+2):
		sys.stdout.write("#")
	print()
	for row in matrix:
		sys.stdout.write("#")
		for field in row:
			sys.stdout.write(field)
		sys.stdout.write("#")
		print()
	for i in range(0, len(matrix)+2):
		sys.stdout.write("#")
	print()


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
	tmp = [[None for index in range(0, x)] for index in range(0, y)]
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


print("enter x:")
x = int(input())
print("enter y:")
y = int(input())

matrix = [[" " for index in range(0, x)] for index in range(0, y)]
print_matrix(matrix)

insert_5_block(matrix, 10, 7)
# while True:
# 	print("enter x:")
# 	tmpx = input()
# 	if tmpx == "": break
# 	tmpx = int(tmpx)
# 	print("enter y:")
# 	tmpy = input()
# 	if tmpy == "": break
# 	tmpy = int(tmpy)
# 	matrix[tmpy][tmpx] = "*"
# 	print_matrix(matrix)

while True:
	sleep(1)
	os.system("clear")
	matrix = calculate_turn(matrix, x, y)
	print()
	print_matrix(matrix)
