import random
from tkinter import Tk, simpledialog
import pygame
from classes import Game, Button
from utils import closest_divs, print_text, render_text
from math import sqrt
pygame.init()
pygame.font.init()


class PercentVisualisation(Game):

    # constants
    BLUE_MAN = pygame.image.load('assets\\blueman.png')
    YELLOW_MAN = pygame.image.load('assets\\yellowman.png')
    LIGHT = pygame.image.load('assets\\light.png')
    BACKGROUND = (30, 30, 30)

    def __init__(self):
        super().__init__((800, 800), 60, caption='Percent Visualisation', first_state=self.main)

        self.user_input = 1
        self.grid = []
        self.max_grid_size = round(1 / self.user_input * 100)
        self.square_width = self.width - 100
        self.square_height = self.height - 100
        self.man_size = int(sqrt((self.square_width * self.square_height) / self.max_grid_size))
        self.random_pos = (0, 0)
        self.info = False
        self.options = False
        self.mode2_size = 20

        # 0 - 1st mode
        # 1 - 2nd mode
        self.mode = 0

        self.buttons = [
            Button([10, self.height-40, 195, 30], self.screen, 'Change value',
                   (50, 50, 50), (40, 40, 40), command=self.value_entry),
            Button([205, self.height - 40, 195, 30], self.screen, 'Random value',
                   (50, 50, 50), (40, 40, 40), command=self.random_value),
            Button([400, self.height - 40, 195, 30], self.screen, 'Show info',
                   (50, 50, 50), (40, 40, 40), command=self.info_switch),
            Button([595, self.height - 40, 195, 30], self.screen, 'Options',
                   (50, 50, 50), (40, 40, 40), command=self.options_switch),
        ]

        self.option_buttons = [
            Button([self.width - 205, self.height - 220, 195, 30], self.screen, 'Mode 1',
                   (50, 50, 50), (40, 40, 40), command=lambda: self.mode_switch(0)),
            Button([self.width - 205, self.height - 170, 195, 30], self.screen, 'Mode 2',
                   (50, 50, 50), (40, 40, 40), command=lambda: self.mode_switch(1)),
            Button([self.width - 85, self.height - 140, 30, 30], self.screen, '+',
                   (50, 50, 50), (40, 40, 40), command=lambda: self.change_size(1)),
            Button([self.width - 55, self.height - 140, 30, 30], self.screen, '-',
                   (50, 50, 50), (40, 40, 40), command=lambda: self.change_size(-1)),
            Button([self.width - 135, self.height - 140, 30, 30], self.screen, '',
                   (50, 50, 50), (40, 40, 40), command=self.size_entry),
            Button([self.width - 30, self.height - 240, 20, 20], self.screen, 'X',
                   (50, 50, 50), (40, 40, 40), command=self.options_switch),
        ]

    def setup(self):
        """Setup before starting program loop."""
        super().setup()
        self.update_grid()

    def value_entry(self):
        """Enter new percent value."""
        root = Tk()
        root.withdraw()
        user_input = self.user_input
        self.user_input = simpledialog.askfloat('Entry', 'Enter your percent value here:',
                                                minvalue=0.001, maxvalue=100)
        if self.user_input is None:
            self.user_input = user_input
            return
        self.update_grid()

    def size_entry(self):
        """Enter new size value."""
        root = Tk()
        root.withdraw()
        size = self.mode2_size
        self.mode2_size = simpledialog.askinteger('Entry', 'New size:', minvalue=1)
        if self.mode2_size is None:
            self.mode2_size = size

    def show_info(self):
        """Display information"""
        rows, cols = closest_divs(self.max_grid_size)
        chance_info = render_text(f'Chance: ~ 1 / {self.max_grid_size}', color=(150, 150, 150))
        mode_info = render_text(f'Mode: {self.mode + 1}', color=(150, 150, 150))

        self.screen.blit(chance_info, (650, 0))
        self.screen.blit(mode_info, (650, 20))
        if not self.mode:
            print_text(self.screen, f'Grid size: {rows}x{cols}', 650, 40, color=(150, 150, 150))

    def show_options(self):
        """Display options."""
        pygame.draw.rect(self.screen, (40, 40, 40), (595, self.height - 240, 195, 200))

        for button in self.option_buttons:
            button.radius = 0
            button.draw()

        print_text(self.screen, f'size: {self.mode2_size}', self.width - 185, self.height - 140,
                   size=25, color=(150, 150, 150))

    def update_grid(self):
        """Update grid and update man's size."""

        # calculating max grid size with user input given
        self.max_grid_size = round(1 / self.user_input * 100)

        # calculating most optimal number of rows and columns to grid
        rows, cols = closest_divs(self.max_grid_size)

        # calculating size of picture to scale
        self.man_size = round(max(self.square_width, self.square_height) / max(rows, cols))

        # calculating offset of the whole grid
        x_offset = (self.width - rows * self.man_size) // 2
        y_offset = (self.height - cols * self.man_size) // 2

        # creating grid itself
        self.grid = [(row * self.man_size + x_offset, col * self.man_size + y_offset)
                     for row in range(rows) for col in range(cols)]

        # setting random pos for yellow guy
        self.random_pos = random.choice(self.grid)

    def random_value(self):
        self.user_input = round(random.random(), 3)
        if random.randint(0, 1):
            self.user_input += random.randint(0, 100)
        self.update_grid()
        pygame.time.wait(100)

    def info_switch(self):
        self.info = not self.info
        pygame.time.wait(100)

    def options_switch(self):
        self.options = not self.options
        pygame.time.wait(100)

    def mode_switch(self, mode):
        self.mode = mode
        pygame.time.wait(100)

    def change_size(self, value):
        if self.mode2_size < 2 and value < 0:
            return
        self.mode2_size += value
        pygame.time.wait(100)

    def draw_mode(self):
        if self.mode == 0:
            for pos in self.grid:
                self.screen.blit(pygame.transform.scale(self.BLUE_MAN, (self.man_size, self.man_size)), pos)

            # drawing yellow man images
            self.screen.blit(pygame.transform.scale(self.YELLOW_MAN, (self.man_size, self.man_size)), self.random_pos)
            self.screen.blit(pygame.transform.scale(self.LIGHT, (self.man_size, self.man_size)), self.random_pos)

        else:
            man_size = round(self.square_height / self.mode2_size)
            grid = [(row * man_size + 50, col * man_size + 50)
                    for row in range(self.mode2_size) for col in range(self.mode2_size)]

            for pos in grid:
                self.screen.blit(pygame.transform.scale(self.BLUE_MAN, (man_size, man_size)), pos)

            for pos in range(round(self.user_input/100 * self.mode2_size**2)):
                self.screen.blit(pygame.transform.scale(self.YELLOW_MAN, (man_size, man_size)),
                                 grid[pos])

    def main(self):
        """Main state of the program."""
        self.screen.fill(self.BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                pass

        # display percent value
        digits = [num for num in range(1, 101)]
        print_text(self.screen, f'{int(self.user_input) if self.user_input in digits else self.user_input}%',
                   5, 5, size=50)

        self.draw_mode()

        # draw buttons
        for button in self.buttons:
            button.radius = 0
            button.draw()

        # show information about grid size and chance
        if self.info:
            self.show_info()

        if self.options:
            self.show_options()


if __name__ == '__main__':
    my_game = PercentVisualisation()
    my_game.running = True
    my_game.start()
