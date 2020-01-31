import pygame
from constants import MAP_RENDER, MAP_R,\
    MAP_X, MAP_Y


class Minimap(pygame.sprite.Sprite):
    def __init__(self, player, group, vision_r):
        super().__init__(group)
        self.px, self.py = player.x, player.y
        self.player = player
        self.vision_r = vision_r

        self.image = pygame.Surface([2 * MAP_R, 2 * MAP_R])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = MAP_X, MAP_Y

        self.x, self.y = 0, 0

    def update(self, *args):
        self.image.fill(pygame.Color(0, 0, 0))

        pygame.draw.circle(self.image, pygame.Color('white'),
                        [MAP_R, MAP_R], MAP_R, 7)

        for group in MAP_RENDER:
            for sprite in group:
                dx = self.px - sprite.x
                dy = self.py - sprite.y

                if (dx ** 2 + dy ** 2) ** 0.5:
                    pass
