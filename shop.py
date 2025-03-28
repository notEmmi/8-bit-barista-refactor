import pygame
import pygame_gui
import first_page

class ShopUI:
    def __init__(self, game_instance):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.SHOP_WIDTH = self.WIDTH // 4
        self.INVENTORY_WIDTH = self.WIDTH - self.SHOP_WIDTH

        # Colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 100, 75)
        self.DARK_BROWN = (100, 50, 25)
        self.BLACK = (0, 0, 0)
        self.GOLD = (255, 215, 0)
        self.game = game_instance

        # Screen and UI setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Shop & Inventory UI")
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))

        # Panels
        self.shop_icon = pygame.Rect(10, self.HEIGHT - 60, 50, 50)
        self.shop_panel = pygame.Rect(self.INVENTORY_WIDTH, 0, self.SHOP_WIDTH, self.HEIGHT)
        self.inventory_panel = pygame.Rect(0, 0, self.INVENTORY_WIDTH, self.HEIGHT)

        # Buttons
        self.back_button = pygame_gui.elements.UIButton(pygame.Rect(10, 10, 80, 40), "Back", self.manager)
        self.return_button = pygame_gui.elements.UIButton(pygame.Rect(350, 10, 150, 40), "Return to Game", self.manager)
        self.crops_tab = pygame_gui.elements.UIButton(pygame.Rect(120, 10, 100, 40), "Crops", self.manager)
        self.upgrades_tab = pygame_gui.elements.UIButton(pygame.Rect(220, 10, 100, 40), "Upgrades", self.manager)
        self.buy_button = pygame_gui.elements.UIButton(pygame.Rect(self.WIDTH - 100, self.HEIGHT - 80, 80, 40), "Buy", self.manager)
        self.sell_button = pygame_gui.elements.UIButton(pygame.Rect(self.WIDTH - 200, self.HEIGHT - 80, 80, 40), "Sell", self.manager)
        self.add_button = pygame_gui.elements.UIButton(pygame.Rect(self.WIDTH - 300, self.HEIGHT - 80, 40, 40), "+", self.manager)
        self.subtract_button = pygame_gui.elements.UIButton(pygame.Rect(self.WIDTH - 350, self.HEIGHT - 80, 40, 40), "-", self.manager)
        self.remove_button = pygame_gui.elements.UIButton(pygame.Rect(self.WIDTH - 400, self.HEIGHT - 80, 40, 40), "X", self.manager)

        # Gold and Inventory
        self.gold = 1000
        self.gold_text = pygame_gui.elements.UILabel(pygame.Rect(self.INVENTORY_WIDTH - 100, 10, 90, 30), f"{self.gold} 💰", self.manager)
        self.inventory = {}

        # Shop Items
        self.shop_items_crops = [
            {"name": "Carrot", "price": 5, "rect": pygame.Rect(120, 100, 100, 40)},
            {"name": "Corn", "price": 10, "rect": pygame.Rect(250, 100, 100, 40)}
        ]
        self.shop_items_upgrades = [
            {"name": "House Upgrade", "price": 100, "rect": pygame.Rect(120, 100, 150, 40)},
            {"name": "Inventory Upgrade", "price": 25, "rect": pygame.Rect(300, 100, 150, 40)}
        ]
        self.current_shop_items = self.shop_items_crops

        self.cart = None
        self.cart_quantity = 1
        self.shop_open = False
        self.clock = pygame.time.Clock()

        self.toggle_buttons_visibility(True)

    def toggle_buttons_visibility(self, show):
        self.sell_button.visible = show
        self.add_button.visible = show
        self.subtract_button.visible = show

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.screen.fill(self.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.shop_open:
                    if self.shop_icon.collidepoint(event.pos):
                        self.shop_open = True
                elif event.type == pygame.MOUSEBUTTONDOWN and self.shop_open:
                    if self.return_button.rect.collidepoint(event.pos):
                        running = False
                        self.game.run()
                    for item in self.current_shop_items:
                        if item["rect"].collidepoint(event.pos):
                            self.cart = item
                            self.cart_quantity = 1
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_button:
                        self.shop_open = False
                    elif event.ui_element == self.add_button and self.cart:
                        if self.cart not in self.shop_items_upgrades:
                            self.cart_quantity += 1
                    elif event.ui_element == self.subtract_button and self.cart and self.cart_quantity > 1:
                        if self.cart not in self.shop_items_upgrades:
                            self.cart_quantity -= 1
                    elif event.ui_element == self.remove_button:
                        self.cart = None
                        self.cart_quantity = 1
                    elif event.ui_element == self.buy_button and self.cart:
                        total_cost = self.cart["price"] * self.cart_quantity
                        if self.gold >= total_cost:
                            self.gold -= total_cost
                            self.inventory[self.cart["name"]] = self.inventory.get(self.cart["name"], 0) + self.cart_quantity
                            self.gold_text.set_text(f"{self.gold} 💰")
                            if self.cart in self.shop_items_upgrades:
                                self.cart["price"] = 0
                                self.shop_items_upgrades.remove(self.cart)
                            self.cart = None
                            self.cart_quantity = 1
                    elif event.ui_element == self.sell_button and self.cart:
                        if self.inventory.get(self.cart["name"], 0) >= self.cart_quantity:
                            self.gold += self.cart["price"] * self.cart_quantity
                            self.inventory[self.cart["name"]] -= self.cart_quantity
                            if self.inventory[self.cart["name"]] == 0:
                                del self.inventory[self.cart["name"]]
                            self.gold_text.set_text(f"{self.gold} 💰")
                            self.cart = None
                            self.cart_quantity = 1
                    elif event.ui_element == self.crops_tab:
                        self.current_shop_items = self.shop_items_crops
                        self.toggle_buttons_visibility(True)
                    elif event.ui_element == self.upgrades_tab:
                        self.current_shop_items = self.shop_items_upgrades
                        self.toggle_buttons_visibility(False)

                self.manager.process_events(event)

            if self.shop_open:
                pygame.draw.rect(self.screen, self.GRAY, self.inventory_panel)
                pygame.draw.rect(self.screen, self.DARK_BROWN, self.shop_panel)
                for item in self.current_shop_items:
                    pygame.draw.rect(self.screen, self.GOLD if item == self.cart else self.WHITE, item["rect"])
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(f"{item['name']} - {item['price']}💰", True, self.BLACK)
                    self.screen.blit(text_surface, (item["rect"].x + 5, item["rect"].y + 10))

                if self.cart:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(f"{self.cart['name']} x{self.cart_quantity}", True, self.BLACK)
                    self.screen.blit(text_surface, (self.INVENTORY_WIDTH + 10, 150))
                    total_cost = self.cart["price"] * self.cart_quantity
                    total_text = font.render(f"Total: {total_cost} 💰", True, self.BLACK)
                    self.screen.blit(total_text, (self.WIDTH - 200, self.HEIGHT - 120))

                self.manager.update(time_delta)
                self.manager.draw_ui(self.screen)
            else:
                pygame.draw.rect(self.screen, self.BLACK, self.shop_icon)
                pygame.draw.line(self.screen, self.WHITE, self.shop_icon.topleft, self.shop_icon.bottomright, 3)
                pygame.draw.line(self.screen, self.WHITE, self.shop_icon.topright, self.shop_icon.bottomleft, 3)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    shop = ShopUI()
    shop.run()
