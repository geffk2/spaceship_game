import pygame
from spaceships import PlayerShip, BossShip
from other_stuff import BackgroundTile, Bullet
import sys
import os

FPS = 60

pygame.init()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()


width, height = size = 800, 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
player = PlayerShip(player_group, (100, 100), (67, 50))
boss = BossShip(boss_group, (200, 200), (384, 696), player)

BackgroundTile(tiles_group, (-100, -100))


def render():
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    bullets_group.draw(screen)
    player_group.draw(screen)
    boss_group.draw(screen)


pygame.time.set_timer(30, 10)
pygame.time.set_timer(31, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == 30:
            player_group.update()
            bullets_group.update()
        if event.type == 31:
            boss_group.update(player_group)
    render()
    pygame.display.flip()
