import pygame
import math
from settings import *
from os import path
from game_functions import img_dir

def apply_freeze_effect(image):
        overlay = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 191, 255, 100))  # RGBA: голубой с прозрачностью
        frozen_image = image.copy()
        frozen_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return frozen_image

class Mob(pygame.sprite.Sprite):
    def __init__(self, formation_index, formation_row):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "baseEnemy.png")).convert(), (50, 40))
        self.image.set_colorkey(BLACK)
        self.og_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.formation_row = formation_row
        self.start_x = formation_index * 100 + 50
        self.start_y = -100
        
        self.rect.center = (self.start_x, self.start_y)

        # Для траектории
        self.trajectory_time = 0
        self.attack_phase = False
        self.formation_start_time = 0
        self.trajectory_duration = TRAJECTORY_DURATION * FPS
        self.in_formation = False

        #замедление
        self.slowed_end_time = 0
        self.slowed = False
        self.frozen_image = apply_freeze_effect(self.image)

    def update(self):
        if self.slowed:
            self.image = self.frozen_image
            if pygame.time.get_ticks() > self.slowed_end_time:
                self.slowed = False
                self.image = self.og_image
            else:
                return

        if not self.in_formation:
            # Движение по траектории (синусоида + движение вниз)
            self.trajectory_time += 1
            t = self.trajectory_time / FPS

            # Синусоидальное движение
            x = self.start_x + math.sin(t * 2) * 50
            y = self.start_y + t * 100  # скорость снижения

            self.rect.center = (x, y)

            if (self.formation_row == 1 and y == 80) or (self.formation_row == 2 and y == 200):
                self.in_formation = True
                self.formation_start_time = pygame.time.get_ticks()
        elif not self.attack_phase:
            now = pygame.time.get_ticks()
            if now - self.formation_start_time >= 2000:
                self.attack_phase = True
        if self.attack_phase:
            self.rect.y += 5

        if self.rect.top > HEIGHT:
            self.kill()

    def apply_slow(self):
        self.slowed = True
        self.slowed_end_time = pygame.time.get_ticks() + 2000
        
    
    