import pygame


class Game:
    def __init__(self, window=(500, 500), fps=60, caption=None, icon=None, first_state=None):
        self.FPS = fps
        self.window = window
        self.caption = caption
        self.icon = icon
        self.game_state = first_state
        self.width = window[0]
        self.height = window[1]

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.window)
        self.running = True

    def setup(self):
        """Setup anything you want before starting game"""
        if self.caption is not None:
            pygame.display.set_caption(self.caption)
        if self.icon is not None:
            pygame.display.set_icon(self.icon)

    def change_state(self, state):
        self.game_state = state

    def run(self):
        """Run game events"""
        self.clock.tick(self.FPS)
        if self.game_state is not None:
            self.game_state()
        pygame.display.update()

    def start(self):
        """Setup and loop all events while running"""
        self.setup()
        while self.running:
            self.run()


class Button:
    def __init__(self, rect, surface, text, active_color, inactive_color, command=None):
        """Create and draw button on screen"""
        self.rect = rect
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.screen = surface
        self.text = text
        self.text_len = 0
        self.command = command
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.outline = 3
        self.radius = 3

    def print_text(self, message, x, y, font_color=(100, 100, 100), font='Arial', font_size=30):
        """Prints text on button"""
        font = pygame.font.SysFont(font, font_size)
        text = font.render(message, True, font_color)
        self.text_len = text.get_width()
        self.screen.blit(font.render(message, True, (0, 0, 0)), (x + 1, y + 1))
        self.screen.blit(text, (x, y))

    def draw(self):
        """Draws button and text on it"""
        if self.collide():
            pygame.draw.rect(self.screen, self.active_color, self.rect, border_radius=self.radius)
            self.click()
        else:
            pygame.draw.rect(self.screen, self.inactive_color, self.rect, border_radius=self.radius)

        # center text
        text_x_pos = self.x + (self.width - self.text_len) // 2
        text_y_pos = self.y - self.height//10
        self.print_text(self.text, text_x_pos, text_y_pos, font_size=self.height)

    def collide(self):
        """Check if cursor collides with button"""
        x, y = pygame.mouse.get_pos()
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return True
        return False

    def click(self):
        """If button is clicked - command()"""
        if self.command is None:
            return
        if self.collide() and pygame.mouse.get_pressed()[0]:
            self.command()
