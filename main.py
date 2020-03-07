from cell import Cell
from coordinate import Coordinate 
from cell_entry import CellEntry
from intent import Intent
from obstacle import Obstacle
from os import system, name 

import random

MAX_OBSTACLES = 5
DEFAULT_ORIENTATION_MIN_VALUE = 1
DEFAULT_ORIENTATION_MAX_VALUE = 2

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def is_valid_obstacle(grid, x, y, length, width):
	for i in range(0, length):
		for j in range(0, width):
			if grid[i + x][j + y].cell_entry != CellEntry.EMPTY:
				return False
	return True

def fill_grid_with_obstacle(grid, x, y, length, width):
	for i in range(0, length):
		for j in range(0, width):
			grid[i + x][j + y].cell_entry = CellEntry.OBSTACLE;

def generate_obstacle(grid, rows, cols):

	#Toss a coin to decide if the obstacle needs to be vertical or horizontal (0 for vertical/1 for horizonal)
	orientation = random.choice([0, 1])

	cell_x = random.randrange(0, rows - 1, 1)
	cell_y = random.randrange(0, cols - 1, 1)

	print("cell_x: " + str(cell_x))
	print("cell_y: " + str(cell_y))
	
	if orientation == 0:
		obstacle_length = random.randrange(2, rows - cell_x, 1)
		obstacle_width = random.choice([DEFAULT_ORIENTATION_MIN_VALUE, DEFAULT_ORIENTATION_MAX_VALUE])
	else:
		obstacle_length = random.choice([DEFAULT_ORIENTATION_MIN_VALUE, DEFAULT_ORIENTATION_MAX_VALUE])
		obstacle_width = random.randrange(2, cols - cell_y, 1)

	print("Obstacle length: " + str(obstacle_length))
	print("Obstacle width: " + str(obstacle_width))


	is_valid = is_valid_obstacle(grid, cell_x, cell_y, obstacle_length, obstacle_width)

	while not is_valid:
		print("Not valid")
		cell_x = random.randrange(0, rows - 1, 1)
		cell_y = random.randrange(0, cols - 1, 1)

		is_valid = is_valid_obstacle(grid, cell_x, cell_y, obstacle_length, obstacle_width)

	fill_grid_with_obstacle(grid, cell_x, cell_y, obstacle_length, obstacle_width)

	return obstacle_length, obstacle_width, cell_x, cell_y, grid


def render_flying_area(grid, rows, cols):
	clear()

	full_str = ''
	for i in range(rows):
		for k in range(cols * 4):
			full_str += '-'
		full_str += '\n'
		
		col_str = '| '
		for j in range(cols):
			cell_value = grid[i][j].cell_entry.value
			if grid[i][j].cell_entry.value == 1:
				col_str += "X | "
			else:
				col_str += "  | "

		col_str += '\n'
		full_str += col_str


	for k in range(cols * 4):
		full_str += '-'
	print(full_str)

	
if __name__ == '__main__':

	print("Fix the grid size")
	rows = int(input("Enter the number of rows: "))
	cols = int(input("Enter the number of columns: "))

	#Create a two dimensional grid of FlyingAreas
	grid = [ [Cell("EMPTY") for j in range(cols)] for i in range(rows) ]

	num_obstacles = int(input("Enter the number of obstacles(0 - " + str(MAX_OBSTACLES) + "): "))

	while num_obstacles > MAX_OBSTACLES:
		print("The number of obstacles can't be more than ", MAX_OBSTACLES)
		num_obstacles = int(input("Enter the number of obstacles(0 - " + str(MAX_OBSTACLES) + "): "))


	obstacles = []

	intent_values = []
	
	for intent in Intent:
		intent_values.append(intent.value)

	for i in range(0, num_obstacles):
		for intent in Intent:
			print('{:15} = {}'.format(intent.name, intent.value))
		
		intent_input = int(input("Enter the intent for obstacle " + str(i + 1) + ": "))
		
		while intent_input not in intent_values:
			print("Enter a value from the list")

			for intent in Intent:
				print('{:15} = {}'.format(intent.name, intent.value))
		
			intent_input = int(input("Enter the intent for obstacle " + str(i + 1) + ": "))


		length, width, x, y, grid = generate_obstacle(grid, rows, cols)
	
		obstacles.append(Obstacle(x, y, length, width, intent_input))


	render_flying_area(grid, rows, cols)
		