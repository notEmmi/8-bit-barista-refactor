import pygame
import os

class Toolbox:
    def __init__(self):
        self.tools = ["hoe", "mallet", "seedpouch", "watercan", "axe"]  # List of tools
        self.selected_tool = 0  # Index of the selected tool

    def select_tool(self, index):
        if 0 <= index < len(self.tools):
            self.selected_tool = index  # Change selected tool

    def draw(self, surface):
        """Draw toolbox UI at the bottom of the screen."""
        font = pygame.font.Font(None, 30)
        box_x, box_y = 20, 500  # Position
        box_width, box_height = 300, 50  # Size

        pygame.draw.rect(surface, (50, 50, 50), (box_x, box_y, box_width, box_height))  # Background
        pygame.draw.rect(surface, (200, 200, 200), (box_x, box_y, box_width, box_height), 2)  # Border

        for i, tool in enumerate(self.tools):
            color = (255, 255, 0) if i == self.selected_tool else (255, 255, 255)  # Highlight selected tool
            text = font.render(tool, True, color)
            surface.blit(text, (box_x + 10 + i * 60, box_y + 10))
