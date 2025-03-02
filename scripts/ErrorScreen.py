# import pygame
# from pygame import mixer
# from Log_In import LogInScreen

# class ErrorScreen:
#     def __init__(self):
#         # Initialize Pygame
#         pygame.init()

#         # Constants
#         self.WIDTH, self.HEIGHT = 800, 600
#         self.RED = (200, 0, 0)
#         self.WHITE = (255, 255, 255)
#         self.BLACK = (0, 0, 0)
#         self.FONT_SIZE = 40

#         # Setup display
#         self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
#         pygame.display.set_caption("Error Screen")
#         self.clock = pygame.time.Clock()
#         self.TIMER_CHANGE_SCREEN = pygame.USEREVENT + 1
#         pygame.time.set_timer(self.TIMER_CHANGE_SCREEN, 5000)

#         # Load font
#         self.font = pygame.font.Font(None, self.FONT_SIZE)

#         self.darkbg = pygame.image.load("assets/images/others/darkbg.png")
#         self.darkbg = pygame.transform.scale(self.darkbg, (self.WIDTH, self.HEIGHT))

#         self.errorsign = pygame.image.load("assets/images/others/errorsign_transparent.png")
#         self.errorsign = pygame.transform.scale(self.errorsign, (250, 400))

#         self.cloud = pygame.image.load("assets/images/others/rain_transparent.png")
#         self.cloud = pygame.transform.scale(self.cloud, (100, 100))

#         # Error message
#         mixer.init()
#         mixer.music.load("assets/sounds/error.mp3")
#         mixer.music.play()

#     def run(self):
#         running = True
#         while running:
#             # Set background to red
#             # Render error message
#             self.screen.blit(self.darkbg, (0, 0))
#             self.screen.blit(self.errorsign, ((self.WIDTH / 2) - 125, (self.HEIGHT / 2) - 100))
#             self.screen.blit(self.cloud, (((self.WIDTH / 2) - 50), (self.HEIGHT / 2) - 250))
#             self.screen.blit(self.cloud, (((self.WIDTH / 2) - 250), (self.HEIGHT / 2) - 250))
#             self.screen.blit(self.cloud, (((self.WIDTH / 2) + 150), (self.HEIGHT / 2) - 250))

#             # Event handling
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:  # Close button
#                     running = False
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_ESCAPE:  # Exit on ESC key
#                         running = False
#                     elif event.key == pygame.K_RETURN:
#                         # Call function from Log_In.py
#                         log_in_screen = LogInScreen()
#                         log_in_screen.run()
#                         running = False

#             self.clock.tick(30)
#             pygame.display.flip()  # Update the screen

#         pygame.quit()

# # Example usage:
# error_screen = ErrorScreen()
# error_screen.run()