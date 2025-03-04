import pygame

class Inventory:
	def __init__(self):
		self.slots = {}

	def add_item(self, item):
		if item in self.slots:
			self.slots[item] += 1
		else:
			self.slots[item] = 1
	
	def remove_item(self, item):
		if item in self.slots:
			self.slots[item] -= 1
			if self.slots[item] == 0:
				del self.slots[item]
	
	def has_item(self, item):
		return item in self.slots
	
	def draw_inventory(self, surface):
		font = pygame.font.Font(None, 30)
		x, y = 20, 20  # Inventory position

		pygame.draw.rect(surface, (50, 50, 50), (x - 10, y - 10, 200, 200))  # Inventory Box
		pygame.draw.rect(surface, (200, 200, 200), (x - 10, y - 10, 200, 200), 2)  # Border

		for i, (item, count) in enumerate(self.slots.items()):
			text = font.render(f"{item}: {count}", True, (255, 255, 255))
			surface.blit(text, (x, y + i * 30))