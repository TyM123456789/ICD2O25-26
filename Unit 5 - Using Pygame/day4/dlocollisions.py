
   

import pygame
import random
pygame.init()

#prepare the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Collision Detection")
clock = pygame.time.Clock()

x = random.randint(0,SCREEN_WIDTH-20)
y = random.randint(0,SCREEN_HEIGHT-20)

player1_rect = pygame.Rect(100,75,50,75)
player2_rect = pygame.Rect(500,475,50,75)
prize_rect = pygame.Rect(x,y,20,20)

dx = 1
dy = 1 

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

score1 = 0
score2 = 0
font = pygame.font.SysFont(None, 40)
# main game loop runs until game is over
running = True
while running:
    # events (quit, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    old_x, old_y = player1_rect.x, player1_rect.y
    if keys[pygame.K_RIGHT]:  player1_rect.x += dx
    if keys[pygame.K_LEFT]:  player1_rect.x -= dx
    if keys[pygame.K_UP]:  player1_rect.y -= dy
    if keys[pygame.K_DOWN]:  player1_rect.y += dy
    
    player1_rect.x = max(0, player1_rect.x)
    player1_rect.y = max(0, player1_rect.y)
    player1_rect.y = min(SCREEN_HEIGHT-player1_rect.h, player1_rect.y)
    player1_rect.x = min(SCREEN_WIDTH-player1_rect.w, player1_rect.x)
    
    if rectangles_overlap(player1_rect,player2_rect):
        player1_rect.x = old_x
        player1_rect.y = old_y
    
    if keys[pygame.K_d]:  player2_rect.x += dx
    if keys[pygame.K_a]:  player2_rect.x -= dx
    if keys[pygame.K_w]:  player2_rect.y -= dy
    if keys[pygame.K_s]:  player2_rect.y += dy
    
    player2_rect.x = max(0, player2_rect.x)
    player2_rect.y = max(0, player2_rect.y)
    player2_rect.y = min(SCREEN_HEIGHT-player2_rect.h, player2_rect.y)
    player2_rect.x = min(SCREEN_WIDTH-player2_rect.w, player2_rect.x)
    
    
    screen.fill((128,128,128))
    pygame.draw.rect(screen,(150,0,0), player1_rect)
    pygame.draw.rect(screen,(0,150,0), player2_rect)
    pygame.draw.rect(screen,(0,0,150), prize_rect)
    
    
    msg = font.render(str(score1) + " - " + str(score2), True, (200, 200, 210))
    screen.blit(msg, (12, 10))
    pygame.display.flip() #redraw the screen
    clock.tick(600)  # 60 FPS
pygame.quit()
