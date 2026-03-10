# starting up pygame stuff

import pygame
from pygame.locals import *
import sys
import random
import os

# makes sure python looks in the same folder as this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# function to draw text on the screen
def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# some basic colors and game settings
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
N_PIXELS_PER_FRAME = 3

# start pygame and make the window
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# load the ball picture
ballImage = pygame.image.load("ball.png")

# make the ball smaller so it doesn't get stuck
ballImage = pygame.transform.scale(ballImage, (50, 50))

# font for text
font = pygame.font.SysFont(None, 36)

# get the ball's rectangle (its size and position)
ballRect = ballImage.get_rect()

# make sure the random range doesn't break
MAX_WIDTH = max(1, WINDOW_WIDTH - ballRect.width)
MAX_HEIGHT = max(1, WINDOW_HEIGHT - ballRect.height)

# put the ball somewhere random to start
ballRect.left = random.randrange(MAX_WIDTH)
ballRect.top = random.randrange(MAX_HEIGHT)

# how fast the ball moves
xSpeed = N_PIXELS_PER_FRAME
ySpeed = N_PIXELS_PER_FRAME

# score and game state
score = 0
gameOver = False
startTime = pygame.time.get_ticks()

# main game loop (runs forever)
while True:

    # check for events like clicking or closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # clicking on the ball
        if event.type == MOUSEBUTTONDOWN and not gameOver:
            if ballRect.collidepoint(event.pos):
                score += 1

                # move ball to a new random spot
                ballRect.left = random.randrange(MAX_WIDTH)
                ballRect.top = random.randrange(MAX_HEIGHT)

                # make the ball go faster
                xSpeed = abs(xSpeed) + random.randint(1, 5)
                ySpeed = abs(ySpeed) + random.randint(1, 5)

                # randomly flip direction
                xSpeed *= random.choice([-1, 1])
                ySpeed *= random.choice([-1, 1])

                # win the game at score 5
                if score == 5:
                    gameOver = True
                    endTime = pygame.time.get_ticks()
                    elapsedTime = (endTime - startTime) / 1000

    # move the ball around if the game isn't over
    if not gameOver:

        # bounce off left wall
        if ballRect.left < 0:
            ballRect.left = 0
            xSpeed = -xSpeed

        # bounce off right wall
        if ballRect.right > WINDOW_WIDTH:
            ballRect.right = WINDOW_WIDTH
            xSpeed = -xSpeed

        # bounce off top wall
        if ballRect.top < 0:
            ballRect.top = 0
            ySpeed = -ySpeed

        # bounce off bottom wall
        if ballRect.bottom > WINDOW_HEIGHT:
            ballRect.bottom = WINDOW_HEIGHT
            ySpeed = -ySpeed

        # actually move the ball
        ballRect.left += xSpeed
        ballRect.top += ySpeed

    # clear the screen
    window.fill(BLACK)

    # draw the score
    draw_text(window, f"Score: {score}", 10, 10, WHITE, 36)

    # draw the ball or the win message
    if not gameOver:
        window.blit(ballImage, ballRect)
    else:
        message = font.render(
            f"You won! Time: {elapsedTime:.2f} seconds",
            True,
            WHITE
        )
        messageRect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(message, messageRect)

    # update the screen
    pygame.display.update()

    # keep the game running at the right speed
    clock.tick(FRAMES_PER_SECOND)
