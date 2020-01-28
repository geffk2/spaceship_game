import pygame
import math
import random
from load_image import load_image


class BackgroundTile(pygame.sprite.Sprite):
    def __init__(self, group, coordinates):
        super().__init__(group)
        self.image = load_image('background_v2.png')
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = coordinates


class Bullet(pygame.sprite.Sprite):
    velocity = 15

    def __init__(self, group, bullet_type, coordinates, angle):
        super().__init__(group)
        self.image = load_image('shot.png' if bullet_type == 0 else 'shot1.png', -1, size=(10, 3))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordinates
        self.angle = angle + (random.random() - 0.5) * 2 * (5 / 180) * math.pi
        self.image = pygame.transform.rotate(self.image, self.angle * 180 / math.pi)

    def update(self):
        self.rect.x -= self.velocity * math.cos(self.angle)
        self.rect.y -= self.velocity * math.sin(self.angle)
