import pygame
from os import path
from settings import *


# Загрузка изображений
img_dir = path.join(path.dirname(__file__), 'assets/img')
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Инициализация групп спрайтов
all_sprites = pygame.sprite.Group()
mobs_row_1 = pygame.sprite.Group()
mobs_row_2 = pygame.sprite.Group()
mobs = pygame.sprite.Group()
spells = pygame.sprite.Group()
active_explosions = pygame.sprite.Group()


# Заполняем списки словаря картинками анимаций
# Словарь для хранения анимаций
spells_anims = {'Fire':[], 'Frost':[], 'Light':[]}
for key in spells_anims.keys():
    for i in range(1, 7):
        filename = f'{key}_0{i}.png'
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img = pygame.transform.rotate(img, -90)
        img = pygame.transform.scale(img, (30, 60))
        img.set_colorkey(WHITE)
        spells_anims[key].append(img)

baseSpell_img = pygame.image.load(path.join(img_dir, "baseSpell.png")).convert()

explosion_anim = []
for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (80, 90))
    explosion_anim.append(img)

def draw_button(surface, text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))

    small_text = pygame.font.SysFont("arial", 24)
    text_surf = small_text.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    surface.blit(text_surf, text_rect)

def draw_text(surf, text, size, x, y):
    font = pygame.font.match_font('arial')
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_hp_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
