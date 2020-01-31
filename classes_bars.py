from constants import *
from math import pi
import pygame


class HpBar(pygame.sprite.Sprite):
    def __init__(self, obj, group):
        super().__init__(group)

        self.max_hp = obj.hp
        self.image = pygame.Surface([HP_BARS_W, HP_BARS_H])
        self.image.fill(pygame.Color('green'))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = obj.rect.x, obj.rect.y - HP_BARS_H

        self.obj = obj
        self.size = obj.image_w, obj.image_h

    def update(self, *args):
        for col in range(HP_BARS_W):
            color = 'green' if col < HP_BARS_W * self.obj.hp / self.max_hp else 'red'
            for row in range(HP_BARS_H):
                self.image.set_at((col, row), pygame.Color(color))

    def set_coords(self, x, y):
        self.rect.x, self.rect.y = int(x), int(y - 5)


class PlayerBar(pygame.sprite.Sprite):
    def __init__(self, obj, group):
        super().__init__(group)

        self.max_hp = obj.hp

        r = PLAYER_HP_BAR_R
        self.image = pygame.Surface([2 * r, 2 * r])
        self.image.fill(pygame.Color(0, 0, 0))
        self.image.set_colorkey(self.image.get_at((0, 0)))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH - 100, HEIGHT - 100
        self.x, self.y = self.rect.x, self.rect.y

        self.obj = obj
        self.r = r

        self.font = pygame.font.Font('data/StarJedi.ttf', 20)
        self.w, self.h = self.font.size('123')

    def update(self, *args, text=None):
        self.image.fill(pygame.Color(0, 0, 0))

        div = self.obj.hp / self.max_hp
        pygame.draw.arc(self.image, pygame.Color('red'),
                        (0, 0, 2 * self.r, 2 * self.r),
                        pi / 2, pi / 2 + 2 * pi * div,
                        7)

        self.w, self.h = self.font.size(f'{int(div * 100)}')
        text = self.font.render(f'{int(div * 100)}', 1, (255, 0, 0))
        self.w, self.h = self.font.size(f'{int(div * 100)}')
        self.image.blit(text, (self.r - self.w // 2, self.r - self.h // 2))


class BossBar(pygame.sprite.Sprite):
    def __init__(self, obj, group):
        super().__init__(group)
        self.max_hp = obj.hp

        self.image = pygame.Surface([BOSS_BAR_W * WIDTH, BOSS_BAR_H])
        self.image.fill(pygame.Color('black'))
        self.image.set_colorkey(self.image.get_at((0, 0)))

        self.rect = self.image.get_rect()
        self.rect.y = BOSS_BAR_H
        self.rect.x = (WIDTH - BOSS_BAR_W * WIDTH) / 2
        self.obj = obj

        self.size = self.rect.w, self.rect.h

    def update(self, *args):
        self.image.fill(pygame.Color('black'))
        pygame.draw.rect(self.image, pygame.Color('red'), [0, 0, self.size[0] * self.obj.hp // self.max_hp, BOSS_BAR_H // 2])
        pygame.draw.rect(self.image, pygame.Color('blue'), [0, BOSS_BAR_H // 2, self.size[0] * self.obj.shields //
                                                           self.obj.max_shields, BOSS_BAR_H // 2])

        pygame.draw.rect(self.image, pygame.Color('white'), [0, 0, *self.size], 2)

