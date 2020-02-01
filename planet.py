import pygame
from load_image import load_image


class Planet(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, image_w=300, image_h=300, collision_dmg=30):
        super().__init__(group)

        self.image_w, self.image_h = image_w, image_h
        self.collision_dmg = collision_dmg

        self.image = load_image(sprite, -1)
        self.image = pygame.transform.scale(self.image, (image_w, image_h))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.x, self.y = coords

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect.x, self.rect.y = self.x, self.y

    def get_damage(self, dmg):
        pass
