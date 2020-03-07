from intent import Intent

class Obstacle:
	
	def __init__(self, x, y, length, width, intent):
		self.x = x
		self.y = y
		self.length = length
		self.width = width
		self.intent = Intent(intent)
