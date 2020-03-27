from random import randint

from src.data import *
from src.game_object import Game_object


class Pipes(Game_object):
    origin_space = 300
    origin_velocity = 7.5
    max_pos = -570
    min_pos = -220

    def __init__(self, screen, first=True, single_player=True):
        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_rect().size

        self.image = {"up": images["pipe_up"], "down": images["pipe_down"]}
        self.rect = self.image["up"].get_rect()
        self.width, self.height = self.rect.size

        self.first = first
        self.single_player = single_player

        self.space = self.origin_space
        self.space_next_pipes = (self.screenWidth / 2) + self.width
        self.start_point = self.screenWidth - self.width

        if first:
            self.x_pos = self.start_point
        else:
            self.x_pos = self.start_point + self.space_next_pipes
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.velocity = self.origin_velocity
        self.passed = False

    def move(self):
        self.x_pos -= self.velocity
        if self.x_pos < -self.width:
            self.updateCoordinates()

    def draw(self):
        self.screen.blit(self.image["up"], (self.x_pos, self.y_pos_up))
        self.screen.blit(self.image["down"], (self.x_pos, self.y_pos_down))

    def reset(self):
        self.space = self.origin_space
        if self.first:
            self.x_pos = self.start_point
        else:
            self.x_pos = self.start_point + self.space_next_pipes
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.velocity = self.origin_velocity
        self.passed = False

    def updateCoordinates(self):
        self.x_pos = self.screenWidth + self.width
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.passed = False
