import pygame


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
    return center, int(number / center)


def print_text(screen, message, x, y, color=(255, 255, 255), size=20, font=None):
    text = render_text(message, color, size, font)
    screen.blit(text, (x, y))


def render_text(message, color=(255, 255, 255), size=20, font=None):
    if font is None:
        font = pygame.font.SysFont('Arial', size)
    else:
        font = pygame.font.Font(font, size)
    text = font.render(message, True, color)
    return text
