import pygame, random

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60
frames =0

pygame.display.set_caption("My Pygame Application")
BACKGROUND_COLOR = (255,255,255) # WHITE

player_image = pygame.image.load("dog.png")
player_rect = player_image.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if frames%1==0:
        BACKGROUND_COLOR = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    screen.fill(BACKGROUND_COLOR)
    screen.blit(player_image,player_rect)
    pygame.display.flip()
    clock.tick(60)
    frames+=1