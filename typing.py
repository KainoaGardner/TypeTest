import pygame
from settings import *
import random
import string
class TypeGame():
    def __init__(self,fontSize,fontColor,wordAmount):
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.wordAmount = wordAmount
        self.font = pygame.font.SysFont("Arial",self.fontSize)
        self.text = ""
        self.getText()
        self.lines = []
        self.makeLines()
        self.textGrid = []
        self.makeGrid()

        self.cursor = pygame.Surface((1,TILESIZE))
        self.cursor.fill("Red")
        self.cursorRect = self.cursor.get_rect(topleft = (WMARGINSIZE + TILESIZE // 4,HMARGINSIZE))
        self.pressed = False
        self.cursorCounter = 0
        self.cursorLineCounter = 0
        self.cursorY = 0

        self.incorrect = False
        self.incorrectLetter = ""

        self.shift = False
        self.correctLine = ""
        self.correctLetters = []
        self.correctSentence = []
        self.inputDict = {
            "space":" "
        }

        self.timer = 0
        self.start = False
        self.complete = False
        self.typedCharacters = 0
        self.highScore = 0
        self.buffer = 0

    def reset(self):
        self.timer = 0
        self.start = False
        self.complete = False
        self.correctLine = ""
        self.correctLetters = []
        self.correctSentence = []

        self.cursorRect.topleft = (WMARGINSIZE + TILESIZE // 4,HMARGINSIZE)

        self.pressed = False
        self.cursorCounter = 0
        self.cursorLineCounter = 0
        self.cursorY = 0
        self.text = ""
        self.getText()
        self.lines = []
        self.makeLines()
        self.textGrid = []
        self.makeGrid()

        self.typedCharacters = 0
        self.buffer = 0

    def getText(self):
        for i in range(self.wordAmount):
            self.text += words[random.randint(0,len(words)-1)].lower() + " "

    def makeLines(self):
        index = 0
        rowIndex = 0
        lastSpace = 0
        counter = 0
        while index < len(self.text):
            if self.text[index] == " ":
                lastSpace = index

            if rowIndex >= LINELENGTH * 2 - 1:
                self.lines.append(self.text[counter:lastSpace])
                counter = lastSpace + 1
                index = counter
                rowIndex = 0

            index += 1
            rowIndex += 1

        if lastSpace < index and self.text[lastSpace:] != " ":
            self.lines.append(self.text[lastSpace:-1])


    def makeGrid(self):
        for character in self.text:
            self.textGrid.append(character)

    def displayGraph(self):
        for r,row in enumerate(self.lines):
            for col in range(LINELENGTH * 2 - 1):
                pygame.draw.rect(screen,"#ecf0f1",pygame.Rect(WMARGINSIZE + TILESIZE //2 * col,HMARGINSIZE + r * TILESIZE,TILESIZE,TILESIZE))

    def displayCharacter(self):
        for r,row in enumerate(self.lines):
            for c,col in enumerate(row):
                character = self.font.render(col,True,self.fontColor)
                characterRect = character.get_rect(center = (WMARGINSIZE + c * TILESIZE //2 + TILESIZE // 2, HMARGINSIZE + r * TILESIZE + TILESIZE // 2))
                screen.blit(character,characterRect)

        for r,letter in enumerate(self.correctLetters):
                character = self.font.render(letter, True, "#27ae60")
                characterRect = character.get_rect(center=(WMARGINSIZE + r * TILESIZE // 2 + TILESIZE // 2, HMARGINSIZE + self.cursorLineCounter * TILESIZE + TILESIZE // 2))
                screen.blit(character, characterRect)

        for r, row in enumerate(self.correctSentence):
            for c, col in enumerate(row):
                character = self.font.render(col, True, "#27ae60")
                characterRect = character.get_rect(center=(
                WMARGINSIZE + c * TILESIZE // 2 + TILESIZE // 2, HMARGINSIZE + r * TILESIZE + TILESIZE // 2))
                screen.blit(character, characterRect)

        character = self.font.render(self.incorrectLetter,True,"#e74c3c")
        characterRect = character.get_rect(center=(WMARGINSIZE + self.cursorCounter * TILESIZE // 2 + TILESIZE //2,HMARGINSIZE + self.cursorLineCounter * TILESIZE + TILESIZE // 2))
        screen.blit(character, characterRect)
    def border(self):
        pygame.draw.line(screen,"#2d3436",(WMARGINSIZE,HMARGINSIZE),(WIDTH - WMARGINSIZE,HMARGINSIZE),5)
        pygame.draw.line(screen, "#2d3436", (WMARGINSIZE, HMARGINSIZE + TILESIZE * len(self.lines)), (WIDTH - WMARGINSIZE, HMARGINSIZE + TILESIZE * len(self.lines)), 5)

        pygame.draw.line(screen, "#2d3436", (WMARGINSIZE, HMARGINSIZE), (WMARGINSIZE, HMARGINSIZE + TILESIZE * len(self.lines)), 5)
        pygame.draw.line(screen, "#2d3436", (WIDTH - WMARGINSIZE, HMARGINSIZE),(WIDTH - WMARGINSIZE, HMARGINSIZE + TILESIZE * len(self.lines)), 5)


    def displayCursor(self):
        screen.blit(self.cursor,self.cursorRect)

    def type(self,input):
        if input in string.ascii_letters or input == "space" or input == "backspace":
            if self.complete == False:
                if self.start == False:
                    self.start = True
            if input in self.inputDict:
                input = self.inputDict.get(input)

            if self.cursorCounter < len(self.lines[self.cursorLineCounter]):
                if self.lines[self.cursorLineCounter][self.cursorCounter] == input and self.incorrectLetter == "":
                    self.correctLetters.append(input)
                    self.cursorRect.x += TILESIZE // 2
                    self.cursorCounter += 1
                    self.typedCharacters += 1
                elif input == "backspace" and len(self.incorrectLetter) == 1:
                    self.incorrectLetter = ""
                    self.incorrect = False
                    self.cursorRect.x -= TILESIZE // 2
                elif input not in ["backspace","left shift"]:
                    self.incorrectLetter = input
                    if self.incorrect == False:
                        self.cursorRect.x += TILESIZE // 2
                        self.incorrect = True


        if len(self.lines[self.cursorLineCounter]) == len(self.correctLetters) and input == " " or (len(self.lines) - 1 == len(self.correctSentence) and len(self.lines[self.cursorLineCounter]) == len(self.correctLetters)):
            self.correctLine = self.correctLine.join(self.correctLetters)
            self.correctSentence.append(self.correctLine)
            self.correctLine = ""
            self.cursorCounter = 0
            self.cursorLineCounter += 1
            self.correctLetters = []
            self.cursorRect.y += TILESIZE
            self.cursorRect.x = WMARGINSIZE + TILESIZE // 4

    def checkFinish(self):
        if self.correctSentence == self.lines:
            if (((self.typedCharacters / 4.7) / (self.timer // FPS)) * FPS) > self.highScore:
                self.highScore = round((((self.typedCharacters / 4.7) / (self.timer // FPS)) * FPS),2)
            self.complete = True

    def displayEndResult(self):
        if self.complete:
            self.start = False
            text = self.font.render(str(round((self.timer / FPS),1)) + "s", True, "#ecf0f1")
            textRect = text.get_rect(center=(WIDTH // 2, HMARGINSIZE + TILESIZE * len(self.lines) + TILESIZE))
            screen.blit(text, textRect)

            wpm = (((self.typedCharacters / 4.7) / (self.timer // FPS)) * FPS)
            wordsPerMin = self.font.render(str(round(wpm,2)) + " Words Per Minute", True, "#ecf0f1")
            wordsPerMinRect = wordsPerMin.get_rect(center=(WIDTH // 2, HEIGHT - TILESIZE * 3))
            screen.blit(wordsPerMin, wordsPerMinRect)

            restart = self.font.render("Press R to restart", True, "#ecf0f1")
            restartRect = restart.get_rect(center=(WIDTH // 2, HEIGHT - TILESIZE))
            screen.blit(restart, restartRect)

            highScore = self.font.render("HighScore: " + str(self.highScore) + " Words Per Minute", True, "#ecf0f1")
            highScoreRect = highScore.get_rect(center=(WIDTH // 2, HEIGHT - TILESIZE * 2))
            screen.blit(highScore, highScoreRect)

    def updateTimer(self):
        if self.start:
            self.timer += 1
            text = self.font.render(str(round((self.timer / FPS),1)) + "s", True, "#ecf0f1")
            textRect = text.get_rect(center=(WIDTH // 2, HMARGINSIZE + TILESIZE * len(self.lines) + TILESIZE))
            screen.blit(text, textRect)

    def keyInput(self):
        if self.complete:
            self.buffer += 1
            if self.buffer > 50:
                key = pygame.key.get_pressed()
                if key[pygame.K_r]:
                    self.reset()
    def display(self):
        self.displayGraph()
        self.border()
        self.displayCharacter()
        self.displayCursor()
        self.checkFinish()
        self.updateTimer()
        self.displayEndResult()
        self.keyInput()

typeGame = TypeGame(TILESIZE,"#636e72",30)