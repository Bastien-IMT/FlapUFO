from src.background import Background
from src.data import *
from src.pipes import Pipes
from src.ship import Ship


class Game_split_screen:
    clock = pygame.time.Clock()

    def __init__(self, screen, username, is_left):
        self.username = username
        self.screen = screen
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()

        self.split_screen = pygame.Surface((self.screenWidth / 2, self.screenHeight))
        self.rect = self.screen.get_rect(left=0 if is_left else self.screenWidth / 2)

        self.ship = Ship(self.split_screen, single_player=False)
        self.pipes = Pipes(self.split_screen, first=True)
        self.bg = Background(self.split_screen)

        self.game_objects = {"ship": self.ship, "pipes": self.pipes, "bg": self.bg}

    def createTextObj(self, text, font):
        textSurface = font.render(text, True, colors["white"])
        return textSurface, textSurface.get_rect()

    def draw_split_screen(self):
        self.screen.blit(self.split_screen, self.rect)

        # for object in self.game_objects.values():
        #     object.draw()

        self.bg.draw()
        self.ship.draw()
        self.pipes.draw()

        text = pygame.font.Font(font["bradbunr"], 25)

        string = "Score {0} : {1}".format(self.username, self.game_objects["ship"].score)
        textSurface, textRect = self.createTextObj(string, text)
        self.split_screen.blit(textSurface, textRect)

        pygame.display.update()
        self.clock.tick(120)
