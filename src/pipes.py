from random import randint

from src.data import *
from src.gameobject import GameObject


class Pipes(GameObject, pygame.sprite.Sprite):
    """
    Class that defines all_pipes that the character has to pass threw.
    """
    origin_space = 300
    origin_velocity = 7.5
    max_pos = -570
    min_pos = -220

    def __init__(self, PlayGame, first: bool = True):
        """
        Initialize all_pipes object (= top pipe + bottom pipe).
        :param PlayGame: PlayGame object
        :param first: bool if this pipe is the first that must appear on the screen
        """

        super().__init__()

        self.game = PlayGame

        # display settings
        self.screen = PlayGame.game_window
        self.screenWidth, self.screenHeight = self.screen.get_rect().size
        self.image = {"up": images["pipe_up1"], "down": images["pipe_down1"]} if PlayGame.is_left else {
            "up": images["pipe_up2"],
            "down": images[
                "pipe_down2"]}
        self.rect = self.image["up"].get_rect()
        self.width, self.height = self.image["up"].get_rect().size

        # internal settings to make it run
        self.passed = False
        self.first = first
        self.single_player = PlayGame.solo

        # position settings
        self.space = self.origin_space
        self.space_next_pipes = (self.screenWidth / 2) + self.width
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.velocity = self.origin_velocity
        self.start_point = self.screenWidth - self.width
        if self.first:
            self.x_pos = self.start_point
        else:
            self.x_pos = self.start_point + self.space_next_pipes

    def move(self):
        """
        Make all_pipes move.
        """
        self.x_pos -= self.velocity
        if self.x_pos < -self.width:
            self.updateCoordinates()

    def draw(self):
        """
        Draw all_pipes on game window.
        """
        self.screen.blit(self.image["up"], (self.x_pos, self.y_pos_up))
        self.screen.blit(self.image["down"], (self.x_pos, self.y_pos_down))

    def reset(self):
        """
        Reset some attributes to start a new game.
        """
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
        """
        Update coordinates when all_pipes cross the screen and need to start again.
        """
        self.x_pos = self.screenWidth + self.width
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.passed = False
