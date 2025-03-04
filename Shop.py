import pygame
import pygame_gui

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SHOP_WIDTH = WIDTH // 4
INVENTORY_WIDTH = WIDTH - SHOP_WIDTH
UI_HEIGHT = HEIGHT
GRID_ROWS, GRID_COLS = 4, 5
CELL_SIZE = 80

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 100, 75)
DARK_BROWN = (100, 50, 25)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shop & Inventory UI")

# UI Manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Shop Icon
shop_icon = pygame.Rect(10, HEIGHT - 60, 50, 50)

# UI Panels
shop_panel = pygame.Rect(INVENTORY_WIDTH, 0, SHOP_WIDTH, HEIGHT)
inventory_panel = pygame.Rect(0, 0, INVENTORY_WIDTH, HEIGHT)

# Tabs
crops_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(120, 10, 100, 40), text="Crops", manager=manager)
upgrades_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(220, 10, 100, 40), text="Upgrades", manager=manager)

# Shop Buttons
buy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(WIDTH - 100, HEIGHT - 80, 80, 40), text="Buy", manager=manager)
sell_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(WIDTH - 200, HEIGHT - 80, 80, 40), text="Sell", manager=manager)

# Back Button
back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(10, 10, 80, 40), text="Back", manager=manager)

# Gold Display
gold = 1000
gold_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(INVENTORY_WIDTH - 100, 10, 90, 30), text=f"{gold} 💰", manager=manager)

# Inventory and Shop Items
inventory = []
shop_items_crops = [
    {"name": "Carrot", "price": 5, "rect": pygame.Rect(120, 100, 100, 40)},
    {"name": "Corn", "price": 10, "rect": pygame.Rect(250, 100, 100, 40)}
]
shop_items_upgrades = [
    {"name": "House Upgrade", "price": 100, "rect": pygame.Rect(120, 100, 150, 40)},
    {"name": "Inventory Upgrade", "price": 25, "rect": pygame.Rect(300, 100, 150, 40)}
]

current_shop_items = shop_items_crops

# State
shop_open = False
selected_item = None
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not shop_open:
            if shop_icon.collidepoint(event.pos):
                shop_open = True  # Open shop
        elif event.type == pygame.MOUSEBUTTONDOWN and shop_open:
            for item in current_shop_items:
                if item["rect"].collidepoint(event.pos):
                    selected_item = item  # Select item
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == back_button:
                shop_open = False  # Close shop
            elif event.ui_element == buy_button and selected_item:
                if gold >= selected_item["price"]:
                    gold -= selected_item["price"]
                    inventory.append(selected_item)
                    gold_text.set_text(f"{gold} 💰")
                    if selected_item in shop_items_upgrades:
                        selected_item["price"] = 0 # Repurchasing/Selling makes 0 gold, future errors look here if there are further upgrades!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        shop_items_upgrades.remove(selected_item)  # Remove upgrade after purchase
            elif event.ui_element == sell_button and selected_item in inventory:
                inventory.remove(selected_item)
                gold += selected_item["price"]
                gold_text.set_text(f"{gold} 💰")
            elif event.ui_element == crops_tab:
                current_shop_items = shop_items_crops
            elif event.ui_element == upgrades_tab:
                current_shop_items = shop_items_upgrades

        manager.process_events(event)
    
    if shop_open:
        pygame.draw.rect(screen, GRAY, inventory_panel)  # Inventory side
        pygame.draw.rect(screen, DARK_BROWN, shop_panel)  # Shop side
        for item in current_shop_items:
            pygame.draw.rect(screen, GOLD if item == selected_item else WHITE, item["rect"])
            font = pygame.font.Font(None, 24)
            text_surface = font.render(f"{item['name']} - {item['price']}💰", True, BLACK)
            screen.blit(text_surface, (item["rect"].x + 5, item["rect"].y + 10))
        manager.update(time_delta)
        manager.draw_ui(screen)
    else:
        pygame.draw.rect(screen, BLACK, shop_icon)  # Shop icon
        pygame.draw.line(screen, WHITE, shop_icon.topleft, shop_icon.bottomright, 3)
        pygame.draw.line(screen, WHITE, shop_icon.topright, shop_icon.bottomleft, 3)
    
    pygame.display.flip()

pygame.quit()
