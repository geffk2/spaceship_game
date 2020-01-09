from load_image import load_image
import pygame
from math import sin, cos, pi
from numpy import arctan2


PLAYER_SPRITE = 'falcon.png'
BULLET_SPRITE = 'bullet.png'
OBSTACLES_SPRITE = 'rock.png'


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, max_speed=100, max_acceleration=50, direction=0):
        super().__init__(group, all_sprites)

        self.image_w, self.image_h = 100, 100

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

    def shoot(self, group, player_pos=None):
        bullet = Bullet([self.x, self.y], BULLET_SPRITE, group, self.direction)

    def get_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, direction, dmg=10, speed=500):
        super().__init__(group, all_sprites)

        self.image = pygame.transform.rotate(load_image(sprite, -1), 360 - 180 * direction / pi)
        self.rect = self.image.get_rect()

        self.direction = direction

        self.x = coords[0]
        self.y = coords[1]

        # координаты изображения
        self.rect.x = int(coords[0])
        self.rect.y = int(coords[1])

        self.dmg = dmg
        self.speed = speed

    def update(self, time):
        self.x += cos(self.direction) * time * self.speed
        self.y += sin(self.direction) * time * self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if not self.rect.colliderect(screen_rect):
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, size_w=50):
        super().__init__(group, all_sprites)

        self.image = load_image(sprite, -1)

        img_w, img_h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,
                                            (size_w, img_h * size_w // img_h))

        self.rect = self.image.get_rect()

        self.rect.x = int(coords[0])
        self.rect.y = int(coords[1])


class Camera:
    pass


if __name__ == '__main__':

    pygame.init()
    w, h = 512, 512
    screen = pygame.display.set_mode((w, h))

    # groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()

    # test obstacles
    obs_1 = Obstacle((10, 10), OBSTACLES_SPRITE, obstacles)
    obs_2 = Obstacle((150, 150), OBSTACLES_SPRITE, obstacles, size_w=100)

    # player spaceship
    spaceship = Spaceship([256, 256], PLAYER_SPRITE, all_sprites)

    # screen rect obj
    screen_rect = (0, 0, w, h)

    # clock
    clock = pygame.time.Clock()

    # событие движения
    MOTION = 30
    pygame.time.set_timer(MOTION, 5)

    # кд выстрела игрока
    PLAYER_SHOOT_KD = 100
    shoot_timer = 0

    running = True
    while running:
        screen.fill((255, 255, 255))

        # acceleration properties
        new_properties = 0

        states = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == MOTION:
                if states[pygame.K_LCTRL]:
                    new_properties = -1
                elif states[pygame.K_LSHIFT]:
                    new_properties = 1

                spaceship.update_acceleration(new_properties)

            if (event.type == pygame.KEYUP and event.key == pygame.K_SPACE) \
                    or states[pygame.K_SPACE]:
                if shoot_timer >= PLAYER_SHOOT_KD:
                    shoot_timer = 0
                    spaceship.shoot(player_bullets)

            if event.type == pygame.MOUSEMOTION:
                spaceship.update_direction(event.pos)

        t = clock.tick()
        shoot_timer += t

        all_sprites.update(t / 1000)
        all_sprites.draw(screen)
        pygame.display.flip()

