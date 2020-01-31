from classes_spaceship import *
from adds import *
from obstacles import Obstacle
from constants import *
from buttons import Button
from settings import setting
from load_image import terminate
from planet import Planet


def start_screen():
    buttons = [
               Button(WIDTH // 6, 2 * HEIGHT // 12, WIDTH // 3,
                      HEIGHT // 6, 'Play', pygame.Color('black')),
               Button(WIDTH // 6, 5 * HEIGHT // 12, WIDTH // 3,
                      HEIGHT // 6, 'Settings', pygame.Color('black')),
               Button(WIDTH // 6, 8 * HEIGHT // 12, WIDTH // 3,
                      HEIGHT // 6, 'Exit', pygame.Color('black'))
               ]

    while True:
        screen.fill((255, 255, 255))

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.is_selected(event.pos):
                        button.col = (255, 255, 0)
                    else:
                        button.col = pygame.Color('black')
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.is_selected(event.pos):
                        idx = buttons.index(button)
                        if idx == 0:
                            return
                        if idx == 1:
                            setting()
                        if idx == 2:
                            terminate()

        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

start_screen()

# background
# Background(backgrounds)

# test obstacles
# obs_1 = Obstacle((10, 10), OBSTACLES_SPRITE, obstacles)
obs_2 = Obstacle((650, 150), OBSTACLES_SPRITE, obstacles, size_w=100)

# player spaceship
spaceship = Player([206, 206], PLAYER_SPRITE, player, hp=999999999200,
                   image_w=PLAYER_SPRITE_W, image_h=PLAYER_SPRITE_H,
                   bar_type='circle', max_speed=300)

# enemy
'''
enemy_1 = Enemy([206, 0], ENEMY_SPRITE, enemies,
                image_h=ENEMY_SPRITE_H, image_w=ENEMY_SPRITE_W)

enemy_2 = Enemy([0, 206], ENEMY_SPRITE, enemies,
                image_h=ENEMY_SPRITE_H, image_w=ENEMY_SPRITE_W)
'''
enemy_3 = Enemy([0, 0], ENEMY_SPRITE, enemies,
                image_h=ENEMY_SPRITE_H, image_w=ENEMY_SPRITE_W, hp=99999900)

# boss
# boss = BossShip([400, 400], BOSS_SPRITE, boss_group)

earth = Planet([800, 800], EARTH_SPRITE, obstacles)
spaceship.set_spawn(earth)

# clock
clock = pygame.time.Clock()

# camera
camera = Camera(spaceship)

# buttons in pause
pause_buttons = [Button(WIDTH // 2 - 100, HEIGHT // 2 - 150, 200,
                        50, 'Resume', pygame.Color('white'), txt_col=(0, 0, 0)),
                 Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200,
                        50, 'Settings', pygame.Color('white'), txt_col=(0, 0, 0)),
                 Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200,
                        50, 'Menu', pygame.Color('white'), txt_col=(0, 0, 0))]

paused = False
while True:
    screen.fill((0, 0, 0))

    t = clock.tick(60) / 1000
    camera.update(t)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            terminate()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_t:
                camera.pressed()
            if e.key == pygame.K_ESCAPE:
                paused = not paused
        if e.type == pygame.MOUSEMOTION:
            for button in pause_buttons:
                if button.is_selected(e.pos):
                    button.col = (255, 255, 0)
                else:
                    button.col = (255, 255, 255)
        if e.type == pygame.MOUSEBUTTONUP:
            for button in pause_buttons:
                if button.is_selected(e.pos):
                    idx = pause_buttons.index(button)
                    if idx == 0:
                        paused = not paused
                    if idx == 1:
                        setting()
                    if idx == 2:
                        start_screen()
        if not paused:
            spaceship.event_treatment(e)

    for sprite_group in RENDER_ORDER:
        if sprite_group != hp_bars:
            for sprite in sprite_group:
                camera.apply(sprite)
        if not paused:
            sprite_group.update(t, spaceship)
        sprite_group.draw(screen)

    if paused:
        for button in pause_buttons:
            button.draw(screen)

    pygame.display.flip()
