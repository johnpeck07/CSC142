# Click-the-ball game (GitHub-friendly version)
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
BALL_SIZE = 50  # scaled ball

# ----------------------------
# 2. Initialize Pygame
# ----------------------------
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Click the Ball!")
clock = pygame.time.Clock()

# ----------------------------
# 3. Load assets (relative paths)
# ----------------------------
# Get current folder (so relative paths work)
current_dir = os.path.dirname(__file__)

ball_path = os.path.join(current_dir, 'images', 'ball.png')
ballImage = pygame.image.load(ball_path)
ballImage = pygame.transform.scale(ballImage, (BALL_SIZE, BALL_SIZE))

# Optional: bounce and success sounds
try:
    bounceSound = pygame.mixer.Sound(os.path.join(current_dir, 'sounds', 'boing.wav'))
except:
    bounceSound = None

try:
    successSound = pygame.mixer.Sound(os.path.join(current_dir, 'sounds', 'success.wav'))
except:
    successSound = None

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

# Max position to avoid ball going off-screen
MAX_WIDTH = max(1, WINDOW_WIDTH - ballRect.width)
MAX_HEIGHT = max(1, WINDOW_HEIGHT - ballRect.height)

# Random initial position
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
                if successSound:
                    successSound.play()
                # Move ball to a new random location
                ballRect.left = random.randrange(MAX_WIDTH)
                ballRect.top = random.randrange(MAX_HEIGHT)
                # Randomly increase speed
                xSpeed += random.randint(1, 5) * (1 if xSpeed > 0 else -1)
                ySpeed += random.randint(1, 5) * (1 if ySpeed > 0 else -1)
                # Check if game over
                if score >= TARGET_SCORE:
                    game_over = True
                    game_end_time = pygame.time.get_ticks()

    if not game_over:
        # Move ball and bounce off edges
        if ballRect.left < 0 or ballRect.right >= WINDOW_WIDTH:
            xSpeed = -xSpeed
            if bounceSound:
                bounceSound.play()
        if ballRect.top < 0 or ballRect.bottom >= WINDOW_HEIGHT:
            ySpeed = -ySpeed
            if bounceSound:
                bounceSound.play()

        ballRect.left += xSpeed
        ballRect.top += ySpeed

    # Draw everything
    window.fill(BLACK)

    if not game_over:
        window.blit(ballImage, ballRect)
        draw_text(window, f"Score: {score}", 10, 10, WHITE)
    else:
        elapsed_time = (game_end_time - game_start_time) / 1000
        draw_text(window, "You clicked the ball 5 times!", 150, 200, WHITE, 36)
        draw_text(window, f"Time: {elapsed_time:.2f} seconds", 180, 260, WHITE, 30)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)