import pygame
import pygame as pg
from constants import GRAY, BLACK, height


class InputModel:
    def __init__(self, screen, x, y, w, h, text_color, box_color):
        self.screen = screen
        self.text_color = GRAY
        self.box_color = GRAY
        self.w = w
        self.input_rect = pg.Rect(x, y, w, h)
        self.active = False
        self.base_font = pg.font.Font('images/Montserrat-Medium.ttf', 20)
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

        self.screen.blit(self.base_font.render("Nr of generation:", True, BLACK), (self.input_rect.x-200, self.input_rect.y+15))
        pg.draw.rect(self.screen, self.box_color, self.input_rect, 2)
        text_surface = self.base_font.render(self.user_text, True, self.text_color)
        self.screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+15))

        self.input_rect.w = max(text_surface.get_width()+10, self.w)

    def changeText(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                               pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                self.user_text += event.unicode

    def isPressed(self, event):
        if self.input_rect.collidepoint(event.pos):
            self.active = True
        else:
            self.active = False

    def print_current(self, gen):
        self.screen.blit(self.base_font.render("Current generation:", True, BLACK),
                         (self.input_rect.x-240, self.input_rect.y - height/7))

        self.screen.blit(self.base_font.render(gen, True, BLACK),
                         (self.input_rect.x, self.input_rect.y - height/7))
