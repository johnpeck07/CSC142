import pygame
import sys
from Ball import Ball

# =========================
# Helper Function
# =========================
def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# =========================
# Main Program
# =========================
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ball Click Game")

clock = pygame.time.Clock()

# Load ball image (use Irv's method/path)
ballImage = pygame.image.load("images/ball.png")

# Game Variables
ballList = []
score = 0
gameStartTicks = pygame.time.get_ticks()
lastSeconds = 0
gameOver = False

running = True
while running:
    clock.tick(FPS)

    # Calculate elapsed time
    currentTicks = pygame.time.get_ticks()
    elapsedSeconds = (currentTicks - gameStartTicks) // 1000

    # Check for game over
    if elapsedSeconds >= 15:
        gameOver = True
        ballList.clear()

    # Add new ball every second
    if not gameOver and elapsedSeconds > lastSeconds:
        newBall = Ball(ballImage, WINDOW_WIDTH, WINDOW_HEIGHT)
        ballList.append(newBall)
        lastSeconds = elapsedSeconds

    # =========================
    # Event Handling
    # =========================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse click detection
        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            mousePos = pygame.mouse.get_pos()

            for ball in ballList[:]:  # iterate over copy
                if ball.rect.collidepoint(mousePos):
                    ballList.remove(ball)
                    score += 1

    # =========================
    # Update Balls
    # =========================
    if not gameOver:
        for ball in ballList:
            ball.update()

    # =========================
    # Drawing
    # =========================
    window.fill((30, 30, 30))

    for ball in ballList:
        ball.draw(window)

    # Display score and time
    draw_text(window, f"Score: {score}", 10, 10, (255, 255, 255), 30)
    draw_text(window, f"Time: {elapsedSeconds}", 10, 45, (255, 255, 255), 30)

    if gameOver:
        draw_text(window, "GAME OVER", 300, 250, (255, 0, 0), 50)
        draw_text(window, f"Final Score: {score}", 300, 320, (255, 255, 255), 40)

    pygame.display.update()

pygame.quit()
sys.exit()