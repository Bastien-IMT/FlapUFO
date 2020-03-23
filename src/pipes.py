from src.data import *
from random import randint


class Pipes:

    def __init__(self, screen, screenHeight, screenWidth, screenOverlay, space=300, first=True):
        self.width = 200
        self.height = 600
        self.min_pos = -220
        self.max_pos = -570
        self.start_point = screenWidth - self.width
        self.image = {"up": images["pipe_up"], "down": images["pipe_down"]}
        self.screen = screen
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.screenOverlay = screenOverlay
        self.space = space
        if first:
            self.x_pos = self.start_point
        else:
            self.x_pos = self.start_point + SCREEN_WIDTH / 2 + self.width
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.velocity = 7.5
        self.passed = False

    def move(self):
        self.x_pos -= self.velocity
        if self.x_pos < -self.width:
            self.updateCoordinates()

    def draw(self):
        self.screen.blit(self.image["up"], (self.x_pos, self.y_pos_up))
        self.screen.blit(self.image["down"], (self.x_pos, self.y_pos_down))

    def updateCoordinates(self):
        self.x_pos = self.screenWidth + self.width
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.passed = False
