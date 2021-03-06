import pygame
from load_image import load_image
from constants import player_bullets, enemy_bullets


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, size_w=50,
                 collision_dmg=50):
        super().__init__(group)

        self.image = load_image(sprite, -1)
        self.collision_dmg = collision_dmg
        self.hp = collision_dmg

        img_w, img_h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,
                                            (size_w, img_h * size_w // img_h))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.x, self.y = coords
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self, *args):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.bullet_collision()

    def bullet_collision(self):
        for sprite in player_bullets:
            if pygame.sprite.collide_mask(self, sprite):
                sprite.kill()

        for sprite in enemy_bullets:
            if pygame.sprite.collide_mask(self, sprite):
                sprite.kill()

    def get_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
