from load_image import load_image
import pygame


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, coords, sprite, group, max_speed=10, max_acceleration=5, direction=0):
        super().__init__(group)
        self.image = load_image(sprite, -1)
        self.image = pygame.transform.scale(self.image, (86, 64))
        self.rect = self.image.get_rect()

        # дробные координаты
        self.x = coords[0]
        self.y = coords[1]

        # целочисленные координаты
        self.rect.x = self.x
        self.rect.y = self.y

        # начальная и максимальная скорости
        self.speed = [0, 0]
        self.max_speed = max_speed

        # начальное и максимальное ускорение
        self.acceleration = [0, 0]
        self.max_acceleration = max_acceleration
        self.direction = direction

        # торможение
        self.deceleration = False

        self.hp = 100

    def update(self, time):
        # обновление координат
        self.x += self.speed[0] + self.acceleration[0] * (time ** 2) / 2
        self.y += self.speed[1] + self.acceleration[1] * (time ** 2) / 2

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # обновление скоростей
        self.speed[0] += self.acceleration[0] * time
        self.speed[1] += self.acceleration[1] * time

        self.speed[0] = min(self.max_speed, self.speed[0])
        self.speed[1] = min(self.max_speed, self.speed[1])

        if self.deceleration:
            if abs(self.speed[0] / self.max_speed) <= 0.001:
                self.speed[0] = 0
            if abs(self.speed[1] / self.max_speed) <= 0.001:
                self.speed[1] = 0

        '''if pygame.sprite.spritecollideany(self, obstacles):
            self.get_damage(self.hp)

        if pygame.sprite.spritecollideany(self, enemy_bullets):
            self.get_damage(10)'''

    def update_acceleration(self, new_prop):
        # new prop like [-1, 1] or [0, 1]
        # 1 - ускорение по оси
        # 0 - нет ускорения
        # -1 - против оси
        self.acceleration = [self.max_acceleration * new_prop[0],
                             self.max_acceleration * new_prop[1]]

        if new_prop == [0, 0]:
            x_d = 1 if self.speed[0] > 0 else -1
            if self.speed[0] == 0:
                x_d = 0

            y_d = 1 if self.speed[1] > 0 else -1
            if self.speed[1] == 0:
                y_d = 0

            self.acceleration = [-self.max_speed * x_d * 10, -self.max_speed * y_d * 10]
            self.deceleration = True
        else:
            self.deceleration = False

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
    w, h = 1024, 1024
    screen = pygame.display.set_mode((w, h))

    # group
    all_sprites = pygame.sprite.Group()

    # spaceship
    spaceship = Spaceship([50, 50], 'falcon.png', all_sprites)

    # clock
    clock = pygame.time.Clock()

    # событие движения
    MOTION = 30
    pygame.time.set_timer(MOTION, 40)

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOTION:

                states = pygame.key.get_pressed()
                new_properties = [0, 0]

                if states[pygame.K_UP]:
                    new_properties[1] = -1
                elif states[pygame.K_DOWN]:
                    new_properties[1] = 1
                if states[pygame.K_LEFT]:
                    new_properties[0] = -1
                elif states[pygame.K_RIGHT]:
                    new_properties[0] = 1

                spaceship.update_acceleration(new_properties)

        all_sprites.update(clock.tick() / 10000)
        all_sprites.draw(screen)
        pygame.display.flip()

