import os
import pickle

import lib.pygame_functions as pg_functions
from src.background import Background
from src.clock_item import Clock_item
from src.data import *
from src.pipes import Pipes
from src.ship import Ship


class Game:
    screenW = SCREEN_WIDTH
    screenH = SCREEN_HEIGHT
    pg_functions.screenSize(screenW, screenW)
    end_game = False
    username = None
    clock = pygame.time.Clock()
    all_scores = dict()

    def __init__(self):
        self.all_scores = self.getScore()
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((self.screenW, self.screenH))
        pygame.display.set_caption("FlapUFO")
        pygame.display.set_icon(images["icon"])
        pygame.mixer.music.play(-1, 25.3)

    def highScoreMenu(self):
        sorted_scores = sorted(self.all_scores.items(), key=lambda t: t[1], reverse=True)

        first = ["", 0]
        second = ["", 0]
        third = ["", 0]

        if len(sorted_scores) > 0:
            first = sorted_scores[0]
        if len(sorted_scores) > 1:
            second = sorted_scores[1]
        if len(sorted_scores) > 2:
            third = sorted_scores[2]

        string1 = "1) {0} : {1} points".format(first[0], first[1])
        string2 = "2) {0} : {1} points".format(second[0], second[1])
        string3 = "3) {0} : {1} points".format(third[0], third[1])

        text_font = pygame.font.Font(font["bradbunr"], 75)

        text1, textRect1 = self.createTextObj(string1, text_font)
        textRect1.center = self.screenW / 2, 250

        text2, textRect2 = self.createTextObj(string2, text_font)
        textRect2.center = self.screenW / 2, 350

        text3, textRect3 = self.createTextObj(string3, text_font)
        textRect3.center = self.screenW / 2, 450

        rectMenu = images["menu"].get_rect()
        rectMenu.center = (self.screenW / 2, self.screenH - rectMenu.size[1] / 2 - 50)

        rectLogo = images["highscores"].get_rect()
        rectLogo.center = (self.screenW / 2, rectLogo.height / 2)

        endMenu = False
        while not endMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endMenu = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if rectMenu.collidepoint(x, y):
                        endMenu = True
                        self.menu()

            self.screen.blit(images["bg_large"], (0, -50))
            self.screen.blit(images["highscores"], rectLogo)
            self.screen.blit(images["menu"], rectMenu)
            self.screen.blit(text1, textRect1)
            self.screen.blit(text2, textRect2)
            self.screen.blit(text3, textRect3)

            pygame.display.update()
        pygame.quit()
        quit()

    def menu(self):
        self.username = None

        rectLogo = images["logo"].get_rect()
        rectLogo.center = (self.screenW / 2, rectLogo.height / 2)

        rectSolo = images["start_solo"].get_rect()
        rectSolo.center = (self.screenW / 2, self.screenW / 2 - 100)

        rect_2_players = images["start_2_players"].get_rect()
        rect_2_players.center = (self.screenW / 2, self.screenW / 2)

        rectHighscores = images["see_highscore"].get_rect()
        rectHighscores.center = (self.screenW / 2, self.screenW / 2 + 100)

        endMenu = False
        while not endMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endMenu = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if rectSolo.collidepoint(x, y):
                        endMenu = True
                        self.enterName_solo()
                    elif rect_2_players.collidepoint(x, y):
                        endMenu = True
                        self.enterName_duo()
                    elif rectHighscores.collidepoint(x, y):
                        endMenu = True
                        self.highScoreMenu()

            self.screen.blit(images["bg_large"], (0, -50))
            self.screen.blit(images["logo"], rectLogo)
            self.screen.blit(images["start_solo"], rectSolo)
            self.screen.blit(images["start_2_players"], rect_2_players)
            self.screen.blit(images["see_highscore"], rectHighscores)

            pygame.display.update()
        pygame.quit()
        quit()

    def createTextObj(self, text, font):
        textSurface = font.render(text, True, colors["white"])
        return textSurface, textSurface.get_rect()

    def updateScore(self, ship, pipes, bg, clock):
        for pipe in pipes:
            if ship.x_pos > pipe.x_pos and not pipe.passed:
                ship.score += 1
                sounds["score"].play()
                if pipe.velocity < 13:
                    for pipe2 in pipes:
                        pipe2.velocity += 0.5
                    clock.velocity += 0.5
                if bg.velocity < 4:
                    bg.velocity += 0.2

                if pipe.space > 230 and ship.score % 5 == 0:
                    pipe.space -= 40
                pipe.passed = True
        if ship.score % 4 == 0 and ship.score != 0:
            clock.start()

    def getScore(self):
        if os.path.exists(name_score_file):
            with open(name_score_file, 'rb') as file:
                score_obj = pickle.Unpickler(file)
                scores = score_obj.load()
        else:
            scores = dict()
        return scores

    def saveScore(self):
        with open(name_score_file, 'wb') as file:
            score_obj = pickle.Pickler(file)
            score_obj.dump(self.all_scores)

    def drawGame_solo(self, game_objects):
        for object in game_objects.values():
            object.draw()

        text = pygame.font.Font(font["bradbunr"], 25)

        string = "Score : {}".format(game_objects["ship"].score)
        textSurface, textRect = self.createTextObj(string, text)
        self.screen.blit(textSurface, textRect)

        if game_objects["ship"].score > self.all_scores[self.username]:
            highScore = game_objects["ship"].score
        else:
            highScore = self.all_scores[self.username]

        string2 = "Player {0} best score : {1}".format(self.username, highScore)
        textSurface2, textRect2 = self.createTextObj(string2, text)
        textRect2.center = (self.screenW - textRect2.width / 2, textRect2.height / 2)
        self.screen.blit(textSurface2, textRect2)

        pygame.display.update()
        self.clock.tick(60)

    def startGame_solo(self):
        if self.username not in self.all_scores.keys():
            self.all_scores[self.username] = 0

        game_objects = {"bg": Background(self.screen), "ship": Ship(self.screen),
                        "pipes1": Pipes(self.screen, first=True), "pipes2": Pipes(self.screen, first=False),
                        "clock": Clock_item(self.screen)}

        # shortcuts for shorter code
        bg = game_objects["bg"]
        ship = game_objects["ship"]
        all_pipes = [game_objects["pipes1"], game_objects["pipes2"]]
        clock = game_objects["clock"]

        while not self.end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and ship.y_pos > ship.max_pos_y + ship.height:  # Jump with mouth
                        ship.jump()
                if pygame.mouse.get_pressed()[0] and ship.y_pos > ship.max_pos_y + ship.height:  # Jump with space bar
                    ship.jump()
            if ship.y_pos + ship.height > self.screenH:  # Fall
                self.lose_solo(ship)

            ship.move()
            if not ship.goForward:
                bg.move()
                clock.move()
                for pipe in all_pipes:
                    pipe.move()

            self.updateScore(ship, all_pipes, bg, clock)
            self.drawGame_solo(game_objects)
            if ship.collision_pipes(all_pipes):
                self.lose_solo(ship)
            if clock.appears and ship.collision_clock(clock):
                sounds["slow"].play()
                clock.respawn()
                for pipe in all_pipes:
                    pipe.velocity = pipe.origin_velocity
                bg.velocity = bg.origin_velocity
                clock.velocity = clock.origin_x_velocity

        pygame.quit()
        quit()

    def lose_solo(self, ship):
        rectBoom = images["boom"].get_rect()
        rectBoom.center = (self.screenW / 2, 350)

        rectStart_again = images["start_again"].get_rect()
        rectStart_again.center = (self.screenW / 2, 500)

        rectMenu = images["menu"].get_rect()
        rectMenu.center = (self.screenW / 2, self.screenH - rectMenu.size[1] / 2 - 50)

        rectAlien = images["alien"].get_rect()
        rectAlien.center = (self.screenW / 2, rectAlien.size[1] / 2 + 10)

        self.screen.blit(images["alien"], rectAlien)
        self.screen.blit(images["menu"], rectMenu)
        self.screen.blit(images["boom"], rectBoom)
        self.screen.blit(images["start_again"], rectStart_again)

        pygame.display.update()
        sounds["crash"].play()

        if ship.score > self.all_scores[self.username]:
            self.all_scores[self.username] = ship.score
            self.saveScore()
        ship.score = 0

        end_lose = False

        while not end_lose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if rectMenu.collidepoint(x, y):
                        end_lose = True
                        self.menu()
                    else:
                        self.waitBeforeStart_solo()
                        end_lose = True
                if event.type == pygame.KEYDOWN:
                    self.waitBeforeStart_solo()
                    end_lose = True

    def enterName_solo(self):
        endName = False

        while not endName:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endName = True

            text_name = pygame.font.Font(font["bradbunr"], 40)
            textSurface_name, textRect_name = self.createTextObj("Please enter your name", text_name)
            textRect_name.center = self.screenW / 2, ((self.screenH / 2) + 100)

            wordBox = pg_functions.makeTextBox(self.screenW / 2 - 150, self.screenH / 2 + 150, 300, 0, "Write here", 0,
                                               24)

            rectLogo = images["logo"].get_rect()
            rectLogo.center = (self.screenW / 2, rectLogo.height / 2)
            self.screen.blit(images["bg_large"], (0, -50))
            self.screen.blit(images["logo"], rectLogo)
            self.screen.blit(textSurface_name, textRect_name)
            pg_functions.showTextBox(wordBox)
            self.username = pg_functions.textBoxInput(wordBox).upper()
            pygame.display.update()
            if self.username is not None:
                endName = True
                self.waitBeforeStart_solo()
        pygame.quit()
        quit()

    def waitBeforeStart_solo(self):
        startGame = False

        text_one = pygame.font.Font(font["bradbunr"], 60)
        textSurface, textRect = self.createTextObj("Use space of left click to jump", text_one)
        textRect.center = 2 * self.screenW / 3, (2 * (self.screenH / 3))

        rectMenu = images["menu"].get_rect()
        rectMenu.center = (self.screenW / 2, self.screenH - rectMenu.size[1] / 2 - 50)

        rectReady = images["ready"].get_rect()
        rectReady.center = (self.screenW / 2, rectReady.height / 2)

        rectStart = images["start"].get_rect()
        rectStart.center = (self.screenW / 6, self.screenH / 2 + 100)

        self.screen.blit(images["bg_large"], (0, -50))
        self.screen.blit(images["start"], rectStart)
        self.screen.blit(images["ready"], rectReady)
        self.screen.blit(images["menu"], rectMenu)
        self.screen.blit(textSurface, textRect)
        pygame.display.update()

        while not startGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    startGame = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if rectMenu.collidepoint(x, y):
                        startGame = True
                        self.menu()
                    else:
                        startGame = True
                        self.startGame_solo()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        startGame = True
                        self.startGame_solo()

        pygame.quit()
        quit()

    def enterName_duo(self):
        pass
