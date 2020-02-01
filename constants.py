from win32api import GetSystemMetrics
import pygame

# окно
WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
SCREEN_RECT = (0, 0, WIDTH, HEIGHT)


# спрайты
PLAYER_SPRITE = 'falcon.png'
PLAYER_BULLET_SPRITE = 'p_bullet.png'
ENEMY_BULLET_SPRITE = 'e_bullet.png'
OBSTACLES_SPRITE = 'rock.png'
ENEMY_SPRITE = 'tie_fighter.png'
BOSS_SPRITE = 'star_destroyer2.png'
BACKGROUND = 'stars_jpeg.jpg'
EARTH_SPRITE = 'planet_earth.jpg'

# размеры спрайтов
ENEMY_SPRITE_W = 53
ENEMY_SPRITE_H = 48

PLAYER_SPRITE_W = 100
PLAYER_SPRITE_H = 100

BOSS_SPRITE_W = 200
BOSS_SPRITE_H = 400

# hp bars
HP_BARS_W = 40
HP_BARS_H = 4

PLAYER_HP_BAR_R = 35

BOSS_BAR_W = 0.6    # в % от экрана
BOSS_BAR_H = 20

# характеристики игрока
PLAYER_SHOOT_KD = 0.3
PLAYER_GUN_LEN = 50

# характеристики врага (in angles)
ENEMY_W = 120  # angles in msec
ENEMY_SHOOT_KD = 0.5
ACCURACY = 10

# управление
DOUBLE_CLICK_S = 0.5

# groups
backgrounds = pygame.sprite.Group()
stars_background = pygame.sprite.Group()

obstacles = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
player = pygame.sprite.Group()
enemies = pygame.sprite.Group()
hp_bars = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

RENDER_ORDER = [stars_background, obstacles, enemy_bullets, player_bullets, boss_group,
                enemies, player, hp_bars]

# событие движения
MOTION = 30
pygame.time.set_timer(MOTION, 5)

