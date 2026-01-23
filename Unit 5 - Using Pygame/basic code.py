import pygame, random

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60
frames =0

pygame.display.set_caption("My Pygame Application")
WHITE = (255,255,255)
RED = (255,0,0)

BACKGROUND_COLOR = (255,255,255) # WHITE

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()
    clock.tick(60)
    frames+=1
pygame.quit()