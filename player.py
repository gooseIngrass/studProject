import pygame
from settings import *
from spell import LightSpell, FireSpell, FrostSpell
from os import path
from game_functions import all_sprites, spells, img_dir

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "mage.png")).convert(), (50, 40))
        self.image.set_colorkey(BLACK)
        self.radius = 20

        self.hp = 100

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx -= 8
        if keystate[pygame.K_RIGHT]:
            self.speedx += 8
        
        self.rect.x += self.speedx

        # Если выйдет за пределы экрана - персонаж остановится
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, spell_name):
        if spell_name == 'Fire':
            spell = FireSpell(self.rect.centerx, self.rect.top)
        elif spell_name == 'Frost':
            spell = FrostSpell(self.rect.centerx, self.rect.top)
        else:
            spell = LightSpell(self.rect.centerx, self.rect.top)
        all_sprites.add(spell)
        spells.add(spell)