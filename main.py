import pygame
import sys

pygame.init()

# Установка разрешения окна
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Настройка текстов (шрифт, размер)
test_font = pygame.font.Font('media/font/Pixeltype.ttf', 50)

# Создание статических поверхностей
sky_surface = pygame.image.load('media/graphics/Sky.png').convert()
ground_surface = pygame.image.load('media/graphics/ground.png').convert()
text_surface = test_font.render('Test', False, 'black').convert()

# Создание динамических поверхностей
snail_surface = pygame.image.load('media/graphics/snail/snail1.png').convert_alpha()
snail_x_pos = 700

player_surface = pygame.image.load('media/graphics/player/player_walk_1.png').convert_alpha()

# Установка названия и иконки окна
pygame.display.set_caption('Test')
game_icon = pygame.image.load('media/icon.png').convert()
pygame.display.set_icon(game_icon)

# Инициализация часов для контроля частоты кадров
clock = pygame.time.Clock()

# Бесконечный цикл для отображения игрового окна
while True:
    # Отслеживание событий игрока
    for event in pygame.event.get():
        # Поимка события выхода из игры
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Установка статических поверхностей
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (370, 50))

    # Установка динамических поверхностей
    # Перемещение улитки (изменяем позицию улитки по координате X)
    snail_x_pos -= 3
    if snail_x_pos < -100:
        snail_x_pos = 800
    screen.blit(snail_surface, (snail_x_pos, 265))

    screen.blit(player_surface, (80, 200))

    pygame.display.update()
    clock.tick(60)
