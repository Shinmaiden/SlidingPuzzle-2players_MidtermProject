import os, pygame

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 750

WHITE = (255, 255, 255)
GREY = (10, 10, 10)
BLACK = (0, 0, 0)
DISABLED = (150, 150, 150)

LOCAL_DIR = os.path.dirname(__file__)
PUZZLE_BORDER_SIZE = 0.165

big_font = pygame.font.Font(os.path.join(LOCAL_DIR, 'Assets/pixel.ttf'), 100)
medium_font = pygame.font.Font(os.path.join(LOCAL_DIR, 'Assets/pixel.ttf'), 70)
small_font = pygame.font.Font(os.path.join(LOCAL_DIR, 'Assets/pixel.ttf'), 40)

opposites = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}

ANIMATION_TIME = 100
