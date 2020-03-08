from cell import Cell
from coordinate import Coordinate 
from cell_entry import CellEntry
from intent import Intent
from obstacle import Obstacle
from output_data import OutputData
from obstacle_output import ObstacleOutput
from os import system, name 
import matplotlib.pyplot as plt

import random
import json

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

# The generated obstacle 
# 1) Doesn't intersect with any of the previously created obstacles
# 2) Doesn't block the start and goal cells
def is_valid_obstacle(grid, x, y, length, width, rows, cols):
	for i in range(0, length):
		if i + x >= rows:
			return False
		for j in range(0, width):

			if j + y >= cols:
				return False

			if i + x == 0 and j + y == cols - 1:
				return False

			if i + x == rows - 1 and j + y == 0:
				return False

			if grid[i + x][j + y].cell_entry != CellEntry.EMPTY:
				return False
	return True

def fill_grid_with_obstacle(grid, x, y, length, width, obstacle_number):
	for i in range(0, length):
		for j in range(0, width):
			grid[i + x][j + y].cell_entry = CellEntry.OBSTACLE;
			grid[i + x][j + y].obstacle_number = obstacle_number
			grid[i + x][j + y].is_obstacle = True

#Needs some more intelligence in creating the obstacles
def generate_obstacle(grid, rows, cols, obstacle_number):

	#Toss a coin to decide if the obstacle needs to be vertical or horizontal (0 for vertical/1 for horizonal)
	orientation = random.choice([0, 1])

	cell_x = random.randint(0, rows - 2)
	cell_y = random.randint(0, cols - 2)

	#This is used to ensure that the obstacles don't cover the entire row or column
	random_subtractor = random.randint(2,5)
	
	if orientation == 0:
		obstacle_length = random.randint(2, rows - cell_x)
		obstacle_width = random.choice([DEFAULT_ORIENTATION_MIN_VALUE, DEFAULT_ORIENTATION_MAX_VALUE])
	else:
		obstacle_length = random.choice([DEFAULT_ORIENTATION_MIN_VALUE, DEFAULT_ORIENTATION_MAX_VALUE])
		obstacle_width = random.randint(2, cols - cell_y)


	#Not a great logic 
	if obstacle_length > cols/2:
		obstacle_length -= random_subtractor

	if obstacle_width > rows/2:
		obstacle_width -= random_subtractor

	is_valid = is_valid_obstacle(grid, cell_x, cell_y, obstacle_length, obstacle_width, rows, cols)

	while not is_valid:
		cell_x = random.randint(0, rows - 1)
		cell_y = random.randint(0, cols - 1)

		is_valid = is_valid_obstacle(grid, cell_x, cell_y, obstacle_length, obstacle_width, rows, cols)

	fill_grid_with_obstacle(grid, cell_x, cell_y, obstacle_length, obstacle_width, obstacle_number)

	return obstacle_length, obstacle_width, cell_x, cell_y, grid


def render_flying_area(grid, rows, cols):
	clear()

	full_str = 'Current position is indicated by *\n'
	for i in range(rows):
		full_str += "   "
		
		for k in range(cols * 4):
			full_str += '-'
		full_str += '\n'
		
		if i == rows - 1:
			col_str = "==>| "
		else:
			col_str = '   | '
		
		for j in range(cols):
			cell_entry = grid[i][j].cell_entry
			if cell_entry == CellEntry.OBSTACLE:
				col_str += "O" + str(grid[i][j].obstacle_number + 1) + "| "
			elif cell_entry == CellEntry.CURRENT:
				col_str += "* | "
			elif cell_entry == CellEntry.UP:
				col_str += "U | "
			elif cell_entry == CellEntry.RIGHT:
				col_str += "R | "
			elif cell_entry == CellEntry.LEFT:
				col_str += "L | "
			elif cell_entry == CellEntry.DOWN:
				col_str += "D | "
			elif cell_entry == CellEntry.VISITED_OBSTACLE:
				col_str += "VO| "
			elif cell_entry == CellEntry.LEFT_UP:
				col_str += "LU| "
			elif cell_entry == CellEntry.RIGHT_UP:
				col_str += "RU| "
			elif cell_entry == CellEntry.LEFT_DOWN:
				col_str += "LD| "
			elif cell_entry == CellEntry.RIGHT_DOWN:
				col_str += "RD| "
			else:
				col_str += "  | "

		if i == 0:
			col_str += " <== Goal "
		col_str += '\n'
		full_str += col_str


	full_str += "   "
	for k in range(cols * 4):
		full_str += '-'
	print(full_str)


def check_intent_avoidance_violation(grid, rows, cols, moves, obstacles):

	violated_intents = []
	for move in moves:
		if grid[move.x][move.y].is_obstacle:
			obstacle_number = grid[move.x][move.y].obstacle_number

			obstacle = obstacles[obstacle_number]

			if obstacle.intent == Intent.AVOID:
				if obstacle_number + 1 not in violated_intents:
					violated_intents.append(obstacle_number + 1)


	for i in range(len(violated_intents)):
		obstacles[violated_intents[i] - 1].intent_violation = True
	
	return violated_intents


def check_intent_reach_violation(grid, rows, cols, moves, obstacles):
	should_reach_obstacles = set()

	for obs in obstacles:
		if obs.intent == Intent.REACH:
			should_reach_obstacles.add(obs.number + 1)

	for move in moves:
		if grid[move.x][move.y].is_obstacle:
			obstacle_number = grid[move.x][move.y].obstacle_number

			if obstacle_number + 1 in should_reach_obstacles:
				should_reach_obstacles = should_reach_obstacles - set([obstacle_number])

	should_reach_obstacles = list(should_reach_obstacles)

	for i in range(len(should_reach_obstacles)):
		obstacles[should_reach_obstacles[i] - 1].intent_violation = True
	
	return should_reach_obstacles
	

def fly(grid, rows, cols):

	moves = []

	current_pos = Coordinate(rows - 1, 0)

	while current_pos.x != 0 or current_pos.y != cols - 1:
		move = input("Press w -> UP, a -> LEFT, s -> DOWN, d -> RIGHT, i -> LEFT_UP, o -> RIGHT_UP, j -> LEFT_DOWN, k -> RIGHT_DOWN: ")

		if move == 'w' or move == 'W':
			if current_pos.x - 1 >= 0:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.UP

				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x - 1][current_pos.y].cell_entry = CellEntry.CURRENT
				current_pos.x = current_pos.x - 1
		elif move == 'a' or move == 'A':
			if current_pos.y - 1 >= 0:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.LEFT
				
				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x][current_pos.y - 1].cell_entry = CellEntry.CURRENT
				current_pos.y= current_pos.y - 1
		elif move == 's' or move == 'S':
			if current_pos.x + 1 < rows:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.DOWN
				
				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x + 1][current_pos.y].cell_entry = CellEntry.CURRENT
				current_pos.x= current_pos.x + 1
		elif move == 'd' or move == 'D':
			if current_pos.y + 1 < cols:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.RIGHT
				
				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x][current_pos.y + 1].cell_entry = CellEntry.CURRENT
				current_pos.y= current_pos.y + 1
		elif move == 'i' or move == 'I':
			if current_pos.x - 1 >= 0 and current_pos.y - 1 >= 0:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.LEFT_UP

				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x - 1][current_pos.y - 1].cell_entry = CellEntry.CURRENT
				current_pos.x = current_pos.x - 1
				current_pos.y = current_pos.y - 1
		elif move == 'o' or move == 'O':
			if current_pos.x - 1 >= 0 and current_pos.y + 1 < cols:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.RIGHT_UP

				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x - 1][current_pos.y + 1].cell_entry = CellEntry.CURRENT
				current_pos.x = current_pos.x - 1
				current_pos.y = current_pos.y + 1
		elif move == 'j' or move == 'J':
			if current_pos.x + 1 < rows and current_pos.y - 1 >= 0:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.LEFT_DOWN

				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x + 1][current_pos.y - 1].cell_entry = CellEntry.CURRENT
				current_pos.x = current_pos.x + 1
				current_pos.y = current_pos.y - 1
		elif move == 'k' or move == 'k':
			if current_pos.x + 1 < rows and current_pos.y + 1 < cols:
				if grid[current_pos.x][current_pos.y].is_obstacle:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.VISITED_OBSTACLE
				else:
					grid[current_pos.x][current_pos.y].cell_entry = CellEntry.RIGHT_DOWN

				moves.append(Coordinate(current_pos.x, current_pos.y))
				grid[current_pos.x + 1][current_pos.y + 1].cell_entry = CellEntry.CURRENT
				current_pos.x = current_pos.x + 1
				current_pos.y = current_pos.y + 1

		else:
			print("Press a correct option")

		render_flying_area(grid, rows, cols)
	moves.append(Coordinate(current_pos.x, current_pos.y))

	return moves

def plot_moves(moves):
	plot_x = []
	plot_y = []
	for move in moves:

		plot_x.append(move.x)
		plot_y.append(move.y)

	plt.plot(plot_x, plot_y)
	plt.plot(plot_x[0], plot_y[0], 'go', ms=8)
	plt.plot(plot_x[len(plot_x) - 1], plot_y[len(plot_y) - 1], 'bo', ms=8)

def plot_obstacles(obstacles):

	all_obstacles_points = []
	count = 1
	for obs in obstacles: 

		obstacle_points = []
		obs_x = []
		obs_y = []
		
		obs_x.append(obs.x)
		obs_y.append(obs.y)

		obstacle_points.append(Coordinate(obs.x, obs.y))

		obs_x.append(obs.x + obs.length - 1)
		obs_y.append(obs.y)

		obstacle_points.append(Coordinate(obs.x + obs.length - 1, obs.y))

		obs_x.append(obs.x + obs.length - 1)
		obs_y.append(obs.y + obs.width - 1)

		obstacle_points.append(Coordinate(obs.x + obs.length - 1, obs.y + obs.width - 1))

		obs_x.append(obs.x)
		obs_y.append(obs.y + obs.width - 1)

		obstacle_points.append(Coordinate(obs.x, obs.y + obs.width - 1))

		obs_x.append(obs.x)
		obs_y.append(obs.y)

		plt.plot(obs_x, obs_y, linewidth=3.0, label='obs')

		if obs.intent_violation == True:
			plt.plot(obs.x, obs.y, 'rX', ms=8)
			plt.plot(obs.x + obs.length - 1, obs.y, 'rX', ms=8)
			plt.plot(obs.x + obs.length - 1, obs.y + obs.width - 1, 'rX', ms=8)
			plt.plot(obs.x, obs.y + obs.width - 1, 'rX', ms=8)

		count += 1

		all_obstacles_points.append(obstacle_points)

	return all_obstacles_points


def convert_to_dict(obj):
  obj_dict = {}
  obj_dict.update(obj.__dict__)
  
  return obj_dict
	
if __name__ == '__main__':

	print("Fix the grid size")
	rows = int(input("Enter the number of rows: "))
	cols = int(input("Enter the number of columns: "))

	#Create a two dimensional grid of cells
	grid = [ [Cell("EMPTY") for j in range(cols)] for i in range(rows) ]


	grid[rows-1][0].cell_entry = CellEntry.CURRENT

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


		length, width, x, y, grid = generate_obstacle(grid, rows, cols, i)
	
		obstacles.append(Obstacle(i, x, y, length, width, intent_input))


	render_flying_area(grid, rows, cols)

	moves = fly(grid, rows, cols)

	avoidance_violated_intents = check_intent_avoidance_violation(grid, rows, cols, moves, obstacles)

	print("Avoidance violated intents: ")
	print(avoidance_violated_intents)

	reach_violated_intents = check_intent_reach_violation(grid, rows, cols, moves, obstacles)
	print("Reach violated intents: ")
	print(reach_violated_intents)
	
	plot_moves(moves)
	all_obstacles_points = plot_obstacles(obstacles)

	# Generating output data

	start_pos = Coordinate(rows - 1, 0)
	goal_pos = Coordinate(0, cols - 1)

	obstacles_output = []
	for i in range(len(all_obstacles_points)):
		name = 'obstactle'+str(i+1)
		intent = obstacles[i].intent.name
		coordinates = all_obstacles_points[i]
		intent_violation = obstacles[i].intent_violation

		obstacles_output.append(ObstacleOutput(name, intent, coordinates, intent_violation))


	output_data = OutputData(rows, cols, start_pos, goal_pos, obstacles_output, moves)
	json_data = json.dumps(output_data, default=convert_to_dict, indent=4)

	with open('output_data.txt', 'w') as outfile:
		json.dump(output_data, outfile, default=convert_to_dict, indent=4)

	plt.show()
		