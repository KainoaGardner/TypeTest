import pygame
import random

TILESIZE = 40
WMARGINSIZE = TILESIZE * 5
HMARGINSIZE = TILESIZE * 2
LINELENGTH = 20
WIDTH = TILESIZE * LINELENGTH + WMARGINSIZE * 2
HEIGHT = HMARGINSIZE * 2 + TILESIZE * LINELENGTH // 2
FPS = 60



pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))


def getWordList(file):
    with open(file, "r") as wordFile:
        text = wordFile.readlines()

    wordList = []
    wordStartCounter = 0
    for index,word in enumerate(text[0]):
        if word == " ":
            wordList.append((text[0][wordStartCounter:index]))
            wordStartCounter = index + 1
    # levelList.append(wordList)
    return wordList

words = getWordList("words.txt")
