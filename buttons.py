import pygame


class Button:
    def __init__(self, x, y, w, h, text, col, txt_col=(255, 255, 255)):
        self.x = x
        self.y = y
        self.col = col
        self.txt_col = txt_col

        self.w = w
        self.h = h

        self.text = text

    def draw(self, scr):
        pygame.draw.rect(scr, self.col, [self.x, self.y, self.w, self.h])

        font = pygame.font.Font('data/StarJedi.ttf', 36)
        text = font.render(self.text, 1, self.txt_col)

        x = self.x + (self.w - text.get_width()) // 2
        y = self.y + (self.h - text.get_height()) // 2

        scr.blit(text, (x, y))

    def is_selected(self, pos):
        return self.x <= pos[0] <= self.x + self.w and \
               self.y <= pos[1] <= self.y + self.h
