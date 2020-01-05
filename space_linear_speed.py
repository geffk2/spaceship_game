from load_image import load_image
import pygame
from math import sin, cos, pi
from numpy import arctan2


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, max_speed=100, max_acceleration=50, direction=0):
        super().__init__(group)

        self.image_w, self.image_h = 60, 60

        # исходное изображение для того, чтобы не затирать методом rotate (up_d) картинку
        self.source_image = load_image(sprite, -1)
        self.source_image = pygame.transform.scale(self.source_image, (self.image_w, self.image_h))

        self.image = self.source_image
        self.rect = self.image.get_rect()

        # hp
        self.hp = 100

        # целочисленные координаты верхнего левого края
        self.rect.x = int(coords[0])
        self.rect.y = int(coords[1])

        # дробные координаты центра
        self.x = coords[0] + self.image_w / 2
        self.y = coords[1] + self.image_h / 2

        # начальная и максимальная скорости
        self.speed = 0
        self.max_speed = max_speed

        # начальное и максимальное ускорение
        self.acceleration = 0
        self.max_acceleration = max_acceleration

        # направление движения
        self.direction = direction

    def update(self, time):
        # обновление координат
        self.x += (self.speed * time + self.acceleration * (time ** 2) / 2) * cos(self.direction)
        self.y += (self.speed * time + self.acceleration * (time ** 2) / 2) * sin(self.direction)

        self.rect.x = int(self.x - self.image_w / 2)
        self.rect.y = int(self.y - self.image_h / 2)

        # обновление скорости
        self.speed += self.acceleration * time
        self.speed = min(self.max_speed, self.speed)

        if self.speed < 0:
            self.speed = 0

        '''if pygame.sprite.spritecollideany(self, obstacles):
            self.get_damage(self.hp)

        if pygame.sprite.spritecollideany(self, enemy_bullets):
            self.get_damage(10)'''

    def update_acceleration(self, prop):
        # обновление ускорения
        if prop == 1:
            self.acceleration = self.max_acceleration
        elif self.speed != 0:
            if prop == -1:
                self.acceleration = -2 * self.max_acceleration
            else:
                self.acceleration = -self.max_acceleration
        else:
            self.acceleration = 0

    def update_direction(self, view_point):
        dx, dy = view_point[0] - self.x,  view_point[1] - self.y
        self.direction = arctan2(dy, dx)

        # rotate image
        self.image = pygame.transform.rotate(self.source_image, 360 - 180 * self.direction / pi)

    def shoot(self, direction):
        pass

    def get_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        self.kill()


if __name__ == '__main__':

    pygame.init()
    w, h = 512, 512
    screen = pygame.display.set_mode((w, h))

    # group
    all_sprites = pygame.sprite.Group()

    # spaceship
    spaceship = Spaceship([256, 256], 'falcon.png', all_sprites)

    # clock
    clock = pygame.time.Clock()

    # событие движения
    MOTION = 30
    pygame.time.set_timer(MOTION, 40)

    running = True
    while running:
        screen.fill((255, 255, 255))

        # acceleration properties
        new_properties = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOTION:

                states = pygame.key.get_pressed()

                if states[pygame.K_LCTRL]:
                    new_properties = -1
                elif states[pygame.K_LSHIFT]:
                    new_properties = 1
                spaceship.update_acceleration(new_properties)

            if event.type == pygame.MOUSEMOTION:
                spaceship.update_direction(event.pos)

        all_sprites.update(clock.tick() / 1000)
        all_sprites.draw(screen)
        pygame.display.flip()

