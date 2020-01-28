import pygame
import math
from load_image import load_image
from other_stuff import Bullet


def dot_product(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dot_product(v, v))


def angle(v1, v2):
    return math.acos(dot_product(v1, v2) / (length(v1) * length(v2)))


class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, group, coordinates, size):
        super().__init__(group)
        self.image = load_image('falcon.png', -1, size)

        self.rect = self.image.get_rect()
        self.move(coordinates)

        self.center_coordinates = (self.rect.x + self.rect.w / 2,
                                   self.rect.y + self.rect.h / 2)

    def move(self, coordinates):
        self.rect.x, self.rect.y = coordinates

        self.center_coordinates = (self.rect.x + self.rect.w / 2,
                                   self.rect.y + self.rect.h / 2)


class BossShip(pygame.sprite.Sprite):
    def __init__(self, group, coordinates, size, player):
        super().__init__(group)
        self.image = load_image('star_destroyer2.png', -1, size)

        self.rect = self.image.get_rect()
        self.move(coordinates)
        self.center_coordinates = (self.rect.x + self.rect.w / 2,
                                   self.rect.y + self.rect.h / 2)

        self.player = player
        self.attack_timer = 0
        self.shields_timer = 0

        self.health = 5000  # placeholder
        self.max_health = 5000

        self.shields = 0
        self.max_shields = 1000

        self.healing_rate = 8
        self.damage = 30
        self.current_action = None

    def move(self, coordinates):
        self.rect.x, self.rect.y = coordinates
        self.center_coordinates = (self.rect.x + self.rect.w / 2,
                                   self.rect.y + self.rect.h / 2)

    def take_damage(self, damage):
        self.shields_timer = 0
        self.health -= damage
        self.die()

    def die(self):
        pass

    def attack(self, bullet_group):
        direction = [1, 1]
        direction[0] = self.center_coordinates[0] - self.player.center_coordinates[0]
        direction[1] = self.center_coordinates[1] - self.player.center_coordinates[1]
        vec2 = [1, 0]
        bullet_angle = angle(direction, vec2)
        Bullet(bullet_group, 1, (self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2), bullet_angle)

    def update(self, *args):
        self.attack_timer += 1
        self.shields_timer += 1
        if self.attack_timer == 20:
            self.attack_timer = 0
            self.current_action = ['attack_1', 2]
        if self.current_action is not None:
            if self.current_action[0] == 'attack_1':
                self.attack(args[0])
                self.current_action[1] -= 1

            if self.current_action[1] == 0:
                self.current_action = None

        if self.shields_timer > 40:
            self.restore_shields()

    def restore_shields(self):
        print('healin...', self.shields)
        self.shields += self.healing_rate
        if self.shields > self.max_shields:
            self.shields = self.max_shields
