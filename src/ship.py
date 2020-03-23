from src.data import *


class Ship:

    def __init__(self, screen, screenHeight, screenOverlay):
        self.width = 400 / 5
        self.height = 480 / 5
        self.image = images["ship"]
        self.spriteJump = spriteShipJump
        self.spriteFall = spriteShipFall
        self.x_pos = -self.width
        self.y_pos = screenHeight / 2 - self.height
        self.screen = screen
        self.isJump = False
        self.velocity = -10
        self.x_velocity = 4
        self.screenHeight = screenHeight
        self.screenOverlay = screenOverlay
        self.score = 0
        self.spriteCount = 0
        self.goForward = True

    def draw(self):
        if self.spriteCount + 1 >= 24:
            self.spriteCount = 0
        if self.isJump:
            self.screen.blit(self.spriteJump[self.spriteCount // 6], (self.x_pos, self.y_pos))
        else:
            self.screen.blit(self.spriteFall[self.spriteCount // 6], (self.x_pos, self.y_pos))
        self.spriteCount += 1

    def jump(self):
        self.isJump = True
        self.velocity = -13.5
        sounds["jump"].play()

    def move(self):

        if self.goForward:
            self.x_pos += self.x_velocity

        if self.x_pos > 200 and self.goForward:
            self.goForward = False

        neg = -1
        if self.velocity > 0:
            self.isJump = False
            neg = 1
        self.y_pos += (self.velocity ** 2) * neg / 15
        self.velocity += 0.5
