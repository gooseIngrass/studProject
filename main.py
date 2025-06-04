import pygame
from os import path
from settings import *
from player import Player
from mob import Mob
from spell import FireSpell, FrostSpell
from game_functions import draw_text, draw_hp_bar, active_explosions, mobs, all_sprites, mobs_row_1, mobs_row_2, spells, img_dir, screen

background = pygame.image.load(path.join(img_dir, 'darkPurple.png')).convert()
background = pygame.transform.scale(background, (480, 600))
background_rect = background.get_rect()


# Инициализация Pygame и создание окна
pygame.init()

pygame.display.set_caption("FIREBALL")
clock = pygame.time.Clock()

    
#Меню
def show_start_screen():
    font = pygame.font.SysFont("arial", 48)
    title = font.render("FIREBALL", True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)

    waiting = True
    while waiting:
        screen.blit(background, (0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        pygame.draw.rect(screen, GREEN, button_rect)
        
        draw_text(screen, "Начать", 28, WIDTH // 2, HEIGHT // 2 - 15)
        draw_text(screen, "Для управления кораблём используйте стрелки ← →", 20, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text(screen, "Для выбора оружия используйте стрелки ↑ ↓", 20, WIDTH // 2, HEIGHT // 2 + 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

        pygame.display.flip()
#Окончание игры
def show_end_screen(score, win):
    font = pygame.font.SysFont("arial", 48)
    if win:
        msg_text = "YOU WON"
    else:
        msg_text = "Nice try..."
    msg = font.render(msg_text, True, WHITE)
    title = font.render(f'Your score {score}', True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    restart_game()
    waiting = True
    while waiting:
        screen.blit(background, (0, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 4 - 40))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        pygame.draw.rect(screen, GREEN, button_rect)
        draw_text(screen, "Начать заново", 28, WIDTH // 2, HEIGHT // 2 - 15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

        pygame.display.flip()

def restart_game():
    global player

    all_sprites.empty()
    mobs.empty()
    spells.empty()
    active_explosions.empty()

    player = Player()
    all_sprites.add(player)

    # Генерируем мобов
    newmob(mobs_row_1, 1)
    newmob(mobs_row_2, 2)


def newmob(group, row=None):
    for i in range(5):
        m = Mob(i, row)
        mobs.add(m)
        group.add(m)


player = Player()
all_sprites.add(player)

# Генерируем мобов
newmob(mobs_row_1, 1)
newmob(mobs_row_2, 2)

score = 0
spell_index = 1
spell_index_dict = {1:'Fire', 2:'Frost', 3:'Light'}

#Вызываем меню перед игрой
show_start_screen()
# Основной цикл игры

running = True
while running:
    clock.tick(FPS)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot(spell_index_dict[spell_index])
            if event.key == pygame.K_UP and spell_index < 3:
                spell_index += 1
            elif event.key == pygame.K_DOWN and spell_index > 1:
                spell_index -= 1
        elif event.type == MOB_KILLED_EVENT:
            score += 1
            if(score >= 100):
                show_end_screen(score, 1)
                score = 0
    # Обновление
    all_sprites.update()
    mobs.update()
    active_explosions.update()
    
        
    
    # Восполняем ряды мобов, если их убили 
    if not mobs_row_1:
        newmob(mobs_row_1, 1)
    if not mobs_row_2:
        newmob(mobs_row_2, 2)
        
    hits_player = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits_player:
        player.hp -= 20
        if player.hp <= 0:
            show_end_screen(score, 0)
            score = 0

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    mobs.draw(screen)
    active_explosions.draw(screen)
    # Рисуем мобов только если убит весь ряд
    # if not mobs_row_1:
    #     mobs_row_1.draw(screen)
    # if not mobs_row_2:
    #     mobs_row_2.draw(screen)

    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_hp_bar(screen, 5, 5, player.hp)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()