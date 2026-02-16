# Ball Click Game - Based on Irv Kalb Chapter 6 Example

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
from Ball import *

# 2 - Define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
GAME_LENGTH = 15  # seconds

# ----------------------------
# Helper function to draw text
# ----------------------------
def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# 3 - Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ball Click Game")
clock = pygame.time.Clock()

# 4 - Initialize variables
ballList = []
score = 0
gameOver = False

startTicks = pygame.time.get_ticks()
lastSecond = 0  # track last full second counted

# Start with one ball
ballList.append(Ball(window, WINDOW_WIDTH, WINDOW_HEIGHT))

# 5 - Game loop
while True:

    # 6 - Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            mouseX, mouseY = pygame.mouse.get_pos()

            # Check if any balls were clicked
            for oBall in ballList[:]:  # copy of list so we can remove safely
                ballRect = pygame.Rect(oBall.x, oBall.y, oBall.width, oBall.height)
                if ballRect.collidepoint(mouseX, mouseY):
                    ballList.remove(oBall)
                    score += 1

    # 7 - Time tracking
    if not gameOver:
        currentTicks = pygame.time.get_ticks()
        secondsElapsed = (currentTicks - startTicks) // 1000

        # Every second add a new ball
        if secondsElapsed > lastSecond:
            lastSecond = secondsElapsed
            ballList.append(Ball(window, WINDOW_WIDTH, WINDOW_HEIGHT))

        # End game at 15 seconds
        if secondsElapsed >= GAME_LENGTH:
            gameOver = True
            ballList.clear()

    # 8 - Update balls
    if not gameOver:
        for oBall in ballList:
            oBall.update()

    # 9 - Clear screen
    window.fill(BLACK)

    # 10 - Draw balls
    for oBall in ballList:
        oBall.draw()

    # 11 - Draw score and timer
    if not gameOver:
        draw_text(window, f"Score: {score}", 10, 10, WHITE, 30)
        draw_text(window, f"Time: {secondsElapsed}", 10, 45, WHITE, 30)
    else:
        draw_text(window, "GAME OVER", 220, 180, WHITE, 50)
        draw_text(window, f"Final Score: {score}", 230, 240, WHITE, 40)

    # 12 - Update display
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)