import pygame
import sys
import random


# Счётчик времени в игре
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(str(current_time), False, (64, 64, 64))
    score_rec = (score_surface.get_rect(center=(400, 50)))
    screen.blit(score_surface, score_rec)
    return current_time


# Перемещение препятствий
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


pygame.init()

# Статус игры (True = играем, False = game over или intro)
game_active = False
# Время, проведённое в игре
start_time = 0
# Счёт
score = 0

# Установка разрешения окна
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Настройка текстов (шрифт, размер)
test_font = pygame.font.Font('media/font/Pixeltype.ttf', 50)

# Создание статических поверхностей
sky_surface = pygame.image.load('media/graphics/Sky.png').convert()
ground_surface = pygame.image.load('media/graphics/ground.png').convert()

# Создание динамических поверхностей
# Улитка
snail_surface = pygame.image.load('media/graphics/snail/snail1.png').convert_alpha()
# Муха
fly_surface = pygame.image.load('media/graphics/fly/fly1.png').convert_alpha()
# Игрок
player_surface = pygame.image.load('media/graphics/player/player_walk_1.png').convert_alpha()
player_rec = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0
# Список препятствий
obstacle_rect_list = []

# Вступительный экран
player_stand = pygame.image.load('media/graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rec = player_stand.get_rect(center=(400, 200))
game_message_surface = test_font.render('Press [space] to run', False, 'Black')
game_message_rec = game_message_surface.get_rect(center=(400, 320))
# Название игры
gameName_surface = test_font.render('Play', False, 'Black')
gameName_rec = gameName_surface.get_rect(center=(400, 50))

# Установка названия и иконки окна
pygame.display.set_caption('Пришелец против гигантских тварей 2D')
game_icon = pygame.image.load('media/graphics/snail/snail1.png').convert_alpha()
pygame.display.set_icon(game_icon)

# Инициализация часов для контроля частоты кадров
clock = pygame.time.Clock()

# Таймер
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

# Бесконечный цикл для отображения игрового окна
while True:
    # Отслеживание событий игрока
    for event in pygame.event.get():
        # Поимка события выхода из игры
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Считывание нажатия мыши (для воспроизведения прыжка)
        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if player_rec.collidepoint(event.pos) and player_rec.bottom == 300:
                player_gravity = -20
        # Считывание нажатия пробела
        if event.type == pygame.KEYDOWN:
            # (для воспроизведения прыжка)
            if event.key == pygame.K_SPACE and player_rec.bottom == 300 and game_active:
                player_gravity = -20
            # (для рестарта игры)
            elif event.key == pygame.K_SPACE and game_active is not True:

                start_time = int(pygame.time.get_ticks() / 1000)
                game_active = True
        if event.type == obstacle_timer and game_active:
            if random.randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(midbottom=(random.randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(midbottom=(random.randint(900, 1100), 210)))
    if game_active:
        # Установка статических поверхностей
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Отображение счёта игры
        score = display_score()

        # Установка динамических поверхностей
        # Игрок
        player_gravity += 1
        player_rec.bottom += player_gravity
        if player_rec.bottom >= 300:
            player_rec.bottom = 300
        screen.blit(player_surface, player_rec)
        # Препятствия
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Столкновение (game over)
        game_active = collisions(player_rec, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rec)

        # Очистка препятствий
        obstacle_rect_list.clear()
        # Обновление позиции игрока после проигрыша
        player_rec.midbottom = (80, 300)
        player_gravity = 0

        # Вывод счёта на экран game over
        score_message = test_font.render(f'Score: {score}', False, 'Black')
        score_message_rec = score_message.get_rect(center=(400, 380))
        if score != 0:
            screen.blit(score_message, score_message_rec)
        screen.blit(game_message_surface, game_message_rec)
        screen.blit(gameName_surface, gameName_rec)

    pygame.display.update()
    clock.tick(60)
