import pygame

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60
frames =0

pygame.display.set_caption("Landscape Assignment")
BACKGROUND_COLOR = (0,0,0) # BLACK

SKY=(10,200,255)
WHITE = (255,255,255)
RED=(255,0,0)
GREEN=(0,170,80)
DARK_GREEN=(0,100,0)
YELLOW=(255,255,0)
PURPLE=(160,32,240)
CYAN=(0,255,255)
LIGHT_GRAY=(200,200,200)
BLACK=(0,0,0)
BEIGE = (230,200,200)
BROWN = (130,60,60)
#150,65,0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #background
    screen.fill(SKY)
    pygame.draw.rect(screen,GREEN,(0,300,900,400))
    pygame.draw.line(screen,DARK_GREEN, (0,300),(800,300),4)
    #SUN
    pygame.draw.circle(screen,YELLOW, (80,80),30)
    pygame.draw.line(screen,YELLOW, (80,115),(80,145),3)
    pygame.draw.line(screen,YELLOW, (80,45),(80,15),3)
    pygame.draw.line(screen,YELLOW, (115,80),(145,80),3)
    pygame.draw.line(screen,YELLOW, (45,80),(15,80),3)
    #CLOUDS (CHANGE CLOUD SHAPES)
    pygame.draw.ellipse(screen,WHITE, (160,50,70,50))
    pygame.draw.ellipse(screen,WHITE, (180,70,120,50))
    pygame.draw.ellipse(screen,WHITE, (190,30,90,50))
    pygame.draw.ellipse(screen,WHITE, (205,50,110,50))

    pygame.draw.ellipse(screen,WHITE, (560,60,80,60))
    pygame.draw.ellipse(screen,WHITE, (600,80,130,60))
    pygame.draw.ellipse(screen,WHITE, (600,40,97,56))
    pygame.draw.ellipse(screen,WHITE, (615,60,120,60))
    
    #house
    pygame.draw.rect(screen,BEIGE,(280,290,243,170))
    pygame.draw.rect(screen,BLACK,(280,290,243,170),3) #523
    #roof
    triangle_points=[(260,290),(543,290),(401.5,180)]
    pygame.draw.polygon(screen,BROWN, triangle_points)
    pygame.draw.polygon(screen,BLACK, triangle_points,3)
    #door 
    pygame.draw.rect(screen,BROWN,(370,350,66,110))
    pygame.draw.rect(screen,BLACK,(370,350,66,110),2)   
    pygame.draw.circle(screen,YELLOW, (425,400),6)
    #windows
    pygame.draw.rect(screen,SKY,(300,330,60,50))
    pygame.draw.rect(screen,BLACK,(300,330,60,50),2)
    pygame.draw.line(screen,BLACK, (300,355),(360,355),2)
    pygame.draw.line(screen,BLACK, (330,330),(330,380),2)
    pygame.draw.rect(screen,SKY,(445,330,60,50))
    pygame.draw.rect(screen,BLACK,(445,330,60,50),2)
    pygame.draw.line(screen,BLACK, (445,355),(505,355),2)
    pygame.draw.line(screen,BLACK, (475,330),(475,380),2)
    #chimney
    pygame.draw.rect(screen,BROWN,(460,200,35,95))
    pygame.draw.rect(screen,BLACK,(460,200,35,95),2)
    #smoke
    pygame.draw.ellipse(screen,LIGHT_GRAY, (475,170,30,20))
    pygame.draw.ellipse(screen,LIGHT_GRAY, (490,150,35,25))

    #birds
    pygame.draw.arc(screen,BLACK, (130, 150, 40, 25), 0, 3.14159, 2)
    pygame.draw.arc(screen,BLACK, (170, 150, 40, 25), 0, 3.14159, 2)
    pygame.draw.arc(screen,BLACK, (205, 125, 30, 20), 0, 3.14159, 2)
    pygame.draw.arc(screen,BLACK, (235, 125, 30, 20), 0, 3.14159, 2)

    pygame.draw.arc(screen,BLACK, (650, 130, 40, 25), 0, 3.14159, 2)
    pygame.draw.arc(screen,BLACK, (690, 130, 40, 25), 0, 3.14159, 2)
    pygame.draw.arc(screen,BLACK, (720, 150, 20, 17), 0, 3.14159, 2)
    pygame.draw.arc(screen,BLACK, (740, 150, 20, 17), 0, 3.14159, 2)

    pygame.display.flip()
    clock.tick(FPS)
    frames+=1
pygame.quit()