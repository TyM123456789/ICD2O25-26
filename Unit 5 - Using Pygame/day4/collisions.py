import pygame,random

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60
frames =0

pygame.display.set_caption("Collision Detection")
BACKGROUND_COLOR = (255,255,255) # WHITE

player1 = pygame.Rect(SCREEN_WIDTH/2-(50+1),SCREEN_HEIGHT/2,50,75)
player2 = pygame.Rect(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,50,75)
prize = pygame.Rect(random.randint(0,SCREEN_WIDTH-20),random.randint(0,SCREEN_HEIGHT-20),20,20)
score1=0
score2=0
font = pygame.font.SysFont(None, 40)
running = True
while running:
    speed = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    p1prevx = player1.x
    p1prevy = player1.y
    p2prevx = player2.x
    p2prevy = player2.y

    if (keys[pygame.K_RIGHT]): player1.x +=speed
    if (keys[pygame.K_LEFT]): player1.x -=speed
    if (keys[pygame.K_UP]): player1.y -=speed
    if (keys[pygame.K_DOWN]): player1.y +=speed
    player1.x=max(0,player1.x)
    player1.y=max(0,player1.y)
    player1.y = min(SCREEN_HEIGHT-player1.h,player1.y)
    player1.x = min(SCREEN_WIDTH-player1.w,player1.x)
    



    if (keys[pygame.K_d]): player2.x +=speed
    if (keys[pygame.K_a]): player2.x -=speed
    if (keys[pygame.K_w]): player2.y -=speed
    if (keys[pygame.K_s]): player2.y +=speed
    if player2.x + player2.w > SCREEN_WIDTH: player2.x = SCREEN_WIDTH-player2.w 
    if player2.y + player2.h > SCREEN_HEIGHT: player2.y = SCREEN_HEIGHT-player2.h
    player2.x=max(0,player2.x)
    player2.y=max(0,player2.y)
    player2.y = min(SCREEN_HEIGHT-player2.h,player2.y)
    player2.x = min(SCREEN_WIDTH-player2.w,player2.x)

    #p1x
    if (player1.x + player1.w == player2.x or player1.x+player1.w == player2.x+1) and (player2.y <= player1.y <= player2.y+player2.h or player2.y <= player1.y +player1.h <= player2.y+player2.h):
        p1xchange = True
    elif (player1.x == player2.x+player2.w or player1.x == player2.x+player2.w-1) and (player2.y <= player1.y <= player2.y+player2.h or player2.y <= player1.y +player1.h <= player2.y+player2.h):
        p1xchange = True
    else: p1xchange = False
    
    #p2x
    if (player2.x + player2.w == player1.x or player2.x+player2.w == player1.x+1) and (player1.y <= player2.y <= player1.y+player1.h or player1.y <= player2.y +player2.h <= player1.y+player1.h):
        p2xchange = True
    elif (player2.x == player1.x+player1.w or player2.x == player1.x+player1.w-1) and (player1.y <= player2.y <= player1.y+player1.h or player1.y <= player2.y +player2.h <= player1.y+player1.h):
        p2xchange = True
    else: p2xchange = False

    if p1xchange:
        player1.x = p1prevx
    if p2xchange:
        player2.x = p2prevx
        
    #p1y
    if (player1.y + player1.h == player2.y or player1.y+player1.h == player2.y+1) and (player2.x <= player1.x <= player2.x+player2.w or player2.x <= player1.x +player1.w <= player2.x+player2.w):
        p1ychange = True
    elif (player1.y == player2.y+player2.h or player1.y == player2.y+player2.h-1) and (player2.x <= player1.x <= player2.x+player2.w or player2.x <= player1.x +player1.w <= player2.x+player2.w):
        p1ychange = True
    else: p1ychange = False

    #p2y
    if (player2.y + player2.h == player1.y or player2.y+player2.h == player1.y+1) and (player1.x <= player2.x <= player1.x+player1.w or player1.x <= player2.x +player2.w <= player1.x+player1.w):
        p2ychange = True
    elif (player2.y == player1.y+player1.h or player2.y == player1.y+player1.h-1) and (player1.x <= player2.x <= player1.x+player1.w or player1.x <= player2.x +player2.w <= player1.x+player1.w):
            p2ychange = True
    else: p2ychange = False

    if p1ychange:
        player1.y = p1prevy
    if p2ychange:
        player2.y = p2prevy


    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen,(255,255,0), prize)
    pygame.draw.rect(screen, (255,0,0), player1)
    pygame.draw.rect(screen, (0,0,255), player2)
    msg = font.render(str(score1) + " - " + str(score2), True, (0,0,0))
    screen.blit(msg, (12, 10))
    pygame.display.flip()
    clock.tick(720)
    frames+=1
pygame.quit()