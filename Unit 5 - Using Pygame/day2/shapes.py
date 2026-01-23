import pygame, random

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60
frames =0

pygame.display.set_caption("Pygame: Colors + Shapes")
BACKGROUND_COLOR = (0,0,0) # BLACK

# player_image = pygame.image.load("dog.png")
# player_rect = player_image.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

BLACK=(0,0,0)
WHITE = (255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
PURPLE=(160,32,240)
CYAN=(0,255,255)
LIGHT_GRAY=(220,220,220)
CUSTOM=(40,170,220)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #background
    screen.fill(LIGHT_GRAY)
    #Rectangle (filled + outline)
    pygame.draw.rect(screen,BLUE, (80,80,160,100))
    pygame.draw.rect(screen,BLACK, (80,80,160,100),3)
    #Circle (filled + outline) & shifted 100 right
    pygame.draw.circle(screen,RED, (550,130),60)
    pygame.draw.circle(screen,BLACK, (550,130),60,3)
    #Line
    pygame.draw.line(screen,GREEN, (60,520),(840,520),2)
    #Polygon (filled + outline)
    triangle_points=[(650,250),(800,400),(500,400)]
    pygame.draw.polygon(screen,PURPLE, triangle_points)
    pygame.draw.polygon(screen,BLACK, triangle_points,3)
    #Ellipse (filled + outline)
    pygame.draw.ellipse(screen,CUSTOM, (80,260,220,120))
    pygame.draw.ellipse(screen,BLACK, (80,260,220,120),3)
    #Arc
    pygame.draw.arc(screen,CYAN, (360, 260, 180, 120), 0, 2*3.14159, 6)
    #Color squares
    pygame.draw.rect(screen,YELLOW, (720,60,50,50))
    pygame.draw.rect(screen,CYAN, (780,60,50,50))
    pygame.draw.rect(screen,PURPLE, (840,60,50,50))
    pygame.display.flip()
    clock.tick(FPS)
    frames+=1
pygame.quit()