import pygame
import sys

from random import choice

from player import Player
from obstacle import Obstacle


# Счётчик времени в игре
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(str(current_time), False, (64, 64, 64))
    score_rec = (score_surface.get_rect(center=(400, 50)))
    screen.blit(score_surface, score_rec)
    return current_time


# Проверка столкновений
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


if __name__ == '__main__':
    pygame.init()
    from settings import *

# Статус игры (True = играем, False = game over или intro)
game_active = False
# Время, проведённое в игре
start_time = 0
# Счёт
score = 0

# Группы
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

while True:
    # Отслеживание событий игрока
    for event in pygame.event.get():
        # Поимка события выхода из игры
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Считывание нажатия пробела для рестарта игры
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active is not True:
                start_time = int(pygame.time.get_ticks() / 1000)
                game_active = True
        # Добаление врагов на экран
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

    if game_active:
        bg_Music.set_volume(0.3)
        # Установка бэкрграунда и игровой поверхности
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # Отображение счёта игры
        score = display_score()
        # Игрок
        player.draw(screen)
        player.update()
        # Препятствия
        obstacle_group.draw(screen)
        obstacle_group.update()
        # Обработка столкновений
        game_active = collision_sprite()

    else:
        bg_Music.set_volume(0.1)
        # Заливка неигрового экрана
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rec)
        # Вывод счёта на экран game over
        score_message = test_font.render(f'Score: {score}', False, 'Black')
        score_message_rec = score_message.get_rect(center=(400, 380))
        if score != 0:
            screen.blit(score_message, score_message_rec)
        screen.blit(game_message_surface, game_message_rec)
        screen.blit(gameName_surface, gameName_rec)

    pygame.display.update()
    clock.tick(60)
