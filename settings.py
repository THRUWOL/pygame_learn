import pygame

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
