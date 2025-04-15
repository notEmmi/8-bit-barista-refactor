import pygame
import first_page

class ShopUI:
    def __init__(self, game_instance=None):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.SHOP_WIDTH = self.WIDTH // 4
        self.INVENTORY_WIDTH = self.WIDTH - self.SHOP_WIDTH

        # Colors - Enhanced for better contrast
        self.WHITE = (255, 255, 255)
        self.CREAM = (255, 248, 220)       # Lighter text color for better readability
        self.LIGHT_BROWN = (201, 121, 77)  # Brighter light brown for buttons
        self.MID_BROWN = (145, 80, 53)     # Mid brown for panel backgrounds
        self.DARK_BROWN = (89, 40, 20)     # Darker brown for borders and contrast
        self.BLACK = (0, 0, 0)
        self.GOLD = (255, 215, 0)          # Bright gold
        self.LIGHT_GOLD = (255, 236, 139)  # Light gold for highlights
        self.TEXT_COLOR = (255, 248, 220)  # Cream text for better readability
        self.HIGHLIGHT = (230, 150, 100)   # Highlight color for selected items
        self.game = game_instance

        # Screen setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Shop & Inventory UI")
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)  # Larger font for titles

        # Panels - Adjusted to make the overlay square bigger
        self.shop_icon = pygame.Rect(10, self.HEIGHT - 60, 50, 50)
        self.shop_panel = pygame.Rect(50, 30, 700, 500)  # Bigger shop panel
        self.inventory_panel = pygame.Rect(0, 0, self.INVENTORY_WIDTH, self.HEIGHT)

        # Buttons as Rects - Repositioned to match Figma
        self.return_button = pygame.Rect(120, 60, 80, 30)
        self.crops_tab = pygame.Rect(120, 60, 80, 30)
        self.upgrades_tab = pygame.Rect(210, 60, 80, 30)
        self.buy_button = pygame.Rect(600, 470, 100, 40)  # Larger, more visible buttons
        self.sell_button = pygame.Rect(490, 470, 100, 40)
        
        # Back arrow button to return to the game - Made larger and more visible
        self.back_arrow = pygame.Rect(60, 40, 50, 50)

        # Gold and Inventory
        self.gold = 1000
        self.inventory = {}

        # Shop Items - Arranged in a grid pattern with more spacing
        self.shop_items_crops = [
            {"name": "Sugar", "price": 3, "rect": pygame.Rect(120, 120, 100, 100)},
            {"name": "Coffee", "price": 15, "rect": pygame.Rect(230, 120, 100, 100)},
            {"name": "Tea", "price": 10, "rect": pygame.Rect(340, 120, 100, 100)},
            {"name": "Milk", "price": 5, "rect": pygame.Rect(120, 230, 100, 100)},
            {"name": "Honey", "price": 20, "rect": pygame.Rect(230, 230, 100, 100)},
            {"name": "Cocoa", "price": 12, "rect": pygame.Rect(340, 230, 100, 100)},
        ]
        
        self.shop_items_upgrades = []  # No upgrades for now
        
        self.current_shop_items = self.shop_items_crops

        self.cart = None
        self.cart_quantity = 1
        self.shop_open = False
        self.clock = pygame.time.Clock()

        self.show_sell_add_subtract = True
        
        # Load coin icon - Create a better coin icon
        self.coin_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.coin_icon, self.GOLD, (10, 10), 10)
        pygame.draw.circle(self.coin_icon, self.DARK_BROWN, (10, 10), 10, 1)  # Border

    def update_gold_display(self):
        # Draw gold in the top right corner with coin icon - Enhanced with shadow effect
        gold_bg = pygame.Rect(self.shop_panel.right - 120, self.shop_panel.top + 10, 100, 40)
        
        # Draw shadow
        shadow_rect = gold_bg.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(self.screen, self.DARK_BROWN, shadow_rect, border_radius=10)
        
        # Draw gold background
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, gold_bg, border_radius=10)
        pygame.draw.rect(self.screen, self.DARK_BROWN, gold_bg, 2, border_radius=10)  # Border
        
        gold_surface = self.font.render(f"{self.gold}", True, self.GOLD)
        self.screen.blit(gold_surface, (gold_bg.x + 15, gold_bg.y + 10))
        self.screen.blit(self.coin_icon, (gold_bg.right - 30, gold_bg.y + 10))

    def toggle_buttons_visibility(self, show):
        self.show_sell_add_subtract = show

    def draw_button(self, rect, text, selected=False, disabled=False, icon=None):
        # Draw rounded rectangle button with shadow effect
        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(self.screen, self.DARK_BROWN, shadow_rect, border_radius=10)
        
        # Button color based on state
        if disabled:
            color = (self.DARK_BROWN[0]//2, self.DARK_BROWN[1]//2, self.DARK_BROWN[2]//2)
        elif selected:
            color = self.HIGHLIGHT
        else:
            color = self.LIGHT_BROWN
            
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, self.DARK_BROWN, rect, 2, border_radius=10)  # Border
        
        # Draw text with slight shadow for depth
        shadow_label = self.font.render(text, True, self.BLACK)
        shadow_rect = shadow_label.get_rect(center=(rect.centerx + 1, rect.centery + 1))
        self.screen.blit(shadow_label, shadow_rect)
        
        label = self.font.render(text, True, self.CREAM)
        text_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, text_rect)
        
        # Draw icon if provided
        if icon:
            self.screen.blit(icon, (rect.x + 5, rect.centery - 8))

    def draw_item(self, item, selected=False):
        # Draw item slot with rounded corners and shadow effect
        shadow_rect = item["rect"].copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, self.DARK_BROWN, shadow_rect, border_radius=15)
        
        # Item background color
        color = self.HIGHLIGHT if selected else self.LIGHT_BROWN
        pygame.draw.rect(self.screen, color, item["rect"], border_radius=15)
        pygame.draw.rect(self.screen, self.DARK_BROWN, item["rect"], 2, border_radius=15)  # Border
        
        # Draw item name with shadow for depth
        name_shadow = self.font.render(f"{item['name']}", True, self.BLACK)
        name_shadow_rect = name_shadow.get_rect(center=(item["rect"].centerx + 1, item["rect"].centery - 15 + 1))
        self.screen.blit(name_shadow, name_shadow_rect)
        
        name_label = self.font.render(f"{item['name']}", True, self.CREAM)
        name_rect = name_label.get_rect(center=(item["rect"].centerx, item["rect"].centery - 15))
        self.screen.blit(name_label, name_rect)
        
        # Draw price with gold coin icon
        price_bg = pygame.Rect(item["rect"].centerx - 30, item["rect"].centery + 10, 60, 25)
        pygame.draw.rect(self.screen, self.DARK_BROWN, price_bg, border_radius=8)
        
        price_label = self.font.render(f"{item['price']}", True, self.GOLD)
        price_rect = price_label.get_rect(center=(price_bg.centerx - 10, price_bg.centery))
        self.screen.blit(price_label, price_rect)
        
        # Small coin icon
        small_coin = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(small_coin, self.GOLD, (7, 7), 7)
        pygame.draw.circle(small_coin, self.DARK_BROWN, (7, 7), 7, 1)
        self.screen.blit(small_coin, (price_bg.right - 20, price_bg.y + 5))

    def draw_back_arrow(self):
        # Draw a more visible back arrow with shadow and highlight
        shadow_rect = self.back_arrow.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(self.screen, self.DARK_BROWN, shadow_rect, border_radius=10)
        
        # Arrow button background
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.back_arrow, border_radius=10)
        pygame.draw.rect(self.screen, self.DARK_BROWN, self.back_arrow, 2, border_radius=10)
        
        # Draw the arrow shape
        arrow_points = [
            (self.back_arrow.x + 35, self.back_arrow.y + 10),
            (self.back_arrow.x + 15, self.back_arrow.y + 25),
            (self.back_arrow.x + 35, self.back_arrow.y + 40)
        ]
        
        # Arrow shadow
        shadow_points = [(p[0]+1, p[1]+1) for p in arrow_points]
        pygame.draw.polygon(self.screen, self.DARK_BROWN, shadow_points)
        
        # Arrow
        pygame.draw.polygon(self.screen, self.CREAM, arrow_points)
        
        # Add "Back" text
        back_text = self.font.render("Back", True, self.CREAM)
        self.screen.blit(back_text, (self.back_arrow.x + 5, self.back_arrow.y - 20))

    def run(self):
        running = True
        self.shop_open = True  # Ensure the shop opens immediately

        while running:
            time_delta = self.clock.tick(60) / 1000.0
            
            # Fill background with a gradient effect
            self.screen.fill(self.DARK_BROWN)
            
            # Draw a subtle pattern in the background
            for x in range(0, self.WIDTH, 20):
                for y in range(0, self.HEIGHT, 20):
                    pygame.draw.rect(self.screen, (self.DARK_BROWN[0]-10, self.DARK_BROWN[1]-5, self.DARK_BROWN[2]-5), 
                                    (x, y, 10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if self.shop_open:
                        # Back arrow to return to the game
                        if self.back_arrow.collidepoint(mouse_pos):
                            running = False
                            if self.game:
                                self.game.run()
                        elif self.crops_tab.collidepoint(mouse_pos):
                            # Switch to crops tab
                            self.current_shop_items = self.shop_items_crops
                            self.toggle_buttons_visibility(True)
                        elif self.upgrades_tab.collidepoint(mouse_pos):
                            # Switch to upgrades tab
                            self.current_shop_items = self.shop_items_upgrades
                            self.toggle_buttons_visibility(False)
                        elif hasattr(self, 'add_button') and self.add_button.collidepoint(mouse_pos) and self.cart:
                            if self.cart not in self.shop_items_upgrades:
                                self.cart_quantity += 1
                        elif hasattr(self, 'subtract_button') and self.subtract_button.collidepoint(mouse_pos) and self.cart and self.cart_quantity > 1:
                            if self.cart not in self.shop_items_upgrades:
                                self.cart_quantity -= 1
                        elif hasattr(self, 'remove_button') and self.remove_button.collidepoint(mouse_pos):
                            self.cart = None
                            self.cart_quantity = 1
                        elif self.buy_button.collidepoint(mouse_pos) and self.cart:
                            total_cost = self.cart["price"] * self.cart_quantity
                            if self.gold >= total_cost:
                                self.gold -= total_cost
                                name = self.cart["name"]
                                self.inventory[name] = self.inventory.get(name, 0) + self.cart_quantity
                                if self.cart in self.shop_items_upgrades:
                                    self.cart["price"] = 0
                                    self.shop_items_upgrades.remove(self.cart)
                                self.cart = None
                                self.cart_quantity = 1
                        elif self.sell_button.collidepoint(mouse_pos) and self.cart:
                            name = self.cart["name"]
                            if self.inventory.get(name, 0) >= self.cart_quantity:
                                self.gold += self.cart["price"] * self.cart_quantity
                                self.inventory[name] -= self.cart_quantity
                                if self.inventory[name] == 0:
                                    del self.inventory[name]
                                self.cart = None
                                self.cart_quantity = 1
                        for item in self.current_shop_items:
                            if item["rect"].collidepoint(mouse_pos):
                                self.cart = item
                                self.cart_quantity = 1

            if self.shop_open:
                # Draw main shop panel with rounded corners and shadow
                shadow_panel = self.shop_panel.copy()
                shadow_panel.x += 5
                shadow_panel.y += 5
                pygame.draw.rect(self.screen, (50, 25, 15), shadow_panel, border_radius=15)
                
                pygame.draw.rect(self.screen, self.MID_BROWN, self.shop_panel, border_radius=15)
                pygame.draw.rect(self.screen, self.DARK_BROWN, self.shop_panel, 3, border_radius=15)  # Border
                
                # Draw shop title
                title = self.title_font.render("SHOP", True, self.CREAM)
                title_shadow = self.title_font.render("SHOP", True, self.BLACK)
                self.screen.blit(title_shadow, (self.shop_panel.centerx - title.get_width()//2 + 2, 
                                              self.shop_panel.top + 15 + 2))
                self.screen.blit(title, (self.shop_panel.centerx - title.get_width()//2, 
                                       self.shop_panel.top + 15))
                
                # Draw back arrow button - more visible now
                self.draw_back_arrow()
                
                # Draw right panel for cart details with shadow
                cart_panel = pygame.Rect(self.shop_panel.right - 180, self.shop_panel.top + 70, 160, 350)
                shadow_cart = cart_panel.copy()
                shadow_cart.x += 3
                shadow_cart.y += 3
                pygame.draw.rect(self.screen, (50, 25, 15), shadow_cart, border_radius=15)
                
                pygame.draw.rect(self.screen, self.MID_BROWN, cart_panel, border_radius=15)
                pygame.draw.rect(self.screen, self.DARK_BROWN, cart_panel, 2, border_radius=15)  # Border
                
                # Draw cart title
                cart_title = self.font.render("CART", True, self.CREAM)
                cart_title_shadow = self.font.render("CART", True, self.BLACK)
                self.screen.blit(cart_title_shadow, (cart_panel.centerx - cart_title.get_width()//2 + 1, 
                                                   cart_panel.top + 15 + 1))
                self.screen.blit(cart_title, (cart_panel.centerx - cart_title.get_width()//2, 
                                            cart_panel.top + 15))
                
                # Draw tabs with better contrast
                tab_bg = pygame.Rect(120, 60, 170, 30)
                pygame.draw.rect(self.screen, self.DARK_BROWN, tab_bg, border_radius=10)
                
                self.draw_button(self.crops_tab, "Crops", selected=self.current_shop_items==self.shop_items_crops)
                self.draw_button(self.upgrades_tab, "Upgrades", selected=self.current_shop_items==self.shop_items_upgrades)
                
                # Draw action buttons with icons
                plus_icon = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.line(plus_icon, self.CREAM, (8, 3), (8, 13), 2)
                pygame.draw.line(plus_icon, self.CREAM, (3, 8), (13, 8), 2)
                
                minus_icon = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.line(minus_icon, self.CREAM, (3, 8), (13, 8), 2)
                
                x_icon = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.line(x_icon, self.CREAM, (4, 4), (12, 12), 2)
                pygame.draw.line(x_icon, self.CREAM, (4, 12), (12, 4), 2)
                
                self.draw_button(self.buy_button, "Buy", disabled=not self.cart)
                if self.show_sell_add_subtract:
                    self.draw_button(self.sell_button, "Sell", disabled=not self.cart)
                # Draw items grid
                for item in self.current_shop_items:
                    self.draw_item(item, selected=item==self.cart)

                # Draw cart details with better formatting
                if self.cart:
                    # Draw selected item title
                    selected_title = self.font.render("Selected Item:", True, self.CREAM)
                    selected_shadow = self.font.render("Selected Item:", True, self.BLACK)
                    self.screen.blit(selected_shadow, (cart_panel.x + 11, cart_panel.y + 51))
                    self.screen.blit(selected_title, (cart_panel.x + 10, cart_panel.y + 50))
                    
                    # Draw item name in a box
                    name_bg = pygame.Rect(cart_panel.x + 10, cart_panel.y + 75, 140, 30)
                    pygame.draw.rect(self.screen, self.LIGHT_BROWN, name_bg, border_radius=8)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, name_bg, 1, border_radius=8)
                    
                    cart_name = self.font.render(f"{self.cart['name']}", True, self.CREAM)
                    name_rect = cart_name.get_rect(center=name_bg.center)
                    self.screen.blit(cart_name, name_rect)
                    
                    y_offset = 120
                    
                    if self.show_sell_add_subtract:
                        # Quantity with +/- controls
                        quantity_label = self.font.render("Quantity:", True, self.CREAM)
                        self.screen.blit(quantity_label, (cart_panel.x + 10, cart_panel.y + y_offset))
                        
                        # Create the +/- buttons dynamically inside the cart panel
                        self.subtract_button = pygame.Rect(cart_panel.x + 80, cart_panel.y + y_offset, 25, 25)
                        self.add_button = pygame.Rect(cart_panel.x + 125, cart_panel.y + y_offset, 25, 25)
                        
                        # Draw the +/- buttons
                        pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.subtract_button, border_radius=5)
                        pygame.draw.rect(self.screen, self.DARK_BROWN, self.subtract_button, 2, border_radius=5)
                        pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.add_button, border_radius=5)
                        pygame.draw.rect(self.screen, self.DARK_BROWN, self.add_button, 2, border_radius=5)
                        
                        # Draw the + and - symbols
                        minus_text = self.font.render("-", True, self.CREAM)
                        plus_text = self.font.render("+", True, self.CREAM)
                        minus_rect = minus_text.get_rect(center=self.subtract_button.center)
                        plus_rect = plus_text.get_rect(center=self.add_button.center)
                        self.screen.blit(minus_text, minus_rect)
                        self.screen.blit(plus_text, plus_rect)
                        
                        # Draw quantity between the buttons
                        qty_text = self.font.render(f"{self.cart_quantity}", True, self.CREAM)
                        qty_rect = qty_text.get_rect(center=(cart_panel.x + 105, cart_panel.y + y_offset + 12))
                        self.screen.blit(qty_text, qty_rect)
                        
                        y_offset += 35
                    
                    # Price display
                    price_label = self.font.render("Price:", True, self.CREAM)
                    self.screen.blit(price_label, (cart_panel.x + 10, cart_panel.y + y_offset))
                    
                    price_bg = pygame.Rect(cart_panel.x + 90, cart_panel.y + y_offset, 60, 25)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, price_bg, border_radius=8)
                    
                    price_text = self.font.render(f"{self.cart['price']}", True, self.GOLD)
                    price_rect = price_text.get_rect(center=price_bg.center)
                    self.screen.blit(price_text, price_rect)
                    
                    y_offset += 35
                    
                    # Show inventory count for the selected item
                    inventory_count = self.inventory.get(self.cart["name"], 0)
                    inventory_label = self.font.render("In Stock:", True, self.CREAM)
                    self.screen.blit(inventory_label, (cart_panel.x + 10, cart_panel.y + y_offset))
                    
                    inv_bg = pygame.Rect(cart_panel.x + 90, cart_panel.y + y_offset, 60, 25)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, inv_bg, border_radius=8)
                    
                    inv_text = self.font.render(f"{inventory_count}", True, self.CREAM)
                    inv_rect = inv_text.get_rect(center=inv_bg.center)
                    self.screen.blit(inv_text, inv_rect)
                    
                    y_offset += 35
                    
                    if self.show_sell_add_subtract:
                        # Total cost
                        total = self.cart["price"] * self.cart_quantity
                        total_label = self.font.render("Total:", True, self.CREAM)
                        self.screen.blit(total_label, (cart_panel.x + 10, cart_panel.y + y_offset))
                        
                        total_bg = pygame.Rect(cart_panel.x + 90, cart_panel.y + y_offset, 60, 25)
                        pygame.draw.rect(self.screen, self.DARK_BROWN, total_bg, border_radius=8)
                        
                        total_text = self.font.render(f"{total}", True, self.GOLD)
                        total_rect = total_text.get_rect(center=total_bg.center)
                        self.screen.blit(total_text, total_rect)
                        
                        y_offset += 35
                    
                    # Add a remove button inside the cart panel
                    self.remove_button = pygame.Rect(cart_panel.centerx - 20, cart_panel.y + y_offset, 40, 25)
                    pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.remove_button, border_radius=5)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, self.remove_button, 2, border_radius=5)
                    remove_text = self.font.render("X", True, self.CREAM)
                    remove_rect = remove_text.get_rect(center=self.remove_button.center)
                    self.screen.blit(remove_text, remove_rect)
                
                # Draw gold counter
                self.update_gold_display()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    shop = ShopUI()
    shop.run()