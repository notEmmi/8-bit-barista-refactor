import pygame
import os

class Inventory:
    def __init__(self):
        self.slots = {}
        self.selected_tool = 0
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TOOLS_PATH = os.path.join(self.BASE_DIR, "assets", "images", "tools")

        # Player Inventory
        self.toolbar = {
            "hoe": pygame.image.load(os.path.join(self.TOOLS_PATH, "hoe.png")),
            "mallet": pygame.image.load(os.path.join(self.TOOLS_PATH, "mallet.png")),
            "seedpouch": pygame.image.load(os.path.join(self.TOOLS_PATH, "seedpouch.png")),
            "watercan": pygame.image.load(os.path.join(self.TOOLS_PATH, "watercan.png")),
            "axe": pygame.image.load(os.path.join(self.TOOLS_PATH, "axe.png"))
        }

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

    def draw_toolbox(self, surface):
        font = pygame.font.Font(None, 30)
        box_x, box_y = 20, 500  # Position of toolbox
        box_width, box_height = 300, 50  # Size of toolbox bar

        pygame.draw.rect(surface, (50, 50, 50), (box_x, box_y, box_width, box_height))  # Background
        pygame.draw.rect(surface, (200, 200, 200), (box_x, box_y, box_width, box_height), 2)  # Border

        for i, (tool_name, tool_image) in enumerate(self.toolbar.items()):
            if i == self.selected_tool:
                pygame.draw.rect(surface, (255, 255, 0), (box_x + i * 60, box_y, 50, 50), 2)  # Highlight selected tool
            surface.blit(tool_image, (box_x + 10 + i * 60, box_y + 10))

    def draw_inventory(self, surface):
        font = pygame.font.Font(None, 30)
        x, y = 20, 20  # Inventory position

        pygame.draw.rect(surface, (50, 50, 50), (x - 10, y - 10, 200, 200))  # Inventory Box
        pygame.draw.rect(surface, (200, 200, 200), (x - 10, y - 10, 200, 200), 2)  # Border

        for i, (item, count) in enumerate(self.slots.items()):
            text = font.render(f"{item}: {count}", True, (255, 255, 255))
            surface.blit(text, (x, y + i * 30))