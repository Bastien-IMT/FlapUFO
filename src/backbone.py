import os
import pickle

import lib.pygame_functions as pg_functions
from src.background import Background
from src.clock_item import Clock_item
from src.data import *
from src.game_split_screen import Game_split_screen
from src.pipes import Pipes
from src.ship import Ship
from src.play_game import Play_game


class Game:
    screenW = SCREEN_WIDTH
    screenH = SCREEN_HEIGHT
    pg_functions.screenSize(screenW, screenW)
    end_game = False
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

        text1, textRect1 = createTextObj(string1, text_font)
        textRect1.center = self.screenW / 2, 250

        text2, textRect2 = createTextObj(string2, text_font)
        textRect2.center = self.screenW / 2, 350

        text3, textRect3 = createTextObj(string3, text_font)
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

    # def updateScore(self, ship, pipes, bg, clock):
    #     for pipe in pipes:
    #         if ship.x_pos > pipe.x_pos and not pipe.passed:
    #             ship.score += 1
    #             sounds["score"].play()
    #             if pipe.velocity < 13:
    #                 for pipe2 in pipes:
    #                     pipe2.velocity += 0.5
    #                 clock.velocity += 0.5
    #             if bg.velocity < 4:
    #                 bg.velocity += 0.2
    #
    #             if pipe.space > 230 and ship.score % 5 == 0:
    #                 pipe.space -= 40
    #             pipe.passed = True
    #     if ship.score % 4 == 0 and ship.score != 0:
    #         clock.start()

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
        textSurface, textRect = createTextObj(string, text)
        self.screen.blit(textSurface, textRect)

        if game_objects["ship"].score > self.all_scores[self.username1]:
            highScore = game_objects["ship"].score
        else:
            highScore = self.all_scores[self.username1]

        string2 = "Player {0} best score : {1}".format(self.username1, highScore)
        textSurface2, textRect2 = createTextObj(string2, text)
        textRect2.center = (self.screenW - textRect2.width / 2, textRect2.height / 2)
        self.screen.blit(textSurface2, textRect2)

        pygame.display.update()
        self.clock.tick(60)

    def startGame_solo(self, game):
        if game.username not in self.all_scores.keys():
            self.all_scores[game.username] = 0

        game.end_game = False

        while not game.end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.end_game = True
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == game.jump_key:
                        game.ship.jump()
            game.update()
            game.draw()

            if game.ship.score > self.all_scores[game.username]:
                highScore = game.ship.score
            else:
                highScore = self.all_scores[game.username]

            text = pygame.font.Font(font["bradbunr"], 25)
            string2 = "Player {0} best score : {1}".format(game.username, highScore)
            textSurface2, textRect2 = createTextObj(string2, text)
            textRect2.center = (self.screenW - textRect2.width / 2, textRect2.height / 2)
            self.screen.blit(textSurface2, textRect2)

            pygame.display.update()
            self.clock.tick(60)

        if game.end_game:
            self.lose_solo(game)

    def lose_solo(self, game):
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

        if game.ship.score > self.all_scores[game.username]:
            self.all_scores[game.username] = game.ship.score
            self.saveScore()
        game.ship.score = 0

        end_lose_menu = False

        while not end_lose_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if rectMenu.collidepoint(x, y):
                        end_lose_menu = True
                        self.menu()
                    else:
                        self.waitBeforeStart_solo(game)
                        end_lose_menu = True
                if event.type == pygame.KEYDOWN:
                    self.waitBeforeStart_solo(game)
                    end_lose_menu = True

    def enterName_solo(self):
        endName = False

        while not endName:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endName = True

            text_name = pygame.font.Font(font["bradbunr"], 40)
            textSurface_name, textRect_name = createTextObj("Please enter your name", text_name)
            textRect_name.center = self.screenW / 2, ((self.screenH / 2) + 100)

            wordBox = pg_functions.makeTextBox(self.screenW / 2 - 150, self.screenH / 2 + 150, 300, 0, "Write here", 0,
                                               24)

            rectLogo = images["logo"].get_rect()
            rectLogo.center = (self.screenW / 2, rectLogo.height / 2)
            self.screen.blit(images["bg_large"], (0, -50))
            self.screen.blit(images["logo"], rectLogo)
            self.screen.blit(textSurface_name, textRect_name)
            pg_functions.showTextBox(wordBox)
            username = pg_functions.textBoxInput(wordBox).upper()
            pygame.display.update()

            game = Play_game(self.screen, username, solo=True)

            if game.username is not None:
                endName = True
                self.waitBeforeStart_solo(game)
        pygame.quit()
        quit()

    def waitBeforeStart_solo(self, game):
        startGame = False

        text_one = pygame.font.Font(font["bradbunr"], 60)
        textSurface, textRect = createTextObj("Use space of left click to jump", text_one)
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
                        self.startGame_solo(game)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        startGame = True
                        self.startGame_solo(game)

        pygame.quit()
        quit()

    def enterName_duo(self):
        endName1 = False
        endName2 = False

        while not (endName1 and endName2):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endName1 = True
                    endName2 = True

            text_name = pygame.font.Font(font["bradbunr"], 40)
            textSurface_name1, textRect_name1 = createTextObj("Player 1 name", text_name)
            textRect_name1.center = self.screenW / 4, ((self.screenH / 2) + 100)

            textSurface_name2, textRect_name2 = createTextObj("Player 2 name", text_name)
            textRect_name2.center = 3 * self.screenW / 4, ((self.screenH / 2) + 100)

            wordBox1 = pg_functions.makeTextBox(self.screenW / 4 - 150, self.screenH / 2 + 150, 300, 0, "Write here", 0,
                                                24)

            wordBox2 = pg_functions.makeTextBox((3 * self.screenW / 4) - 150, self.screenH / 2 + 150, 300, 0,
                                                "Write here", 0, 24)

            rectLogo = images["logo"].get_rect()
            rectLogo.center = (self.screenW / 2, rectLogo.height / 2)
            self.screen.blit(images["bg_large"], (0, -50))
            self.screen.blit(images["logo"], rectLogo)
            self.screen.blit(textSurface_name1, textRect_name1)
            self.screen.blit(textSurface_name2, textRect_name2)
            pg_functions.showTextBox(wordBox1)
            pg_functions.showTextBox(wordBox2)

            self.username1 = pg_functions.textBoxInput(wordBox1).upper()
            self.username2 = pg_functions.textBoxInput(wordBox2).upper()

            pygame.display.update()

            if self.username1 is not None:
                endName1 = True

            if self.username2 is not None:
                endName2 = True

            if endName1 and endName2:
                self.waitBeforeStart_duo()

        pygame.quit()
        quit()

    def waitBeforeStart_duo(self):
        startGame = False
        player1_ready = False
        player2_ready = False

        start_IMG = pygame.image.load("src/assets/start.png").convert_alpha()
        start_IMG = pygame.transform.scale(start_IMG, (300, 300))

        text = pygame.font.Font(font["bradbunr"], 40)
        textSurface1, textRect1 = createTextObj("{0} use Space to Jump".format(self.username1), text)
        textRect1.center = self.screenW / 4, (3 * (self.screenH / 4))

        textSurface2, textRect2 = createTextObj("{0} use Enter to Jump".format(self.username2), text)
        textRect2.center = 3 * self.screenW / 4, (3 * (self.screenH / 4))

        rectMenu = images["menu"].get_rect()
        rectMenu.center = (self.screenW / 2, self.screenH - rectMenu.size[1] / 2 - 50)

        rectReady = images["ready"].get_rect()
        rectReady.center = (self.screenW / 2, rectReady.height / 2)

        rectStart1 = start_IMG.get_rect()
        rectStart1.center = (self.screenW / 4, 300)

        rectStart2 = start_IMG.get_rect()
        rectStart2.center = (3 * self.screenW / 4, 300)

        self.screen.blit(images["bg_large"], (0, -50))
        pygame.draw.rect(self.screen, colors["black"], (self.screenW / 2 - 2, 0, 4, self.screenH))
        self.screen.blit(images["ready"], rectReady)
        self.screen.blit(images["menu"], rectMenu)
        self.screen.blit(textSurface1, textRect1)
        self.screen.blit(textSurface2, textRect2)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player1_ready = True
                        self.screen.blit(start_IMG, rectStart1)
                        pygame.display.update()

                    if event.key == pygame.K_RETURN:
                        player2_ready = True
                        self.screen.blit(start_IMG, rectStart2)
                        pygame.display.update()

            if player1_ready and player2_ready:
                startGame = True
                self.startGame_duo()
        pygame.quit()
        quit()

    def startGame_duo(self):
        game_left = Game_split_screen(self.screen, self.username1, is_left=True)
        game_right = Game_split_screen(self.screen, self.username2, is_left=False)

        while not self.end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_left.ship.y_pos > game_left.ship.max_pos_y + game_left.ship.height:
                        game_left.ship.jump()
                    if event.key == pygame.K_RETURN and game_right.ship.y_pos > game_right.ship.max_pos_y + game_right.ship.height:
                        game_right.ship.jump()
            if game_left.ship.y_pos + game_left.ship.height > self.screenH:  # Ship 1 falls
                self.lose_duo(game_left)
            if game_right.ship.y_pos + game_right.ship.height > self.screenH:  # Ship 2 falls
                self.lose_duo(game_right)

            game_left.ship.move()
            game_right.ship.move()

            if not game_left.ship.goForward:
                game_left.bg.move()
                game_left.pipes.move()
            if not game_right.ship.goForward:
                game_right.bg.move()
                game_right.pipes.move()

            self.updateScore_duo(game_left.ship, game_left.pipes, game_left.bg)
            self.updateScore_duo(game_right.ship, game_right.pipes, game_right.bg)

            game_left.draw_split_screen()
            game_right.draw_split_screen()
            pygame.display.update(
                pygame.draw.rect(self.screen, colors["black"], (self.screenW / 2 - 2, 0, 4, self.screenH)))

            if game_left.ship.collision_pipes([game_left.pipes]):
                self.lose_duo(game_left)
            if game_right.ship.collision_pipes([game_right.pipes]):
                self.lose_duo(game_right)
        pygame.quit()
        quit()

    def lose_duo(self, game):
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
                        self.waitBeforeStart_duo()
                        end_lose = True
                if event.type == pygame.KEYDOWN:
                    self.waitBeforeStart_duo()
                    end_lose = True
        pygame.quit()
        quit()

    def updateScore_duo(self, ship, pipe, bg):
        if ship.x_pos > pipe.x_pos and not pipe.passed:
            ship.score += 1
            sounds["score"].play()
            if pipe.velocity < 13:
                pipe.velocity += 0.5
            if bg.velocity < 4:
                bg.velocity += 0.2
            if pipe.space > 230 and ship.score % 5 == 0:
                pipe.space -= 40
            pipe.passed = True
