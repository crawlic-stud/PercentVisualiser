import random
from tkinter import Tk, simpledialog
import pygame
from classes import Game, Button
from math import sqrt


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

    def setup(self):
        """Setup before starting program loop."""
        super().setup()
        # self.user_entry()

    def user_entry(self):
        """Enter new percent value."""
        root = Tk()
        root.withdraw()
        self.user_input = simpledialog.askfloat('Entry', 'Enter your percent value here:',
                                                minvalue=0.001, maxvalue=100)
        self.update_grid()
        self.random_pos = random.choice(self.grid)

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

        # print(rows, cols, rows * cols, self.max_grid_size, len(self.grid))
        # print(self.grid)

    def main(self):
        """Main state of the program."""
        self.screen.fill(self.BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.user_entry()

        # drawing all blue man images
        for pos in self.grid:
            self.screen.blit(pygame.transform.scale(self.BLUE_MAN, (self.man_size, self.man_size)), pos)

        # drawing yellow man images
        self.screen.blit(pygame.transform.scale(self.YELLOW_MAN, (self.man_size, self.man_size)), self.random_pos)
        self.screen.blit(pygame.transform.scale(self.LIGHT, (self.man_size, self.man_size)), self.random_pos)


def all_divs(number):
    """Finding all dividers of the number."""
    dividers = []
    for i in range(1, number + 1):
        if number % i == 0:
            dividers.append(i)
    return dividers


def closest_divs(number):
    """Finding two closest dividers of the number."""
    dividers = all_divs(number)
    center = dividers[len(dividers)//2]
    return center, int(number / center),


if __name__ == '__main__':
    my_game = PercentVisualisation()
    my_game.running = True
    my_game.start()
    # num = 100
    # divs = all_divs(num)
    # print(divs)
    # print(closest_divs(num))
