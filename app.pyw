import pygame
from pygame.locals import *
import random
from math import sqrt, pow

pygame.init()

# Screen
win = pygame.display.set_mode((288, 512))
win_w = win.get_width()
win_h = win.get_height()

pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('img/bird.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
# Background
bg = pygame.image.load('img/bg.png')
fg = pygame.image.load('img/fg.png')
# Score
score = 0
locked = False

class Bird(object):
    img = pygame.image.load('img/bird.png')
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.flyCount = 6
        self.isFly = False
        self.fallSpeed = 5.5
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # Hitbox

    def isCollide(self):
        if self.y >= win_h - 118 - self.height:
            return True
        return False

class PipeNorth(object):
    img = pygame.image.load('img/pipeNorth.png')
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        win.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # Hitbox

    def isCollide(self, rect):
        if rect[1] <= (self.hitbox[1] + self.hitbox[3]) and ((rect[0] + rect[2]) >= self.hitbox[0]) and (rect[0] <= (self.hitbox[0] + self.hitbox[2])):
            return True
        return False

class PipeSouth(PipeNorth):
    img = pygame.image.load('img/pipeSouth.png')
    def isCollide(self, rect):
        if rect[1] + rect[3] >= (self.hitbox[1]) and ((rect[0] + rect[2]) >= self.hitbox[0]) and (rect[0] <= (self.hitbox[0] + self.hitbox[2])):
            return True
        return False

def updateFile():
    # try:
    f = open('score.txt', 'r')
    file = f.readlines()
    try:
        last = int(file[0])

        if last < int(score):
            f.close()
            file = open('score.txt', 'w')
            file.write(str(int(score)))
            file.close()

            return score
        return last
    except:
        return '0'

def redrawWindow():
    win.blit(bg, (0,0))
    for objectt in objects:
        objectt.draw(win)
    win.blit(fg, (0, win_h - 118))
    bird.draw(win)
    fontScore = pygame.font.Font('font.ttf', 24)
    fontBestScore = pygame.font.Font('font.ttf', 18)
    scoreText = fontScore.render('SCORE: ' + str(int(score)), 1, (255,255,255))
    bestScoreText = fontBestScore.render('BEST SCORE: ' + str(updateFile()), 1, (255,255,255))
    win.blit(bestScoreText, (5, 10))
    win.blit(scoreText, (win_w - scoreText.get_width() - 10, 10))
    pygame.display.update()

def endScreen():
    global objects, score
    objects = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        win.blit(bg, (0,0))
        largeFont = pygame.font.Font('font.ttf', 60)
        smallFont = pygame.font.Font('font.ttf', 32)
        prevoiusScore = smallFont.render('Prevoius Score: ' + str(updateFile()), 1, (200,240,240))
        win.blit(prevoiusScore, (win_w/2 - prevoiusScore.get_width()/2, win_h/2 - prevoiusScore.get_height()/2))

        newScore = largeFont.render('Score: ' + str(int(score)), 1, (0,0,0))
        tapText = smallFont.render('TAP TO PLAY', 1, (100,100,100))
        win.blit(newScore, (win_w/2 - newScore.get_width()/2, win_h/2 - newScore.get_height()/2 + 70))
        win.blit(tapText, (win_w/2 - tapText.get_width()/2, win_h/2 - tapText.get_height()/2 + 120))
        pygame.display.update()

    score = 0
    # bird.falling = False
    bird.fallSpeed = 5.5
    bird.isFly = False
    bird.y = 0

# Game loop
bird = Bird(35, 0 - 26/2, 38, 26)
objects = []
run = True
pygame.time.set_timer(USEREVENT+1, random.randrange(1400,1700))

while run:
    keys = pygame.key.get_pressed()
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == USEREVENT+1:
            r = random.randrange(-200, 0)
            objects.append(PipeNorth(win_w, r, 52, 242))
            objects.append(PipeSouth(win_w, r + 242 + 110, 52, 378))
            locked = True

    # Flying
    if not(bird.isFly):
        if keys[pygame.K_UP] or keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
            bird.isFly = True
            bird.fallSpeed = 5.5
        else:
            bird.fallSpeed += 0.3
            bird.y += bird.fallSpeed
    else:
        if bird.flyCount >= 0:
            neg = 1
            if bird.flyCount < 0:
                neg = -1
            bird.y -= (bird.flyCount ** 2) * 0.5 * neg
            bird.flyCount -= 1
        else:
            bird.isFly = False
            bird.flyCount = 6

    for objectt in objects:
        if objectt.isCollide(bird.hitbox):
            endScreen()
    
        objectt.x -= 3.7
        if objectt.x < objectt.width * -1:
            objects.pop(objects.index(objectt))
            locked = False

        if not(objectt.isCollide(bird.hitbox)) and objectt.x <= 35 - objectt.width/3 and not(locked):
            score += 0.5
            locked = True

    # Collide
    # On the ground
    if bird.isCollide():
        bird.y = win_h - 118 - bird.height
        endScreen()

    redrawWindow()