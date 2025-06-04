# Настройки экрана
import pygame
WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Настройки формирования мобов
FORMATION_X_SPACING = 100
FORMATION_Y = 100
TRAJECTORY_DURATION = 3  # секунд

MOB_KILLED_EVENT = pygame.USEREVENT + 1