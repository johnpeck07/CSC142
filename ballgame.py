import pygame
import random

# ----------------------------
# Helper function
# ----------------------------
def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# ----------------------------
# Ball class
# ----------------------------
class Ball:
    def __init__(self, window):
        self.window = window
        self.radius = 30
        self.color = (255, 0, 0)
        self.reset()

    def reset(self):
        self.x = random.randint(50, 750)
        self.y = random.randint(50, 550)
        self.xSpeed = random.choice([-3, 3])
        self.ySpeed = random.choice([-3, 3])
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def move(self):
        self.x += self.xSpeed
        self.y += self.ySpeed

        if self.x - self.radius <= 0 or self.x + self.radius >= 800:
            self.xSpeed *= -1

        if self.y - self.radius <= 0 or self.y + self.radius >= 600:
            self.ySpeed *= -1

        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def draw(self):
        pygame.draw.circle(self.window, self.color, (self.x, self.y), self.radius)

# ----------------------------
# Main game
# ----------------------------
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Click the Ball Game")
clock = pygame.time.Clock()

ball = Ball(window)

score = 0
game_over = False
start_time = pygame.time.get_ticks()

running = True
while running:
    clock.tick(FPS)
    window.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if ball.rect.collidepoint(event.pos):
                score += 1

                # Increase speed
                ball.xSpeed += random.randint(1, 5) * (1 if ball.xSpeed > 0 else -1)
                ball.ySpeed += random.randint(1, 5) * (1 if ball.ySpeed > 0 else -1)

                # Reset position
                ball.x = random.randint(50, 750)
                ball.y = random.randint(50, 550)

                if score >= 5:
                    game_over = True
                    end_time = pygame.time.get_ticks()
                    elapsed_seconds = (end_time - start_time) / 1000

    if not game_over:
        ball.move()
        ball.draw()
        draw_text(window, f"Score: {score}", 10, 10, (255, 255, 255))
    else:
        draw_text(window, "Game Over!", 320, 250, (255, 255, 255), 36)
        draw_text(
            window,
            f"Time: {elapsed_seconds:.2f} seconds",
            260,
            300,
            (255, 255, 255),
            28
        )

    pygame.display.update()

pygame.quit()
