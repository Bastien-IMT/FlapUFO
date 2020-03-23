from src.data import *


class Background:

    def __init__(self, screen, screenHeight, screenWidth):
        self.image = images["bg_large"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.screen = screen
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.x_pos1 = 0
        self.x_pos2 = self.x_pos1 + self.width
        self.y_pos = -50
        self.velocity = 0.7

    def move(self):
        self.x_pos1 -= self.velocity
        if self.x_pos1 < -self.width:
            self.x_pos1 = self.x_pos2 + self.width

        self.x_pos2 -= self.velocity
        if self.x_pos2 < -self.width:
            self.x_pos2 = self.x_pos1 + self.width

    def draw(self):
        self.screen.blit(self.image, (self.x_pos1, self.y_pos))
        self.screen.blit(self.image, (self.x_pos2, self.y_pos))