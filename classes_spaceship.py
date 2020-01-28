from math import sin, cos, pi, sqrt
from numpy import arctan2
from random import uniform
from classes_bars import HpBar, PlayerBar
from bullet import Bullet
from constants import *
from load_image import load_image


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, max_speed=200, max_acceleration=50,
                 direction=0, image_w=100, image_h=100, collision_dmg=30,
                 hp=100, bar_type='line'):
        super().__init__(group)

        self.image_w, self.image_h = image_w, image_h
        self.collision_dmg = collision_dmg

        # исходное изображение для того, чтобы не затирать методом rotate (up_d) картинку
        self.source_image = load_image(sprite)
        self.source_image = pygame.transform.scale(self.source_image, (self.image_w, self.image_h))

        self.image = self.source_image
        self.rect = self.image.get_rect()

        # маска
        self.mask = pygame.mask.from_surface(self.image)

        # hp
        self.hp = hp

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

        # hp bar
        if bar_type == 'line':
            self.hp_bar = HpBar(self, hp_bars)
        else:
            self.hp_bar = PlayerBar(self, hp_bars)

    def get_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
            self.hp_bar.kill()

    def collision(self, groups):
        for group in groups:
            for sprite in group:
                if pygame.sprite.collide_mask(self, sprite):
                    dmg1 = sprite.collision_dmg
                    dmg2 = self.collision_dmg

                    self.get_damage(dmg1)
                    sprite.get_damage(dmg2)

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

    def update(self, *args):
        time = args[0]
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
        self.collision([enemy_bullets, obstacles, enemies])

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
    def update(self, *args):
        time = args[0]
        spaceship = args[1]
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

        self.hp_bar.set_coords(self.x, self.y)

        self.collision([player_bullets, obstacles])