import pygame
from constants import *
from load_image import load_image


class Camera:
    def __init__(self, obj):
        self.obj = obj
        self.focus_state = False

        self.timer_start = False
        self.double_click_timer = 0

        self.focus()

    def apply(self, obj):
        obj.x += self.dx
        obj.y += self.dy

    def update(self, time):
        if self.timer_start:
            self.double_click_timer += time

        if self.focus_state:
            self.focus()
        else:
            self.dx = 0
            self.dy = 0

    def pressed(self):
        if self.timer_start:
            if self.double_click_timer <= DOUBLE_CLICK_S:
                self.focus_state = not self.focus_state
                self.timer_start = False
            self.double_click_timer = 0
        else:
            self.timer_start = True
        self.focus()

    def focus(self):
        self.dx = WIDTH / 2 - self.obj.x
        self.dy = HEIGHT / 2 - self.obj.y


class Background(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        image = load_image(BACKGROUND)
        w, h = image.get_size()
        self.image = pygame.transform.scale(image, (WIDTH, WIDTH * h // w))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.x, self.y = 0, 0
