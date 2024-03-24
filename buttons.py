import math

import pygame


class Button:
    def __init__(self, screen, color, x, y, tipe, radius):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.tipe = tipe
        if radius:
            self.radius = radius
        else:
            self.radius = 10

    def button(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, (0, 0, 0), (self.x, self.y), self.radius, width=4)
        self.switch(self.tipe)

    def isPressed(self, x, y):
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance <= self.radius

    def next(self):
        image = pygame.image.load("images/next.svg")
        image_size = int(self.radius)  #
        image = pygame.transform.scale(image, (image_size, image_size))
        image_rect = image.get_rect(center=(self.x, self.y))
        self.screen.blit(image, image_rect)

    def previous(self):
        image = pygame.image.load("images/next.svg")
        image_size = int(self.radius)  #
        image = pygame.transform.scale(image, (image_size, image_size))
        image = pygame.transform.flip(image, True, False)
        image_rect = image.get_rect(center=(self.x, self.y))
        self.screen.blit(image, image_rect)

    def stop(self):
        image = pygame.image.load("images/stop.svg")
        image_size = int(self.radius)
        image = pygame.transform.scale(image, (image_size, image_size))
        image_rect = image.get_rect(center=(self.x, self.y))
        self.screen.blit(image, image_rect)

    def play(self):
        image = pygame.image.load("images/play.svg")
        image_size = int(self.radius)
        image = pygame.transform.scale(image, (image_size, image_size))
        image_rect = image.get_rect(center=(self.x, self.y))
        self.screen.blit(image, image_rect)

    def switch(self, type):
        if type == "next":
            self.next()
        elif type == "previous":
            self.previous()
        elif type == "stop":
            self.stop()
        elif type == "play":
            self.play()

    def __str__(self):
        return f"Button at ({self.x}, {self.y}) with radius {self.radius} and type '{self.tipe}'"
