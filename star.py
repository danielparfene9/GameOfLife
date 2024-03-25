import pygame as pg


class Star:
    def __init__(self, screen, color, x, y, w, h):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.image.load("images/star.svg")
        self.image = pg.transform.scale(self.image, (self.w, self.h))
        self.image_rect = self.image.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

    def draw(self):
        # pg.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))
        self.screen.blit(self.image, self.image_rect)
