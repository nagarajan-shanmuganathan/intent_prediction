import enum

class CellEntry(enum.Enum):
	EMPTY = 0
	OBSTACLE = 1
	START = 2
	GOAL = 3
	LEFT = 4
	RIGHT = 5
	DOWN = 6
	UP = 7
	CURRENT = 8
	VISITED_OBSTACLE = 9
	RIGHT_UP = 10
	LEFT_UP = 11
	RIGHT_DOWN = 12
	LEFT_DOWN = 13
