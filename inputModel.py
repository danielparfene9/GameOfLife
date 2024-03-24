import pygame
import pygame as pg
from constants import GRAY, BLACK


class InputModel:
    def __init__(self, screen, x, y, w, h, text_color, box_color):
        self.screen = screen
        self.text_color = GRAY
        self.box_color = GRAY
        self.input_rect = pg.Rect(x, y, w, h)
        self.active = False
        self.base_font = pg.font.Font(None, 32)
        self.user_text = ''

        if box_color:
            self.active_box_color = box_color
        else:
            self.active_box_color = BLACK

        if text_color:
            self.active_text_color = text_color
        else:
            self.active_text_color = BLACK

    def draw(self):
        if self.active:
            self.text_color = self.active_text_color
            self.box_color = self.active_box_color
        else:
            self.text_color = GRAY
            self.box_color = GRAY

        pg.draw.rect(self.screen, self.box_color, self.input_rect, 2)
        text_surface = self.base_font.render(self.user_text, True, self.text_color)
        self.screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+5))

        self.input_rect.w = max(text_surface.get_width()+10, 100)

    def changeText(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else:
                self.user_text += event.unicode

    def isPressed(self, event):
        if self.input_rect.collidepoint(event.pos):
            self.active = True

