import pygame
from load_image import load_image
from math import pi
from constants import *
from math import sin, cos


class Bullet(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, direction,
                 dmg=10, speed=500):
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

        # у каждого объекта есть хп, при ударе от хп
        # отнимется урон противника
        self.collision_dmg = dmg
        self.hp = dmg

        self.speed = speed

    def update(self, *args):
        time = args[0]
        self.x += cos(self.direction) * time * self.speed
        self.y += sin(self.direction) * time * self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()

    def get_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
