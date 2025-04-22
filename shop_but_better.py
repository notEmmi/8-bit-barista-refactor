import pygame

class ShopUI:
    def __init__(self):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.SHOP_WIDTH = self.WIDTH // 3
        self.INVENTORY_WIDTH = self.WIDTH - self.SHOP_WIDTH

        # Colors
        self.WHITE = (255, 255, 255)
        self.LIGHT_BROWN = (210, 180, 140)
        self.BROWN = (150, 100, 75)
        self.DARK_BROWN = (100, 50, 25)
        self.BLACK = (0, 0, 0)
        self.GOLD = (255, 215, 0)
        self.LIGHT_GOLD = (255, 235, 120)
        self.GREEN = (50, 150, 50)
        self.RED = (200, 50, 50)
        self.BLUE = (70, 130, 180)

        # Screen setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Farm Shop & Inventory")
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 16)

        # Panels
        self.shop_icon = pygame.Rect(10, self.HEIGHT - 60, 50, 50)
        self.shop_panel = pygame.Rect(self.INVENTORY_WIDTH, 0, self.SHOP_WIDTH, self.HEIGHT)
        self.inventory_panel = pygame.Rect(0, 0, self.INVENTORY_WIDTH, self.HEIGHT)
        self.preview_panel = pygame.Rect(20, 200, self.INVENTORY_WIDTH - 40, 250)

        # Buttons as Rects
        self.back_button = pygame.Rect(20, 20, 100, 40)
        self.close_button = pygame.Rect(self.INVENTORY_WIDTH - 120, 20, 100, 40)
        self.crops_tab = pygame.Rect(140, 20, 100, 40)
        self.upgrades_tab = pygame.Rect(250, 20, 100, 40)
        self.buy_button = pygame.Rect(self.WIDTH - 120, self.HEIGHT - 80, 100, 40)
        self.sell_button = pygame.Rect(self.WIDTH - 230, self.HEIGHT - 80, 100, 40)
        self.add_button = pygame.Rect(self.WIDTH - 300, self.HEIGHT - 80, 40, 40)
        self.subtract_button = pygame.Rect(self.WIDTH - 350, self.HEIGHT - 80, 40, 40)
        self.remove_button = pygame.Rect(self.WIDTH - 400, self.HEIGHT - 80, 40, 40)

        # Gold and Inventory
        self.gold = 1000
        self.inventory = {}

        # Shop Items with descriptions and images
        self.shop_items_crops = [
            {
                "name": "Carrot", 
                "price": 5, 
                "rect": pygame.Rect(140, 100, 180, 50),
                "description": "A nutritious orange root vegetable. Grows in 3 days.",
                "image": self.create_placeholder_image((100, 100), (255, 140, 0), "Carrot")
            },
            {
                "name": "Corn", 
                "price": 10, 
                "rect": pygame.Rect(140, 160, 180, 50),
                "description": "Sweet yellow corn. Grows in 5 days and yields multiple harvests.",
                "image": self.create_placeholder_image((100, 100), (255, 255, 0), "Corn")
            },
            {
                "name": "Tomato", 
                "price": 15, 
                "rect": pygame.Rect(140, 220, 180, 50),
                "description": "Juicy red tomatoes. Grows in 7 days on a trellis.",
                "image": self.create_placeholder_image((100, 100), (255, 0, 0), "Tomato")
            }
        ]
        
        self.shop_items_upgrades = [
            {
                "name": "House Upgrade", 
                "price": 100, 
                "rect": pygame.Rect(140, 100, 180, 50),
                "description": "Upgrade your farmhouse to unlock new features and storage.",
                "image": self.create_placeholder_image((100, 100), (150, 75, 0), "House")
            },
            {
                "name": "Inventory Upgrade", 
                "price": 25, 
                "rect": pygame.Rect(140, 160, 180, 50),
                "description": "Increase your inventory capacity by 10 slots.",
                "image": self.create_placeholder_image((100, 100), (139, 69, 19), "Backpack")
            },
            {
                "name": "Watering Can", 
                "price": 50, 
                "rect": pygame.Rect(140, 220, 180, 50),
                "description": "Water multiple crops at once and reduce growing time.",
                "image": self.create_placeholder_image((100, 100), (0, 191, 255), "Can")
            }
        ]
        
        self.current_shop_items = self.shop_items_crops

        self.cart = None
        self.cart_quantity = 1
        self.shop_open = False
        self.clock = pygame.time.Clock()
        self.show_preview = False
        self.show_sell_add_subtract = True
        
        # Hover state
        self.hovered_item = None

    def create_placeholder_image(self, size, color, text):
        """Create a placeholder image with text"""
        surface = pygame.Surface(size)
        surface.fill(color)
        pygame.draw.rect(surface, self.BLACK, (0, 0, size[0], size[1]), 2)
        
        text_surface = self.small_font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(size[0]//2, size[1]//2))
        surface.blit(text_surface, text_rect)
        
        return surface

    def update_gold_display(self):
        gold_bg = pygame.Rect(self.INVENTORY_WIDTH - 150, 20, 120, 40)
        pygame.draw.rect(self.screen, self.LIGHT_GOLD, gold_bg, border_radius=10)
        pygame.draw.rect(self.screen, self.GOLD, gold_bg, 2, border_radius=10)
        
        gold_surface = self.font.render(f"{self.gold} 💰", True, self.BLACK)
        self.screen.blit(gold_surface, (self.INVENTORY_WIDTH - 130, 30))

    def toggle_buttons_visibility(self, show):
        self.show_sell_add_subtract = show

    def draw_button(self, rect, text, color=None, hover=False, disabled=False):
        if disabled:
            bg_color = self.BROWN
            text_color = self.BLACK
            border_color = self.DARK_BROWN
        elif hover:
            bg_color = self.LIGHT_BROWN
            text_color = self.BLACK
            border_color = self.GOLD
        else:
            bg_color = color if color else self.BROWN
            text_color = self.BLACK
            border_color = self.DARK_BROWN
            
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)
        
        label = self.font.render(text, True, text_color)
        text_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, text_rect)

    def draw_item_preview(self, item):
        if not item:
            return
            
        # Draw preview panel background
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.preview_panel, border_radius=10)
        pygame.draw.rect(self.screen, self.DARK_BROWN, self.preview_panel, 3, border_radius=10)
        
        # Draw item name
        title = self.title_font.render(item["name"], True, self.BLACK)
        self.screen.blit(title, (self.preview_panel.x + 20, self.preview_panel.y + 20))
        
        # Draw item price
        price = self.font.render(f"Price: {item['price']} 💰", True, self.BLACK)
        self.screen.blit(price, (self.preview_panel.x + 20, self.preview_panel.y + 60))
        
        # Draw item image
        self.screen.blit(item["image"], (self.preview_panel.x + 20, self.preview_panel.y + 100))
        
        # Draw item description
        description_lines = self.wrap_text(item["description"], self.font, self.preview_panel.width - 150)
        for i, line in enumerate(description_lines):
            desc_text = self.font.render(line, True, self.BLACK)
            self.screen.blit(desc_text, (self.preview_panel.x + 140, self.preview_panel.y + 100 + i * 25))

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a certain width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            width, _ = font.size(test_line)
            
            if width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines

    def draw_inventory(self):
        inventory_title = self.title_font.render("Inventory", True, self.BLACK)
        self.screen.blit(inventory_title, (30, 80))
        
        pygame.draw.line(self.screen, self.DARK_BROWN, (20, 110), (self.INVENTORY_WIDTH - 20, 110), 2)
        
        if not self.inventory:
            empty_text = self.font.render("Your inventory is empty.", True, self.BLACK)
            self.screen.blit(empty_text, (30, 130))
            return
            
        y_pos = 130
        for item_name, quantity in self.inventory.items():
            item_rect = pygame.Rect(30, y_pos, self.INVENTORY_WIDTH - 60, 40)
            
            # Check if this inventory item is selected in the cart
            is_selected = self.cart and self.cart["name"] == item_name
            
            pygame.draw.rect(self.screen, self.LIGHT_GOLD if is_selected else self.WHITE, 
                            item_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.DARK_BROWN, item_rect, 2, border_radius=5)
            
            item_text = self.font.render(f"{item_name} x{quantity}", True, self.BLACK)
            self.screen.blit(item_text, (40, y_pos + 10))
            
            y_pos += 50
            
            # Find the matching shop item for preview
            if is_selected:
                for item in self.shop_items_crops + self.shop_items_upgrades:
                    if item["name"] == item_name:
                        self.draw_item_preview(item)
                        break

    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()
            time_delta = self.clock.tick(60) / 1000.0

            # Check for hover states
            self.hovered_item = None
            for item in self.current_shop_items:
                if item["rect"].collidepoint(mouse_pos):
                    self.hovered_item = item
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.shop_open and self.shop_icon.collidepoint(mouse_pos):
                        self.shop_open = True
                    elif self.shop_open:
                        if self.close_button.collidepoint(mouse_pos):
                            self.shop_open = False
                        elif self.back_button.collidepoint(mouse_pos):
                            self.shop_open = False
                        elif self.crops_tab.collidepoint(mouse_pos):
                            self.current_shop_items = self.shop_items_crops
                            self.toggle_buttons_visibility(True)
                            self.cart = None
                        elif self.upgrades_tab.collidepoint(mouse_pos):
                            self.current_shop_items = self.shop_items_upgrades
                            self.toggle_buttons_visibility(False)
                            self.cart = None
                        elif self.add_button.collidepoint(mouse_pos) and self.cart and self.show_sell_add_subtract:
                            if self.cart not in self.shop_items_upgrades:
                                self.cart_quantity += 1
                        elif self.subtract_button.collidepoint(mouse_pos) and self.cart and self.cart_quantity > 1 and self.show_sell_add_subtract:
                            if self.cart not in self.shop_items_upgrades:
                                self.cart_quantity -= 1
                        elif self.remove_button.collidepoint(mouse_pos) and self.cart:
                            self.cart = None
                            self.cart_quantity = 1
                        elif self.buy_button.collidepoint(mouse_pos) and self.cart:
                            total_cost = self.cart["price"] * self.cart_quantity
                            if self.gold >= total_cost:
                                self.gold -= total_cost
                                name = self.cart["name"]
                                self.inventory[name] = self.inventory.get(name, 0) + self.cart_quantity
                                if self.cart in self.shop_items_upgrades:
                                    # Remove one-time purchases from shop
                                    if name in ["House Upgrade", "Inventory Upgrade"]:
                                        self.shop_items_upgrades.remove(self.cart)
                                self.cart = None
                                self.cart_quantity = 1
                        elif self.sell_button.collidepoint(mouse_pos) and self.cart and self.show_sell_add_subtract:
                            name = self.cart["name"]
                            if self.inventory.get(name, 0) >= self.cart_quantity:
                                self.gold += self.cart["price"] * self.cart_quantity
                                self.inventory[name] -= self.cart_quantity
                                if self.inventory[name] == 0:
                                    del self.inventory[name]
                                self.cart = None
                                self.cart_quantity = 1
                                
                        # Check inventory clicks
                        y_pos = 130
                        for item_name in self.inventory:
                            item_rect = pygame.Rect(30, y_pos, self.INVENTORY_WIDTH - 60, 40)
                            if item_rect.collidepoint(mouse_pos):
                                # Find the matching shop item
                                for item in self.shop_items_crops + self.shop_items_upgrades:
                                    if item["name"] == item_name:
                                        self.cart = item
                                        self.cart_quantity = 1
                                        break
                            y_pos += 50
                            
                        # Check shop item clicks
                        for item in self.current_shop_items:
                            if item["rect"].collidepoint(mouse_pos):
                                self.cart = item
                                self.cart_quantity = 1

            if self.shop_open:
                # Draw main panels
                pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.inventory_panel)
                pygame.draw.rect(self.screen, self.DARK_BROWN, self.shop_panel)
                
                # Draw navigation buttons
                self.draw_button(self.close_button, "Close Shop", self.RED, 
                                self.close_button.collidepoint(mouse_pos))
                self.draw_button(self.back_button, "Back", self.RED, 
                                self.back_button.collidepoint(mouse_pos))
                
                # Draw tabs
                is_crops_active = self.current_shop_items == self.shop_items_crops
                is_upgrades_active = self.current_shop_items == self.shop_items_upgrades
                
                self.draw_button(self.crops_tab, "Crops", 
                                self.GREEN if is_crops_active else self.BROWN,
                                self.crops_tab.collidepoint(mouse_pos) and not is_crops_active)
                                
                self.draw_button(self.upgrades_tab, "Upgrades", 
                                self.BLUE if is_upgrades_active else self.BROWN,
                                self.upgrades_tab.collidepoint(mouse_pos) and not is_upgrades_active)
                
                # Draw shop title
                shop_title = self.title_font.render("Shop", True, self.WHITE)
                self.screen.blit(shop_title, (self.INVENTORY_WIDTH + 20, 20))
                
                # Draw shop items
                for item in self.current_shop_items:
                    is_hovered = item == self.hovered_item
                    is_selected = item == self.cart
                    
                    pygame.draw.rect(self.screen, 
                                    self.GOLD if is_selected else (self.LIGHT_BROWN if is_hovered else self.WHITE), 
                                    item["rect"], border_radius=5)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, item["rect"], 2, border_radius=5)
                    
                    label = self.font.render(f"{item['name']} - {item['price']} 💰", True, self.BLACK)
                    self.screen.blit(label, (item["rect"].x + 10, item["rect"].y + 15))
                
                # Draw inventory
                self.draw_inventory()
                
                # Draw preview for hovered item
                if self.hovered_item and not self.cart:
                    self.draw_item_preview(self.hovered_item)
                
                # Draw cart info
                if self.cart:
                    # Draw action buttons
                    can_buy = self.gold >= (self.cart["price"] * self.cart_quantity)
                    can_sell = self.inventory.get(self.cart["name"], 0) >= self.cart_quantity
                    
                    self.draw_button(self.buy_button, "Buy", self.GREEN, 
                                    self.buy_button.collidepoint(mouse_pos) and can_buy,
                                    not can_buy)
                    
                    if self.show_sell_add_subtract:
                        self.draw_button(self.sell_button, "Sell", self.RED, 
                                        self.sell_button.collidepoint(mouse_pos) and can_sell,
                                        not can_sell)
                        self.draw_button(self.add_button, "+", None, 
                                        self.add_button.collidepoint(mouse_pos))
                        self.draw_button(self.subtract_button, "-", None, 
                                        self.subtract_button.collidepoint(mouse_pos) and self.cart_quantity > 1,
                                        self.cart_quantity <= 1)
                    
                    self.draw_button(self.remove_button, "X", self.RED, 
                                    self.remove_button.collidepoint(mouse_pos))
                    
                    # Draw cart summary
                    cart_bg = pygame.Rect(self.WIDTH - 250, self.HEIGHT - 150, 230, 60)
                    pygame.draw.rect(self.screen, self.LIGHT_BROWN, cart_bg, border_radius=5)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, cart_bg, 2, border_radius=5)
                    
                    cart_label = self.font.render(f"{self.cart['name']} x{self.cart_quantity}", True, self.BLACK)
                    self.screen.blit(cart_label, (self.WIDTH - 240, self.HEIGHT - 140))
                    
                    total = self.cart["price"] * self.cart_quantity
                    total_label = self.font.render(f"Total: {total} 💰", True, self.BLACK)
                    self.screen.blit(total_label, (self.WIDTH - 240, self.HEIGHT - 110))
                
                # Draw gold display
                self.update_gold_display()

            else:
                # Draw shop icon when shop is closed
                pygame.draw.rect(self.screen, self.BROWN, self.shop_icon, border_radius=10)
                pygame.draw.rect(self.screen, self.DARK_BROWN, self.shop_icon, 2, border_radius=10)
                
                shop_text = self.small_font.render("SHOP", True, self.WHITE)
                text_rect = shop_text.get_rect(center=self.shop_icon.center)
                self.screen.blit(shop_text, text_rect)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    shop = ShopUI()
    shop.run()