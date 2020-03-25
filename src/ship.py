from src.data import *
from src.game_object import Game_object


class Ship(Game_object):
    origin_x_velocity = 4
    origin_y_velocity = -10

    def __init__(self, screen, single_player=True):
        self.screen = screen
        self.screenHeight = pygame.display.get_surface().get_size()[1]
        self.image = images["ship"]
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.size
        self.spriteJump = spriteShipJump
        self.spriteFall = spriteShipFall
        self.x_pos = -self.width
        self.y_pos = self.screenHeight / 2 - self.height
        self.isJump = False
        self.velocity = self.origin_y_velocity
        self.x_velocity = self.origin_x_velocity
        self.max_pos_y = maxPosShip
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

    def move(self):
        neg = -1
        if self.goForward:
            self.x_pos += self.x_velocity

        if self.x_pos > 150 and self.goForward:
            self.goForward = False

        if self.velocity > 0:
            self.isJump = False
            neg = 1

        self.y_pos += (self.velocity ** 2) * neg / 15
        self.velocity += 0.5

    def jump(self):
        self.isJump = True
        self.velocity = -13.5
        sounds["jump"].play()

    def collision_pipes(self, pipes_list):
        result = False
        for pipe in pipes_list:
            if self.x_pos + self.width > pipe.x_pos and self.x_pos < pipe.x_pos + pipe.width:  # ship between pipes (up and down)
                if self.y_pos < pipe.y_pos_up + pipe.height:  # collide with top
                    result = True
                    break
                elif self.y_pos + self.height > pipe.y_pos_down:  # collide with bottom
                    result = True
                    break
        return result

    def collision_clock(self, clock):
        result = False
        if self.x_pos + self.width >= clock.x_pos and self.x_pos < clock.x_pos + clock.width:  # x collapse
            if self.y_pos < clock.y_pos + clock.height and self.y_pos + self.height > clock.y_pos:  # y collapse top ship
                result = True
            elif self.y_pos + self.height > clock.y_pos and self.y_pos < clock.y_pos + clock.height:  # y collapse bottom ship
                result = True
        return result
