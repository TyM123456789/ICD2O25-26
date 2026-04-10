import pygame,random

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60
frames =0

pygame.display.set_caption("Assessment 2")
BACKGROUND_COLOR = (128,128,128) # WHITE


def x_detection(rect1,rect2):
    #right of rect1
    if (rect1.x + rect1.w == rect2.x or rect1.x+rect1.w == rect2.x+1) and ((rect1.y <= rect2.y <= rect1.y+rect1.h or rect1.y <= rect2.y+rect2.h <= rect1.y+rect1.h)or(rect2.y <= rect1.y <= rect2.y+rect2.h or rect2.y <= rect1.y +rect1.h <= rect2.y+rect2.h)):
        return True
    #left of rect1
    elif (rect1.x == rect2.x+rect2.w or rect1.x == rect2.x+rect2.w-1) and ((rect1.y <= rect2.y <= rect1.y+rect1.h or rect1.y <= rect2.y+rect2.h <= rect1.y+rect1.h)or(rect2.y <= rect1.y <= rect2.y+rect2.h or rect2.y <= rect1.y +rect1.h <= rect2.y+rect2.h)):
        return True
    else:
        return False

def y_detection(rect1,rect2):
    #bottom of rect1
    if (rect1.y + rect1.h == rect2.y or rect1.y+rect1.h == rect2.y+1) and ((rect1.x <= rect2.x <= rect1.x+rect1.w or rect1.x <= rect2.x+rect2.w <= rect1.x+rect1.w)or(rect2.x <= rect1.x <= rect2.x+rect2.w or rect2.x <= rect1.x +rect1.w <= rect2.x+rect2.w)):
        return True
    #top of rect1
    elif (rect1.y == rect1.y+rect2.h or rect1.y == rect2.y+rect2.h-1) and ((rect1.x <= rect2.x <= rect1.x+rect1.w or rect1.x <= rect2.x+rect2.w <= rect1.x+rect1.w)or(rect2.x <= rect1.x <= rect2.x+rect2.w or rect2.x <= rect1.x +rect1.w <= rect2.x+rect2.w)):
        return True
    else:
        return False

def rectangles_overlap(player1_rect, player2_rect):
    # --- Player 1 edges ---
    p1_left   = player1_rect.x
    p1_right  = player1_rect.x + player1_rect.w
    p1_top    = player1_rect.y
    p1_bottom = player1_rect.y + player1_rect.h
    # --- Player 2 edges ---
    p2_left   = player2_rect.x
    p2_right  = player2_rect.x + player2_rect.w
    p2_top    = player2_rect.y
    p2_bottom = player2_rect.y + player2_rect.h
    # --- Overlap checks (broken into parts) ---
    overlap_x = (p1_left < p2_right) and (p1_right > p2_left)
    overlap_y = (p1_top  < p2_bottom) and (p1_bottom > p2_top)
    # --- Collision only if both overlap ---
    collision = overlap_x and overlap_y
    return collision

def spawn_prize():
    global prize
    x=random.randint(0,SCREEN_WIDTH)
    y=random.randint(0,SCREEN_HEIGHT)
    prize = pygame.Rect(x,y,10,10)
    while rectangles_overlap(player1,prize) or rectangles_overlap(player2,prize) or rectangles_overlap(wall_top,prize) or rectangles_overlap(wall_bottom,prize) or rectangles_overlap(wall_left,prize) or rectangles_overlap(wall_right,prize): 
        x=random.randint(0,SCREEN_WIDTH)
        y=random.randint(0,SCREEN_WIDTH)
        prize = pygame.Rect(x,y,10,10)
    prize = pygame.Rect(x,y,10,10)


player1 = pygame.Rect(SCREEN_WIDTH/2-(20+1),SCREEN_HEIGHT/2,20,20)
player2 = pygame.Rect(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,20,20)
wall_left = pygame.Rect(160,150,10,300)
wall_top = pygame.Rect(200,110,400,10)
wall_right = pygame.Rect(630,150,10,300)
wall_bottom = pygame.Rect(200,480,400,10)
spawn_prize()
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

    p1found = False
    p2found = False

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
    if x_detection(player1, player2) or x_detection(player1, wall_top) or x_detection(player1, wall_bottom) or x_detection(player1, wall_left) or x_detection(player1, wall_right): p1xchange = True
    else: p1xchange = False
    
    #p2x
    if x_detection(player2, player1) or x_detection(player2, wall_top) or x_detection(player2, wall_bottom) or x_detection(player2, wall_left) or x_detection(player2, wall_right): p2xchange = True
    else: p2xchange = False

    if p1xchange:
        player1.x = p1prevx
    if p2xchange:
        player2.x = p2prevx
        
    #p1y
    if y_detection(player1, player2) or y_detection(player1, wall_top) or y_detection(player1, wall_bottom) or y_detection(player1, wall_left) or y_detection(player1, wall_right): p1ychange = True
    else: p1ychange = False
    
    #p2x
    if y_detection(player2, player1) or y_detection(player2, wall_top) or y_detection(player2, wall_bottom) or y_detection(player2, wall_left) or y_detection(player2, wall_right): p2ychange = True
    else: p2ychange = False

    if p1ychange:
        player1.y = p1prevy
    if p2ychange:
        player2.y = p2prevy


    #prize detection
    if x_detection(player1, prize) or y_detection(player1, prize):
        p1found = True
    else: p1found = False

    #prize detection
    if x_detection(player2, prize) or y_detection(player2, prize): p2found = True
    else: p2found = False

    if p1found:
        score1+=1
        spawn_prize()
    if p2found:
        score2+=1
        spawn_prize()


    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen,(0,0,255), prize)
    pygame.draw.rect(screen, (255,0,0), player1)
    pygame.draw.rect(screen, (0,110,0), player2)
    pygame.draw.rect(screen,(0,0,0),wall_top)
    pygame.draw.rect(screen,(0,0,0),wall_left)
    pygame.draw.rect(screen,(0,0,0),wall_right)
    pygame.draw.rect(screen,(0,0,0),wall_bottom)
    msg = font.render(str(score1) + " - " + str(score2), True, (230,230,230))
    screen.blit(msg, (12, 10))
    pygame.display.flip()
    clock.tick(400)
    frames+=1
pygame.quit()