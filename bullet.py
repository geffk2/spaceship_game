from load_image import load_image
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, sprite, group, coords):
        super().__init__(group)
        self.image = load_image(sprite, -1)
        self.rect = self.image.get_rect()
        self.direction = direction

        # дробные координаты
        self.x = coords[0]
        self.y = coords[1]

        # целочисленные координаты
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, time):
        self.x += self.direction[0] * time
        self.y += self.direction[1] * time

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
