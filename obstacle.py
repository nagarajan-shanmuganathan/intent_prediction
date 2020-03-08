from intent import Intent

class Obstacle:

	intent_violation = False
	
	def __init__(self, obstacle_number, x, y, length, width, intent):
		self.number = obstacle_number
		self.x = x
		self.y = y
		self.length = length
		self.width = width
		self.intent = Intent(intent)
