import pygame
import settingsdata
from pygame import mixer

class Unlock:
    def __init__(self, return_to_page):
        self.return_to_page = return_to_page
        pygame.init()
        mixer.init()

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("New Recipe Unlocked")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHTBROWN = (254, 195, 117)

        # Fonts
        self.font_large = pygame.font.Font(pygame.font.match_font("Irish Grover"), 36)
        self.font_small = pygame.font.Font(pygame.font.match_font("Irish Grover"), 24)

        # Text
        self.title_surface1 = self.font_large.render("CONGRATS!!!", True, self.BLACK)
        self.title_surface2 = self.font_small.render("YOU'VE UNLOCKED A NEW RECIPE!!!", True, self.BLACK)

        # Background
        self.background = pygame.image.load("images/pinksky.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Image / Recipe
        self.image_rect_size = 200
        self.image_rect = pygame.Rect(self.WIDTH // 2 - self.image_rect_size // 2, self.HEIGHT // 2, self.image_rect_size, self.image_rect_size)
        self.image_rect_surface = pygame.Surface((200, 200))
        self.image_rect_surface.fill(self.LIGHTBROWN)

        self.muffin = pygame.image.load("images/muffin.png")
        self.muffin = pygame.transform.scale(self.muffin, self.image_rect.size)

        # Button
        self.back_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 70, 200, 40)

        # Music
        mixer.music.load("tracks/06 - Victory!.mp3")
        mixer.music.set_volume(settingsdata.volumes[0] * settingsdata.volumes[1])
        mixer.music.play()

    def draw_text(self, surface, text, rect, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect.topleft)

    def draw_button_with_depth(self, surface, rect, color, shadow_offset=4, shadow_alpha=100):
        shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, shadow_alpha), shadow.get_rect(), border_radius=10)
        surface.blit(shadow, (rect.x + shadow_offset, rect.y + shadow_offset))
        pygame.draw.rect(surface, color, rect, border_radius=10)

    def run(self):
        running = True
        while running:
            self.screen.fill(self.LIGHTBROWN)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        print("Returning to previous page...")
                        running = False
                        self.return_to_page.run()

            # Draw everything
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.image_rect_surface, self.image_rect.topleft)
            self.screen.blit(self.title_surface1, (self.WIDTH // 2 - self.title_surface1.get_width() // 2, self.HEIGHT // 6))
            self.screen.blit(self.title_surface2, (self.WIDTH // 2 - self.title_surface2.get_width() // 2, self.HEIGHT // 3))
            self.screen.blit(self.muffin, self.image_rect.topleft)
            pygame.draw.rect(self.screen, self.BLACK, self.image_rect, 3)

            # Back button
            self.draw_button_with_depth(self.screen, self.back_button, self.LIGHTBROWN)
            self.draw_text(self.screen, "Back", self.back_button, self.font_small, self.BLACK)

            pygame.display.flip()

        pygame.quit()
