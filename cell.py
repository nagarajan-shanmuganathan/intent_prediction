import enum
from cell_entry import CellEntry

class Cell:

	obstacle_number = -1
	is_obstacle = False
	
	def __init__(self, cell_entry):
		self.cell_entry = CellEntry[cell_entry]
