from src.background import Background
from src.clock_item import Clock_item
from src.data import *
from src.pipes import Pipes
from src.ship import Ship


class Play_game:
    username = None

    def __init__(self, screen, username, solo=True, is_left=True):
        self.end_game = False
        self.username = username
        self.screen = screen
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.is_left = is_left
        self.solo = solo

        x_origin = 0
        if not (solo and is_left):
            x_origin = self.screenWidth / 2

        self.game_window_width = self.screenWidth if self.solo else self.screenWidth / 2
        self.game_window_height = self.screenHeight

        self.game_window = pygame.Surface((self.game_window_width, self.game_window_height))

        self.rect = self.game_window.get_rect(left=x_origin)

        self.ship = Ship(self.game_window, single_player=solo)
        self.pipes = []
        self.pipes_number = 2 if solo else 1
        for i in range(0, self.pipes_number):
            self.pipes.append(Pipes(self.game_window, first=True if (i == 0) else False))
        self.bg = Background(self.game_window)
        self.clock = Clock_item(self.game_window)

        self.game_objects = {"ship": self.ship, "pipes": self.pipes, "bg": self.bg, "clock": self.clock}

        if is_left:
            self.jump_key = pygame.K_SPACE
        else:
            self.jump_key = pygame.K_RETURN

    def draw(self):
        self.screen.blit(self.game_window, self.rect)

        self.bg.draw()
        self.ship.draw()
        for pipe in self.pipes:
            pipe.draw()
        self.clock.draw()

        text_font = pygame.font.Font(font["bradbunr"], 25)

        string1 = "Score {0} : {1}".format(self.username, self.game_objects["ship"].score)
        textSurface, textRect = createTextObj(string1, text_font)
        self.game_window.blit(textSurface, textRect)

        if not self.solo:
            x_rect_split = self.game_window_width if self.is_left else 0
            pygame.draw.rect(self.game_window, colors["black"], (x_rect_split, 0, 2, self.game_window_height))

    def update(self):
        if self.ship.y_pos + self.ship.height > self.game_window_height:  # Ship falls
            self.end_game = True
        self.ship.move()

        if not self.ship.goForward:
            self.bg.move()
            self.clock.move()
            for pipe in self.pipes:
                pipe.move()

        self.updateScore()

        if self.ship.collision_pipes(self.pipes):
            self.end_game = True
        if self.ship.collision_clock(self.clock):
            sounds["slow"].play()
            self.clock.respawn()
            for pipe in self.pipes:
                pipe.velocity = pipe.origin_velocity
            self.bg.velocity = self.bg.origin_velocity
            self.clock.velocity = self.clock.origin_x_velocity

    def updateScore(self):
        for pipe in self.pipes:
            if self.ship.x_pos > pipe.x_pos and not pipe.passed:
                self.ship.score += 1
                sounds["score"].play()
                if pipe.velocity < 13:
                    for pipe_2 in self.pipes:
                        pipe_2.velocity += 0.5
                    self.clock.velocity += 0.5

                if self.bg.velocity < 4:
                    self.bg.velocity += 0.2

                if pipe.space > 230 and self.ship.score % 2 != 0:
                    pipe.space -= 5

                pipe.passed = True

                if self.ship.score % 4 == 0 and self.ship.score != 0:
                    self.clock.start()

    def reset(self):
        self.ship.reset()
        self.bg.reset()
        self.clock.reset()
        for pipe in self.pipes:
            pipe.reset()

