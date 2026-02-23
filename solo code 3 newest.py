# 1 - Start

import pygame
from pygame.locals import *
import sys
import random

# 2 - Helping function
def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# 3 - Define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
N_PIXELS_PER_FRAME = 3

# 4 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 5 - Load assets  ✅ FIXED PATHS
ballImage = pygame.image.load('Solo Code 3 Updated/images/ball.png')
bounceSound = pygame.mixer.Sound('Solo Code 3 Updated/sounds/boing.wav')
successSound = pygame.mixer.Sound('Solo Code 3 Updated/sounds/boing.wav')
pygame.mixer.music.load('Solo Code 3 Updated/sounds/background.mp3')
pygame.mixer.music.play(-1, 0.0)

# 6 - Font
font = pygame.font.SysFont(None, 36)

# 7 - Initialize variables
ballRect = ballImage.get_rect()
MAX_WIDTH = WINDOW_WIDTH - ballRect.width
MAX_HEIGHT = WINDOW_HEIGHT - ballRect.height
ballRect.left = random.randrange(MAX_WIDTH)
ballRect.top = random.randrange(MAX_HEIGHT)

xSpeed = N_PIXELS_PER_FRAME
ySpeed = N_PIXELS_PER_FRAME

score = 0
gameOver = False
startTime = pygame.time.get_ticks()

# 8 - Main loop
while True:

    # 9 - Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and not gameOver:
            if ballRect.collidepoint(event.pos):
                score += 1
                successSound.play()

                # Move ball to new random position
                ballRect.left = random.randrange(MAX_WIDTH)
                ballRect.top = random.randrange(MAX_HEIGHT)

                # Increase speed
                xSpeed = abs(xSpeed) + random.randint(1, 5)
                ySpeed = abs(ySpeed) + random.randint(1, 5)

                # Randomize direction
                xSpeed *= random.choice([-1, 1])
                ySpeed *= random.choice([-1, 1])

                # End game at score 5
                if score == 5:
                    gameOver = True
                    endTime = pygame.time.get_ticks()
                    elapsedTime = (endTime - startTime) / 1000

    # 10 - Per-frame logic
    if not gameOver:
        if (ballRect.left < 0) or (ballRect.right >= WINDOW_WIDTH):
            xSpeed = -xSpeed
            bounceSound.play()

        if (ballRect.top < 0) or (ballRect.bottom >= WINDOW_HEIGHT):
            ySpeed = -ySpeed
            bounceSound.play()

        ballRect.left += xSpeed
        ballRect.top += ySpeed

    # 11 - Clear screen
    window.fill(BLACK)

    # 12 - Draw
    draw_text(window, f"Score: {score}", 10, 10, WHITE, 36)

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

    # 13 - Update screen
    pygame.display.update()

    # 14 - Tick
    clock.tick(FRAMES_PER_SECOND)