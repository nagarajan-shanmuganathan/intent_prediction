import enum
from cell_entry import CellEntry

class Cell:

	def __init__(self, cell_entry):
		self.cell_entry = CellEntry[cell_entry]
