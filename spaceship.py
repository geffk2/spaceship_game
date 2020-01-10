from load_image import load_image
import pygame
from math import sin, cos, pi, sqrt
from numpy import arctan2
from random import uniform


# окно
WIDTH, HEIGHT = 1024, 1024
SCREEN_RECT = (0, 0, WIDTH, HEIGHT)


# спрайты
PLAYER_SPRITE = 'falcon.png'
PLAYER_BULLET_SPRITE = 'p_bullet.png'
ENEMY_BULLET_SPRITE = 'e_bullet.png'
OBSTACLES_SPRITE = 'rock.png'
ENEMY_SPRITE = 'tie_fighter.png'

ENEMY_SPRITE_W = 53
ENEMY_SPRITE_H = 48

# характеристики игрока
PLAYER_SHOOT_KD = 0.1
PLAYER_GUN_LEN = 50

# характеристики врага (in angles)
ENEMY_W = 30  # angles in sec
ENEMY_SHOOT_KD = 0.5
ACCURACY = 10


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, max_speed=200, max_acceleration=50,
                 direction=0, image_w=100, image_h=100):
        super().__init__(group)

        self.image_w, self.image_h = image_w, image_h

        # исходное изображение для того, чтобы не затирать методом rotate (up_d) картинку
        self.source_image = load_image(sprite)
        self.source_image = pygame.transform.scale(self.source_image, (self.image_w, self.image_h))

        self.image = self.source_image
        self.rect = self.image.get_rect()

        # маска
        self.mask = pygame.mask.from_surface(self.image)

        # hp
        self.hp = 100

        # целочисленные координаты верхнего левого края
        self.rect.x = int(coords[0])
        self.rect.y = int(coords[1])

        # дробные координаты центра
        self.x = coords[0] + self.image_w / 2
        self.y = coords[1] + self.image_h / 2

        # начальная и максимальная скорости
        self.speed = 0
        self.max_speed = max_speed

        # начальное и максимальное ускорение
        self.acceleration = 0
        self.max_acceleration = max_acceleration

        # направление движения
        self.direction = direction

        # таймер выстрела игрока
        self.shoot_timer = 0

    def get_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def collision(self, groups):
        for group in groups:
            for sprite in group:
                if pygame.sprite.collide_mask(self, sprite):
                    self.get_damage(sprite.dmg)
                    sprite.kill()

    def shoot(self, bullets_type):
        Bullet([self.x, self.y], PLAYER_BULLET_SPRITE, bullets_type, self.direction)


class Player(Spaceship):
    def event_treatment(self, event):
        states = pygame.key.get_pressed()

        # acceleration properties
        new_properties = 0

        if event.type == MOTION:
            if states[pygame.K_LCTRL]:
                new_properties = -1
            elif states[pygame.K_LSHIFT]:
                new_properties = 1

            self.update_acceleration(new_properties)

        if (event.type == pygame.KEYUP and event.key == pygame.K_SPACE) \
                or states[pygame.K_SPACE]:
            if self.shoot_timer >= PLAYER_SHOOT_KD:
                self.shoot_timer = 0
                self.shoot(player_bullets)

        if event.type == pygame.MOUSEMOTION:
            self.update_direction(event.pos)

    def update(self, time):
        # обновление таймера
        self.shoot_timer += time

        # обновление координат
        self.x += (self.speed * time + self.acceleration * (time ** 2) / 2) * cos(self.direction)
        self.y += (self.speed * time + self.acceleration * (time ** 2) / 2) * sin(self.direction)

        self.rect.x = int(self.x - self.image_w / 2)
        self.rect.y = int(self.y - self.image_h / 2)

        # обновление скорости
        self.speed += self.acceleration * time
        self.speed = min(self.max_speed, self.speed)

        if self.speed < 0:
            self.speed = 0

        # проверка столкновений
        self.collision([enemy_bullets, obstacles])

    def update_acceleration(self, prop):
        # обновление ускорения
        if prop == 1:
            self.acceleration = self.max_acceleration
        elif self.speed != 0:
            if prop == -1:
                self.acceleration = -2 * self.max_acceleration
            else:
                self.acceleration = -self.max_acceleration
        else:
            self.acceleration = 0

    def update_direction(self, view_point):
        dx, dy = view_point[0] - self.x,  view_point[1] - self.y
        self.direction = arctan2(dy, dx)

        # rotate image
        self.image = pygame.transform.rotate(self.source_image, 360 - 180 * self.direction / pi)
        self.image_w, self.image_h = self.image.get_size()

        self.rect.x = int(self.x - self.image_w / 2)
        self.rect.y = int(self.y - self.image_h / 2)

        # обновление маски
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(Spaceship):
    def update(self, time):
        # обновление таймера
        self.shoot_timer += time

        # угол между кораблями
        direction = arctan2(spaceship.y - self.y, spaceship.x - self.x)

        if self.shoot_timer >= ENEMY_SHOOT_KD:
            self.shoot_timer = 0
            direction += uniform(-1, 1) * ACCURACY * pi / 180
            Bullet([self.x, self.y], ENEMY_BULLET_SPRITE, enemy_bullets, direction)

        r = sqrt((spaceship.x - self.x) ** 2 + (spaceship.y - self.y) ** 2)
        alpha = arctan2(self.y - spaceship.y, self.x - spaceship.x) + ENEMY_W * time * pi / 180

        self.x = r * cos(alpha) + spaceship.x
        self.y = r * sin(alpha) + spaceship.y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.collision([player_bullets, obstacles])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, direction, dmg=10, speed=500):
        super().__init__(group)

        self.image = pygame.transform.rotate(load_image(sprite), 180 - 180 * direction / pi)
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        self.direction = direction

        self.x = coords[0]
        self.y = coords[1]

        # подгон начала пули под пушку корабля
        angle = 180 - 180 * direction / pi
        img_w, img_h = self.image.get_size()

        if 0 < angle < 90:
            self.y -= img_h
        if 90 < angle < 180:
            self.x -= img_w
            self.y -= img_h
        if 180 < angle < 270:
            self.x -= img_w

        self.x += cos(self.direction) * PLAYER_GUN_LEN
        self.y += sin(self.direction) * PLAYER_GUN_LEN

        self.dmg = dmg
        self.speed = speed

    def update(self, time):
        self.x += cos(self.direction) * time * self.speed
        self.y += sin(self.direction) * time * self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, size_w=50):
        super().__init__(group)

        self.image = load_image(sprite)
        self.dmg = 9999

        img_w, img_h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,
                                            (size_w, img_h * size_w // img_h))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect.x = int(coords[0])
        self.rect.y = int(coords[1])


class Camera:
    pass


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # groups
    obstacles = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    player = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    RENDER_ORDER = [obstacles, enemy_bullets, player_bullets, enemies, player]

    # test obstacles
    obs_1 = Obstacle((10, 10), OBSTACLES_SPRITE, obstacles)
    obs_2 = Obstacle((650, 150), OBSTACLES_SPRITE, obstacles, size_w=100)

    # player spaceship
    spaceship = Player([206, 206], PLAYER_SPRITE, player)

    # enemy
    enemy_1 = Enemy([206, 0], ENEMY_SPRITE, enemies,
                    image_h=ENEMY_SPRITE_H, image_w=ENEMY_SPRITE_W)

    # clock
    clock = pygame.time.Clock()

    # событие движения
    MOTION = 30
    pygame.time.set_timer(MOTION, 5)

    running = True
    while running:
        screen.fill((0, 0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            spaceship.event_treatment(e)

        t = clock.tick()

        for sprite_group in RENDER_ORDER:
            sprite_group.update(t / 1000)
            sprite_group.draw(screen)
        pygame.display.flip()

