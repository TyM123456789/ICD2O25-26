import pygame
import sys
import random
# --- setup ---
pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Test: Move the Square")
clock = pygame.time.Clock()
# --- game objects ---
player = pygame.Rect(50, 50, 50, 50)  # x, y, w, h
speed = 1
# --- main loop ---
running = True
while running:
    # events (quit, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # input (held keys)
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += speed
    # update (with simple bounds)
    player.x = max(0, min(WIDTH - player.width, player.x + dx))
    player.y = max(0, min(HEIGHT - player.height, player.y + dy))
    # draw
    screen.fill((25, 25, 25))          # background
    pygame.draw.rect(screen, (0, 200, 255), player)  # player square
    pygame.display.flip()
    clock.tick(360)  # 60 FPS
    # player = pygame.Rect(player.x, player.y, random.randint(30,70), random.randint(30,70))
pygame.quit()
sys.exit()
