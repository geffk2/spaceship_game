import pygame
import os


def load_image(name, color_key=None, size=None):
    fullname = os.path.join(os.path.dirname(__file__) + '\\data', name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    if size is not None:
        image = pygame.transform.scale(image, size)

    return image
