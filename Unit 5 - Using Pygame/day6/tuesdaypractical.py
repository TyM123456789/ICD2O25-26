
import pygame
import random
pygame.init()
# prepare the screen
frames=0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision Detection")
clock = pygame.time.Clock()
# --- sizes ---
PLAYER_SIZE = 20
PRIZE_SIZE = 20
player1_rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
player2_rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
prize_rect = pygame.Rect(0, 0, PRIZE_SIZE, PRIZE_SIZE)
wall_left = pygame.Rect(160,150,10,300)
wall_top = pygame.Rect(200,110,400,10)
wall_right = pygame.Rect(630,150,10,300)
wall_bottom = pygame.Rect(200,480,400,10)
dx1, dy1, dx2, dy2 = 5,5,5,5
def rectangles_overlap(r1, r2):
    r1_left   = r1.x
    r1_right  = r1.x + r1.w
    r1_top    = r1.y
    r1_bottom = r1.y + r1.h
    r2_left   = r2.x
    r2_right  = r2.x + r2.w
    r2_top    = r2.y
    r2_bottom = r2.y + r2.h
    overlap_x = (r1_left < r2_right) and (r1_right > r2_left)
    overlap_y = (r1_top  < r2_bottom) and (r1_bottom > r2_top)
    return overlap_x and overlap_y
def keep_on_screen(r):
    r.x = max(0, min(SCREEN_WIDTH - r.w, r.x))
    r.y = max(0, min(SCREEN_HEIGHT - r.h, r.y))
def random_on_screen(r):
    r.x = random.randint(0, SCREEN_WIDTH - r.w)
    r.y = random.randint(0, SCREEN_HEIGHT - r.h)
def spawn_object(obj):
    x=random.randint(0,SCREEN_WIDTH)
    y=random.randint(0,SCREEN_HEIGHT)
    obj = pygame.Rect(x,y,obj.w,obj.h)
    keep_on_screen(obj)
    while rectangles_overlap(prize_rect,obj) or rectangles_overlap(player1_rect,obj) or rectangles_overlap(player2_rect,obj) or rectangles_overlap(wall_top,obj) or rectangles_overlap(wall_bottom,obj) or rectangles_overlap(wall_left,obj) or rectangles_overlap(wall_right,obj): 
        keep_on_screen(obj)
        x=random.randint(0,SCREEN_WIDTH)
        y=random.randint(0,SCREEN_WIDTH)
        obj = pygame.Rect(x,y,obj.w,obj.h)
    return obj
player1_rect = spawn_object(pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE))
player2_rect = spawn_object(pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE))
prize_rect = spawn_object(pygame.Rect(0, 0, PRIZE_SIZE, PRIZE_SIZE))
# --- place players so they DON'T overlap at the start ---
random_on_screen(player1_rect)
while True:
    random_on_screen(player2_rect)
    if not rectangles_overlap(player1_rect, player2_rect):
        break
# --- place prize (starter) ---
random_on_screen(prize_rect)
score1 = 0
score2 = 0
font = pygame.font.SysFont(None, 40)
# IT player (1 or 2) - Player 1 starts as IT
it_player = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    # ---------------- Player 1 movement ----------------
    old1_x, old1_y = player1_rect.x, player1_rect.y
    if keys[pygame.K_RIGHT]: player1_rect.x += dx1
    if keys[pygame.K_LEFT]:  player1_rect.x -= dx1
    if keys[pygame.K_UP]:    player1_rect.y -= dy1
    if keys[pygame.K_DOWN]:  player1_rect.y += dy1
    keep_on_screen(player1_rect)
    # If player 1 moved into player 2, put player 1 back
    if rectangles_overlap(player1_rect, wall_top) or rectangles_overlap(player1_rect, wall_bottom) or rectangles_overlap(player1_rect, wall_right) or rectangles_overlap(player1_rect, wall_left):
        player1_rect.x, player1_rect.y = old1_x, old1_y
    elif rectangles_overlap(player2_rect, player1_rect):
            it_player = not it_player
            dx1, dy1, dx2, dy2, = 5,5,5,5
            if it_player:
                player1_rect = spawn_object(player1_rect)
                score2+=1
            else:
                player2_rect = spawn_object(player2_rect)    
                score1+=1
    elif rectangles_overlap(player1_rect,prize_rect):
        if it_player:
            prize_rect = spawn_object(prize_rect)
            dx1, dy1 = 7,7         

    ### ADD SPEED BOOST

    # ---------------- Player 2 movement ----------------
    old2_x, old2_y = player2_rect.x, player2_rect.y
    if keys[pygame.K_d]: player2_rect.x += dx2
    if keys[pygame.K_a]: player2_rect.x -= dx2
    if keys[pygame.K_w]: player2_rect.y -= dy2
    if keys[pygame.K_s]: player2_rect.y += dy2
    keep_on_screen(player2_rect)
    # If player 2 moved into player 1, put player 2 back
    if rectangles_overlap(player2_rect, wall_top) or rectangles_overlap(player2_rect, wall_bottom) or rectangles_overlap(player2_rect, wall_right) or rectangles_overlap(player2_rect, wall_left):
        player2_rect.x, player2_rect.y = old2_x, old2_y
    elif rectangles_overlap(player2_rect,prize_rect):
        prize_rect = spawn_object(prize_rect)
        if not it_player:
            dx2, dy2 = 7,7

    ### ADD SPEED BOOST

    # ---------------- draw ----------------
    screen.fill((128, 128, 128))
    pygame.draw.rect(screen, (0, 0, 150), prize_rect)
    pygame.draw.rect(screen, (150, 0, 0), player1_rect)
    pygame.draw.rect(screen, (0, 150, 0), player2_rect)
    pygame.draw.rect(screen, (0, 0, 0), wall_left)
    pygame.draw.rect(screen, (0, 0, 0), wall_bottom)
    pygame.draw.rect(screen, (0, 0, 0), wall_right)
    pygame.draw.rect(screen, (0, 0, 0), wall_top)
    msg = font.render(f"{score1} - {score2}", True, (200, 200, 210))
    screen.blit(msg, (12, 10))
    # stroke/outline on the IT player
    if it_player:
        pygame.draw.rect(screen, (250, 250, 0), player1_rect, 2)
    else:
        pygame.draw.rect(screen, (250, 250, 0), player2_rect, 2)
    pygame.display.flip()
    clock.tick(60)
    frames+=1
pygame.quit()
