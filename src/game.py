from src.data import *
from src.ship import Ship
from src.pipes import Pipes
from src.background import Background
import lib.pygame_functions as pg_functions
import pickle
import os


class Game:
    screenW = SCREEN_WIDTH
    screenH = SCREEN_HEIGHT
    overlay = 50
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

    def createTextObj(self, text, font):
        textSurface = font.render(text, True, colors["white"])
        return textSurface, textSurface.get_rect()

    def endMessage(self, text):
        GOText = pygame.font.Font(font["bradbunr"], 150)
        smallText = pygame.font.Font(font["bradbunr"], 40)

        GOTextSurface, GOTextRect = self.createTextObj(text, GOText)
        GOTextRect.center = self.screenW / 2, (self.screenH / 2) + 50
        self.screen.blit(GOTextSurface, GOTextRect)

        smallTextSurface, smallTextRect = self.createTextObj("Press a key to start again or ENTER to go to menu",
                                                             smallText)
        smallTextRect.center = self.screenW / 2, ((self.screenH / 2) + 200)
        self.screen.blit(smallTextSurface, smallTextRect)

        pygame.display.update()

    def lose(self, ship):
        callMenu = False
        self.screen.blit(images["alien"], (self.screenW / 2 - 100, 30))
        self.endMessage("Boom!")
        sounds["crash"].play()
        if ship.score > self.all_scores[self.username]:
            self.all_scores[self.username] = ship.score
            self.saveScore()
        ship.score = 0
        while not callMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    callMenu = True
                    self.waitBeforeStart()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        callMenu = True
                        self.menu()
                    else:
                        self.waitBeforeStart()

    def updateScore(self, ship, pipes, bg):
        text = pygame.font.Font(font["bradbunr"], 25)

        string = "Score : {}".format(ship.score)
        textSurface, textRect = self.createTextObj(string, text)
        self.screen.blit(textSurface, textRect)

        if ship.score > self.all_scores[self.username]:
            highScore = ship.score
        else:
            highScore = self.all_scores[self.username]

        string2 = "Player {0} best score : {1}".format(self.username, highScore)
        textSurface2, textRect2 = self.createTextObj(string2, text)
        textRect2.center = (self.screenW - textRect2.width / 2, textRect2.height / 2)
        self.screen.blit(textSurface2, textRect2)

        for pipe in pipes:
            if ship.x_pos > pipe.x_pos and not pipe.passed:
                ship.score += 1
                sounds["score"].play()
                if pipe.velocity < 13:
                    for pipe2 in pipes:
                        pipe2.velocity += 0.3
                if bg.velocity < 4:
                    bg.velocity += 0.2

                if pipe.space > 230 and ship.score % 5 == 0:
                    pipe.space -= 40
                pipe.passed = True

    def getScore(self):
        if os.path.exists(name_score_file):
            with open(name_score_file, 'rb') as file:
                score_obj = pickle.Unpickler(file)
                scores = score_obj.load()
        else:
            scores = dict()
        return scores

    def saveScore(self):
        # self.all_scores = sorted(self.all_scores.items(), reverse=True, key=operator.itemgetter(1))

        with open(name_score_file, 'wb') as file:
            score_obj = pickle.Pickler(file)
            score_obj.dump(self.all_scores)

    def collision(self, ship, pipes):
        result = False
        for pipe in pipes:
            if ship.x_pos + ship.width > pipe.x_pos and ship.x_pos < pipe.x_pos + pipe.width:  # ship between pipes
                if ship.y_pos < pipe.y_pos_up + pipe.height:  # collide with top
                    result = True
                    break
                elif ship.y_pos + ship.height > pipe.y_pos_down:
                    result = True
                    break
        return result

    def drawGame(self, ship, pipes, bg):
        bg.draw()
        ship.draw()
        for pipe in pipes:
            pipe.draw()
        self.updateScore(ship, pipes, bg)
        if self.collision(ship, pipes):
            self.lose(ship)
        pygame.display.update()
        self.clock.tick(60)

    def startGame(self):

        if self.username not in self.all_scores.keys():
            self.all_scores[self.username] = 0

        bg = Background(self.screen, self.screenH, self.screenW)
        ship = Ship(self.screen, self.screenH, self.overlay)
        pipes = [Pipes(self.screen, self.screenH, self.screenW, self.overlay, 300, True),
                 Pipes(self.screen, self.screenH, self.screenW, self.overlay, 300, False)]
        while not self.end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and ship.y_pos > self.overlay + ship.height:
                        ship.jump()
                if pygame.mouse.get_pressed()[0] and ship.y_pos > self.overlay + ship.height:
                    ship.jump()
            if ship.y_pos + ship.height > self.screenH:
                self.lose(ship)

            ship.move()
            if not ship.goForward:
                bg.move()
                for pipe in pipes:
                    pipe.move()

            self.drawGame(ship, pipes, bg)
        pygame.quit()
        quit()

    def enterName(self):
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
                self.waitBeforeStart()
        pygame.quit()
        quit()

    def waitBeforeStart(self):
        startGame = False

        text_one = pygame.font.Font(font["bradbunr"], 60)
        textSurface, textRect = self.createTextObj("Use space of left click to jump", text_one)
        textRect.center = 2 * self.screenW / 3, (2 * (self.screenH / 3))

        rectReady = images["ready"].get_rect()
        rectReady.center = (self.screenW / 2, rectReady.height / 2)

        rectStart = images["start"].get_rect()
        rectStart.center = (self.screenW / 6, self.screenH / 2 + 100)

        self.screen.blit(images["bg_large"], (0, -50))
        self.screen.blit(images["start"], rectStart)
        self.screen.blit(images["ready"], rectReady)
        self.screen.blit(textSurface, textRect)
        pygame.display.update()

        while not startGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    startGame = True
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE:
                        startGame = True
                        self.startGame()
                if pygame.mouse.get_pressed()[0]:
                    startGame = True
                    self.startGame()
        pygame.quit()
        quit()

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

        textSurface, textRect = self.createTextObj("Press a key to go to menu", text_font)
        textRect.center = self.screenW / 2, ((self.screenH / 2) + 300)

        rectLogo = images["highscores"].get_rect()
        rectLogo.center = (self.screenW / 2, rectLogo.height / 2)

        endMenu = False
        while not endMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endMenu = True
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    endMenu = True
                    self.menu()

            self.screen.blit(images["bg_large"], (0, -50))
            self.screen.blit(images["highscores"], rectLogo)
            self.screen.blit(textSurface, textRect)
            self.screen.blit(text1, textRect1)
            self.screen.blit(text2, textRect2)
            self.screen.blit(text3, textRect3)

            pygame.display.update()
        pygame.quit()
        quit()

    def menu(self):
        self.username = None

        text_one = pygame.font.Font(font["bradbunr"], 75)
        textSurface, textRect = self.createTextObj("Press a key to start", text_one)
        textRect.center = self.screenW / 2, ((self.screenH / 2) + 100)

        textSurface2, textRect2 = self.createTextObj("Right click to see high scores", text_one)
        textRect2.center = self.screenW / 2, ((self.screenH / 2) + 200)

        endMenu = False
        while not endMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endMenu = True
                if event.type == pygame.KEYDOWN:
                    endMenu = True
                    self.enterName()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        endMenu = True
                        self.enterName()
                    elif pygame.mouse.get_pressed()[2]:
                        endMenu = True
                        self.highScoreMenu()
            rectLogo = images["logo"].get_rect()
            rectLogo.center = (self.screenW / 2, rectLogo.height / 2)
            self.screen.blit(images["bg_large"], (0, -50))
            self.screen.blit(images["logo"], rectLogo)
            self.screen.blit(textSurface, textRect)
            self.screen.blit(textSurface2, textRect2)
            pygame.display.update()
        pygame.quit()
        quit()