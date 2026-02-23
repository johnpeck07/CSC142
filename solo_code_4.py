# 1 - Import stuff we need
import pygame
from pygame.locals import *
import sys
import random
from math import sin

# helper text function (teacher provided)
def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Ball class (teacher version)
class Ball():
    def __init__(self, window, windowWidth, windowHeight):
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.image = pygame.image.load('images/ball.png')

        # rect info
        self.ballRect = self.image.get_rect()
        self.width = self.ballRect.width
        self.height = self.ballRect.height
        self.maxWidth = windowWidth - self.width
        self.maxHeight = windowHeight - self.height

        # random start
        self.x = random.randrange(0, self.maxWidth)
        self.y = self.height

        # random speeds
        speedsList = [-7, -6, -5, -4, -3, 3, 4, 5, 6, 7]
        self.xSpeed = random.choice(speedsList)
        self.ySpeed = random.randrange(self.maxHeight, self.windowHeight * 2)

    def update(self):
        # bounce off left/right
        if (self.x < -self.width) or (self.x >= self.windowWidth):
            self.xSpeed = -self.xSpeed

        # arc movement
        self.x = self.x + self.xSpeed
        self.y = self.windowWidth - self.ySpeed * sin(3.14 * self.x / self.maxWidth)

        # update rect
        self.ballRect.x = self.x
        self.ballRect.y = self.y

    def draw(self):
        self.window.blit(self.image, (self.x, self.y))


# 2 - Game constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30

# 3 - Setup pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ball Clicker Game")
clock = pygame.time.Clock()

# 4 - Font
font = pygame.font.SysFont(None, 36)

# 5 - Game variables
ballList = []
score = 0
lastSeconds = 0
startTicks = pygame.time.get_ticks()
gameOver = False

# 6 - Main loop
while True:

    # how many seconds have passed
    seconds = (pygame.time.get_ticks() - startTicks) // 1000

    # 7 - event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # clicking on balls
        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            mousePos = pygame.mouse.get_pos()
            for ball in ballList[:]:
                if ball.ballRect.collidepoint(mousePos):
                    ballList.remove(ball)
                    score += 1

    # 8 - game logic
    if not gameOver:

        # add a new ball every second
        if seconds > lastSeconds:
            ballList.append(Ball(window, WINDOW_WIDTH, WINDOW_HEIGHT))
            lastSeconds = seconds

        # end game at 15 seconds
        if seconds >= 15:
            gameOver = True
            ballList.clear()

        # update all balls
        for ball in ballList:
            ball.update()

    # 9 - clear screen
    window.fill(BLACK)

    # 10 - draw everything
    draw_text(window, f"Score: {score}", 10, 10, WHITE, 30)
    draw_text(window, f"Time: {seconds}", 10, 40, WHITE, 30)

    if not gameOver:
        for ball in ballList:
            ball.draw()
    else:
        draw_text(window, f"Game Over! Final Score: {score}", 150, 220, WHITE, 36)

    # 11 - update screen
    pygame.display.update()

    # 12 - control speed
    clock.tick(FRAMES_PER_SECOND)
