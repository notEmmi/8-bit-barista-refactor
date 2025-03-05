import pygame
import os

class Toolbox:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TOOLS_PATH = os.path.join(self.BASE_DIR, "assets", "images", "tools")
        
        self.tools = {
            "hoe": pygame.image.load(os.path.join(self.TOOLS_PATH, "hoe.png")),
            "mallet": pygame.image.load(os.path.join(self.TOOLS_PATH, "mallet.png")),
            "seedpouch": pygame.image.load(os.path.join(self.TOOLS_PATH, "seedpouch.png")),
            "watercan": pygame.image.load(os.path.join(self.TOOLS_PATH, "watercan.png")),
            "axe": pygame.image.load(os.path.join(self.TOOLS_PATH, "axe.png"))
        }
        self.selected_tool = 0  # Index of the selected tool
        
        # Colors for the brown theme
        self.background_color = (139, 69, 19)  # Medium brown for background
        self.slot_color = (101, 67, 33)  # Dark brown for slots
        self.highlight_color = (255, 248, 220)  # Cream-white for selection highlight
        
        # Layout configuration
        self.rows = 1  # Change to 1 row
        self.cols = 5  # Adjust the number of columns to fit all tools
        self.slot_width = 50
        self.slot_height = 50  # Make the height equal to the width to form a square
        self.slot_margin = 10
        self.corner_radius = 10  # For rounded corners

    def select_tool(self, index):
        if 0 <= index < len(self.tools):
            self.selected_tool = index  # Change selected tool
    
    def use_tool(self):
        if self.selected_tool == 0:
            
            print("Using hoe")
        elif self.selected_tool == 1:
            print("Using mallet")
        elif self.selected_tool == 2:
            print("Using seedpouch")
        elif self.selected_tool == 3:
            print("Using watercan")
        



    def draw(self, surface):
        screen_width, screen_height = surface.get_size()
        
        # Calculate toolbox dimensions
        box_width = (self.slot_width + self.slot_margin) * self.cols + self.slot_margin
        box_height = (self.slot_height + self.slot_margin) * self.rows + self.slot_margin
        
        # Center the toolbox at the bottom of the screen
        box_x = (screen_width - box_width) // 2
        box_y = screen_height - box_height - 20  # 20px padding from bottom
        
        # Draw the background
        pygame.draw.rect(surface, self.background_color, 
                        (box_x, box_y, box_width, box_height), 
                        border_radius=self.corner_radius)
        
        # Draw the tool slots
        tool_list = list(self.tools.items())
        for i in range(min(self.rows * self.cols, len(tool_list))):
            row = i // self.cols
            col = i % self.cols
            
            # Calculate slot position
            slot_x = box_x + self.slot_margin + col * (self.slot_width + self.slot_margin)
            slot_y = box_y + self.slot_margin + row * (self.slot_height + self.slot_margin)
            
            # Draw slot background
            pygame.draw.rect(surface, self.slot_color, 
                            (slot_x, slot_y, self.slot_width, self.slot_height),
                            border_radius=self.corner_radius)
            
            # Highlight selected tool
            if i == self.selected_tool:
                pygame.draw.rect(surface, self.highlight_color, 
                                (slot_x - 2, slot_y - 2, self.slot_width + 4, self.slot_height + 4), 
                                width=3, border_radius=self.corner_radius)
            
            # Draw the tool icon
            if i < len(tool_list):
                tool_name, tool_image = tool_list[i]
                # Scale the image to fit in the slot with some padding
                scaled_image = pygame.transform.scale(tool_image, (self.slot_width - 20, self.slot_height - 20))
                surface.blit(scaled_image, (slot_x + 10, slot_y + 10))
