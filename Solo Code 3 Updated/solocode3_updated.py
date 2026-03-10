# Click-the-ball game 
import pygame
from pygame.locals import *
import sys
import random
import os

# ----------------------------
# 1. Constants
# ----------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
N_PIXELS_PER_FRAME = 3
TARGET_SCORE = 5
BALL_SIZE = 50

# ----------------------------
# 2. Initialize Pygame
# ----------------------------
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Click the Ball!")
clock = pygame.time.Clock()

# ----------------------------
# 3. Load Ball Image (same folder version)
# ----------------------------
current_dir = os.path.dirname(__file__)
ball_path = os.path.join(current_dir, "ball.png")

# Check if file exists before loading
if not os.path.exists(ball_path):
    print("ERROR: ball.png not found!")
    print("Looking in:", ball_path)
    print("Files in folder:", os.listdir(current_dir))
    pygame.quit()
    sys.exit()

ballImage = pygame.image.load(ball_path)
ballImage = pygame.transform.scale(ballImage, (BALL_SIZE, BALL_SIZE))

# ----------------------------
# 4. Helper function for text
# ----------------------------
def draw_text(surface, text, x, y, color, font_size=24):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# ----------------------------
# 5. Initialize variables
# ----------------------------
ballRect = ballImage.get_rect()

MAX_WIDTH = max(1, WINDOW_WIDTH - ballRect.width)
MAX_HEIGHT = max(1, WINDOW_HEIGHT - ballRect.height)

ballRect.left = random.randrange(MAX_WIDTH)
ballRect.top = random.randrange(MAX_HEIGHT)

xSpeed = N_PIXELS_PER_FRAME
ySpeed = N_PIXELS_PER_FRAME
score = 0
game_start_time = pygame.time.get_ticks()
game_over = False

# ----------------------------
# 6. Main game loop
# ----------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN and not game_over:
            if ballRect.collidepoint(event.pos):
                score += 1

                # Move ball to random location
                ballRect.left = random.randrange(MAX_WIDTH)
                ballRect.top = random.randrange(MAX_HEIGHT)

                # Increase speed slightly
                xSpeed += random.randint(1, 3) * (1 if xSpeed > 0 else -1)
                ySpeed += random.randint(1, 3) * (1 if ySpeed > 0 else -1)

                if score >= TARGET_SCORE:
                    game_over = True
                    game_end_time = pygame.time.get_ticks()

        elif event.type == KEYDOWN and game_over:
            if event.key == K_r:
                # Restart game
                score = 0
                xSpeed = N_PIXELS_PER_FRAME
                ySpeed = N_PIXELS_PER_FRAME
                ballRect.left = random.randrange(MAX_WIDTH)
                ballRect.top = random.randrange(MAX_HEIGHT)
                game_start_time = pygame.time.get_ticks()
                game_over = False

    if not game_over:
        # Bounce logic
        if ballRect.left <= 0 or ballRect.right >= WINDOW_WIDTH:
            xSpeed = -xSpeed

        if ballRect.top <= 0 or ballRect.bottom >= WINDOW_HEIGHT:
            ySpeed = -ySpeed

        ballRect.left += xSpeed
        ballRect.top += ySpeed

    # ----------------------------
    # Draw everything
    # ----------------------------
    window.fill(BLACK)

    if not game_over:
        window.blit(ballImage, ballRect)
        draw_text(window, f"Score: {score}", 10, 10, WHITE)
        draw_text(window, f"Target: {TARGET_SCORE}", 10, 35, WHITE)
    else:
        elapsed_time = (game_end_time - game_start_time) / 1000
        draw_text(window, f"You clicked the ball {TARGET_SCORE} times!", 120, 200, WHITE, 32)
        draw_text(window, f"Time: {elapsed_time:.2f} seconds", 200, 250, WHITE, 28)
        draw_text(window, "Press R to Restart", 220, 300, WHITE, 24)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)