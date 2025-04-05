import pygame
import first_page

class ShopUI:
    def __init__(self, game_instance=None):
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

        # Screen setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Shop & Inventory UI")
        self.font = pygame.font.Font(None, 24)

        # Panels
        self.shop_icon = pygame.Rect(10, self.HEIGHT - 60, 50, 50)
        self.shop_panel = pygame.Rect(self.INVENTORY_WIDTH, 0, self.SHOP_WIDTH, self.HEIGHT)
        self.inventory_panel = pygame.Rect(0, 0, self.INVENTORY_WIDTH, self.HEIGHT)

        # Buttons as Rects
        self.return_button = pygame.Rect(350, 10, 150, 40)
        self.crops_tab = pygame.Rect(120, 10, 100, 40)
        self.upgrades_tab = pygame.Rect(220, 10, 100, 40)
        self.buy_button = pygame.Rect(self.WIDTH - 100, self.HEIGHT - 80, 80, 40)
        self.sell_button = pygame.Rect(self.WIDTH - 200, self.HEIGHT - 80, 80, 40)
        self.add_button = pygame.Rect(self.WIDTH - 300, self.HEIGHT - 80, 40, 40)
        self.subtract_button = pygame.Rect(self.WIDTH - 350, self.HEIGHT - 80, 40, 40)
        self.remove_button = pygame.Rect(self.WIDTH - 400, self.HEIGHT - 80, 40, 40)

        # Gold and Inventory
        self.gold = 1000
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

        self.show_sell_add_subtract = True

    def update_gold_display(self):
        gold_surface = self.font.render(f"{self.gold} 💰", True, self.BLACK)
        self.screen.blit(gold_surface, (self.INVENTORY_WIDTH - 100, 10))

    def toggle_buttons_visibility(self, show):
        self.show_sell_add_subtract = show

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, self.GRAY, rect)
        label = self.font.render(text, True, self.BLACK)
        self.screen.blit(label, (rect.x + 5, rect.y + 10))

    def run(self):
        running = True
        self.shop_open = True  # Ensure the shop opens immediately

        while running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if self.shop_open:
                        if self.return_button.collidepoint(mouse_pos):
                            running = False
                            if self.game:
                                self.game.run()
                        elif self.crops_tab.collidepoint(mouse_pos):
                            self.current_shop_items = self.shop_items_crops
                            self.toggle_buttons_visibility(True)
                        elif self.upgrades_tab.collidepoint(mouse_pos):
                            self.current_shop_items = self.shop_items_upgrades
                            self.toggle_buttons_visibility(False)
                        elif self.add_button.collidepoint(mouse_pos) and self.cart:
                            if self.cart not in self.shop_items_upgrades:
                                self.cart_quantity += 1
                        elif self.subtract_button.collidepoint(mouse_pos) and self.cart and self.cart_quantity > 1:
                            if self.cart not in self.shop_items_upgrades:
                                self.cart_quantity -= 1
                        elif self.remove_button.collidepoint(mouse_pos):
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
                pygame.draw.rect(self.screen, self.GRAY, self.inventory_panel)
                pygame.draw.rect(self.screen, self.DARK_BROWN, self.shop_panel)
                self.draw_button(self.return_button, "Return To Game")
                self.draw_button(self.crops_tab, "Crops")
                self.draw_button(self.upgrades_tab, "Upgrades")
                self.draw_button(self.buy_button, "Buy")
                if self.show_sell_add_subtract:
                    self.draw_button(self.sell_button, "Sell")
                    self.draw_button(self.add_button, "+")
                    self.draw_button(self.subtract_button, "-")
                self.draw_button(self.remove_button, "X")

                for item in self.current_shop_items:
                    pygame.draw.rect(self.screen, self.GOLD if item == self.cart else self.WHITE, item["rect"])
                    label = self.font.render(f"{item['name']} - {item['price']} 💰", True, self.BLACK)
                    self.screen.blit(label, (item["rect"].x + 5, item["rect"].y + 10))

                if self.cart:
                    cart_label = self.font.render(f"{self.cart['name']} x{self.cart_quantity}", True, self.BLACK)
                    self.screen.blit(cart_label, (self.INVENTORY_WIDTH + 10, 150))
                    total = self.cart["price"] * self.cart_quantity
                    total_label = self.font.render(f"Total: {total} 💰", True, self.BLACK)
                    self.screen.blit(total_label, (self.WIDTH - 200, self.HEIGHT - 120))

                self.update_gold_display()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    shop = ShopUI()
    shop.run()
