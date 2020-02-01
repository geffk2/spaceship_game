from constants import *
from load_image import load_image
from random import choice


class Camera:
    def __init__(self, obj):
        self.obj = obj
        self.focus_state = False

        self.timer_start = False
        self.double_click_timer = 0

        self.focus()

    def apply(self, obj):
        if stars_background in obj.groups():
            obj.x += self.dx / 10
            obj.y += self.dy / 10
        else:
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


def background_init():
    for i in range(25):
        Star()
    AnimatedStar()


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(stars_background)
        image = load_image(f'stars\\star_type{choice(range(1, 7))}.jpg', -1)
        self.image = pygame.transform.scale(image, (35, 35))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        collide_with_stars = True

        while collide_with_stars:
            self.rect.x, self.rect.y = choice(range(WIDTH)), choice(range(HEIGHT))
            collide_with_stars = False
            for sprite in stars_background:
                if sprite != self and pygame.sprite.collide_mask(self, sprite):
                    collide_with_stars = True

        self.x, self.y = self.rect.x, self.rect.y

    def update(self, *args):
        self.x %= WIDTH + 100
        self.y %= HEIGHT + 100

        self.rect.x, self.rect.y = self.x, self.y


class AnimatedStar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(stars_background)
        self.frames = []
        self.cut_sheet(load_image(f'stars\\shining_star_v2.jpg', -1), 5, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(choice(range(WIDTH)), choice(range(HEIGHT)))

        self.x, self.y = 0, 0

        self.timer = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        self.timer += args[0]
        if self.timer > 0.1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.timer = 0

            if self.cur_frame == 0:
                self.rect.x = choice(range(WIDTH))
                self.rect.y = choice(range(HEIGHT))
