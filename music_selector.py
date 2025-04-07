import pygame

class MusicSelector:
    def __init__(self, screen, width, height, music_tracks, current_track_index=0):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.music_tracks = music_tracks
        self.current_track_index = current_track_index

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)
        self.DARK_BROWN = (38, 35, 34)
        self.BROWN = (99, 55, 44)
        self.WHITE = (255, 255, 255)
        self.ACTIVE_COLOR = (160, 100, 80)

        # Fonts
        self.title_font = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.button_font = pygame.font.Font(pygame.font.match_font('courier'), 18)

        # Buttons
        self.left_button = pygame.Rect(280, 300, 30, 30)
        self.right_button = pygame.Rect(490, 300, 30, 30)
        self.back_button = pygame.Rect(self.WIDTH // 2 - 40, 500, 80, 30)

        self.track_rects = []  # Store rectangles for each track for click detection

    def draw(self):
        """Draw the music selector menu."""
        self.screen.fill(self.LIGHT_BROWN)

        # Draw Background Panels
        middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
        pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)
        panel_rect = pygame.Rect(180, 50, 450, 500)
        pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)

        # Draw Title
        title_text = self.title_font.render("MUSIC SELECTOR", True, self.WHITE)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 85))

        # Draw Music Tracks as a List with Solid Borders
        self.track_rects.clear()
        y_offset = 150
        for i, track in enumerate(self.music_tracks):
            track_color = self.ACTIVE_COLOR if i == self.current_track_index else self.WHITE
            track_text = self.button_font.render(track, True, track_color)
            track_rect = track_text.get_rect(center=(self.WIDTH // 2, y_offset))

            # Draw Solid Border
            border_rect = pygame.Rect(
                track_rect.left - 10, track_rect.top - 5, 
                track_rect.width + 20, track_rect.height + 10
            )
            pygame.draw.rect(self.screen, self.WHITE, border_rect, width=2)  # Solid border with width 2

            # Draw Track Text
            self.track_rects.append(track_rect)
            self.screen.blit(track_text, track_rect)
            y_offset += 50  # Increased spacing between options

        # Draw Back Button
        pygame.draw.rect(self.screen, self.ACTIVE_COLOR, self.back_button, border_radius=5)
        back_text = self.button_font.render("BACK", True, self.WHITE)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

    def handle_events(self, events):
        """Handle events for the music selector menu."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check Music Track Selection
                for i, track_rect in enumerate(self.track_rects):
                    if track_rect.collidepoint(mouse_pos):
                        self.current_track_index = i

                # Check Back Button
                if self.back_button.collidepoint(mouse_pos):
                    return "back"

        return None

    def run(self):
        """Run the music selector menu."""
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"

            action = self.handle_events(events)
            if action == "back":
                return "options"

            self.draw()
            pygame.display.flip()
