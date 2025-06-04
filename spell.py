import pygame
from game_functions import spells_anims, active_explosions, explosion_anim, mobs
from settings import *

class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, spell_name):
        pygame.sprite.Sprite.__init__(self)
        self.spell_name = spell_name
        
        self.image = pygame.Surface((50, 70))
        self.image = spells_anims[self.spell_name][0]
        
        # Параметры для анимации 
        self.frame = 0
        self.frame_rate = 120
        self.last_update = pygame.time.get_ticks()

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15  # Отрицательное значение, чтобы снаряд летел вверх

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(spells_anims[self.spell_name]):
                self.kill()
            else:
                self.image = spells_anims[self.spell_name][self.frame]
                
        self.rect.y += self.speedy
        # Удалить, если снаряд выходит за экран
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((100, 100))
        self.image = explosion_anim[0]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
       
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        hit_mob = pygame.sprite.spritecollideany(self, mobs)
        if hit_mob:
            event = pygame.event.Event(MOB_KILLED_EVENT, {"points": 1})
            pygame.event.post(event)
            hit_mob.kill()

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class FireSpell(Spell):
    def __init__(self, x, y):
        super().__init__(x, y, "Fire")
        self.speedy = -8
        self.damage = 15

    def update(self):
        super().update()
        hit_mob = pygame.sprite.spritecollideany(self, mobs)
        if hit_mob:
            self.create_explosion()
            self.kill()

        # Если заклинание вышло за экран
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

    def create_explosion(self):
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        active_explosions.add(explosion)

class FrostSpell(Spell):
    def __init__(self, x, y):
        super().__init__(x, y, "Frost")
        self.speedy = -10  # Замедлим немного по сравнению с другими
        self.damage = 10

    def update(self):
        super().update()
        hit_mob = pygame.sprite.spritecollideany(self, mobs)
        if hit_mob:
            hit_mob.apply_slow()
            self.kill()

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class LightSpell(Spell):
    def __init__(self, x, y):
        super().__init__(x, y, "Light")
        self.speedy = -15 
        self.damage = 10

    def update(self):
        super().update()
        hit_mob = pygame.sprite.spritecollideany(self, mobs)
        if hit_mob:
            event = pygame.event.Event(MOB_KILLED_EVENT, {"points": 1})
            pygame.event.post(event)
            hit_mob.kill()

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()
        

