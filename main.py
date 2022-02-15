import pygame
import sys
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('media/graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('media/graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('media/graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('media/audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('media/graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('media/graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('media/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('media/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


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


pygame.init()

# Статус игры (True = играем, False = game over или intro)
game_active = False
# Время, проведённое в игре
start_time = 0
# Счёт
score = 0
# Звук игры
bg_Music = pygame.mixer.Sound('media/audio/music.wav')
bg_Music.set_volume(0)
bg_Music.play(loops=-1)

# Установка разрешения окна
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
# Настройка текстов (шрифт, размер)
test_font = pygame.font.Font('media/font/Pixeltype.ttf', 50)
# Создание статических поверхностей
sky_surface = pygame.image.load('media/graphics/Sky.png').convert()
ground_surface = pygame.image.load('media/graphics/ground.png').convert()

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
game_icon = pygame.image.load('media/icon.png').convert_alpha()
pygame.display.set_icon(game_icon)

# Инициализация часов для контроля частоты кадров
clock = pygame.time.Clock()
# Таймер спавна врагов
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)
# Таймер смены анимации улитки
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
# Таймер смены анимации мухи
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                obstacle_group.add(Obstacle(random.choice(['fly', 'snail', 'snail', 'snail'])))

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
