from src.data import *
from random import randint, choice
from src.game_object import Game_object


class Clock_item(Game_object):
    origin_x_velocity = 7.5
    direction = [-1, 1]
    origin_y_velocity = 1 * choice(direction)

    def __init__(self, screen):
        self.screen = screen
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()

        self.up_pos_max = 30
        self.low_pos_max = self.screenHeight - 30

        self.image = images["clock"]
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.size

        self.start_point = self.screenWidth + self.width + images["pipe_down"].get_rect().size[0]

        self.x_pos = self.start_point
        self.y_pos = self.screenHeight / 2 - self.height  # randint(self.up_pos_max, self.low_pos_max)
        self.velocity = self.origin_x_velocity
        self.y_velocity = self.origin_y_velocity
        self.appears = False

    def move(self):
        if self.appears:
            self.x_pos -= self.velocity
            self.y_pos -= self.y_velocity
        if self.x_pos == -self.width:
            self.appears = False
        if self.x_pos < -self.width:
            self.respawn()
        if self.y_pos < self.up_pos_max:
            self.velocity *= -1
        if self.y_pos > self.low_pos_max:
            self.velocity *= -1

    def draw(self):
        if self.appears:
            self.screen.blit(self.image, (self.x_pos, self.y_pos))

    def respawn(self):
        self.x_pos = self.start_point
        self.y_pos = randint(self.up_pos_max, self.low_pos_max)
        self.appears = False

    def start(self):
        self.appears = True
