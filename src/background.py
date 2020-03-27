from src.data import *
from src.game_object import Game_object


class Background(Game_object):

    offset_y = -50
    origin_velocity = 0.7

    def __init__(self, screen):
        self.image = images["bg_large"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.screen = screen
        self.screenHeight, self.screenWidth = pygame.display.get_surface().get_size()
        self.x_pos1 = 0
        self.x_pos2 = self.x_pos1 + self.width
        self.y_pos = self.offset_y
        self.velocity = self.origin_velocity

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

    def reset(self):
        self.x_pos1 = 0
        self.x_pos2 = self.x_pos1 + self.width
        self.y_pos = self.offset_y
        self.velocity = self.origin_velocity