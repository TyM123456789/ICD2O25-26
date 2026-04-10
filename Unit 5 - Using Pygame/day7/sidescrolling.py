import pygame
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
pygame.display.set_caption("side scrolling")


# Load sprite sheet
sheet = pygame.image.load('boy_walking.png').convert()
BG_KEY = sheet.get_at((0, 0))
sheet.set_colorkey(BG_KEY)

background = pygame.image.load('background.png').convert()
bg_w, bg_h = background.get_size()
scale = SCREEN_H / bg_h
bg_scaled_w = int(bg_w * scale)
background = pygame.transform.smoothscale(background, (bg_scaled_w, SCREEN_H))

CELL_W = sheet.get_width() // 4
CELL_H = sheet.get_height() // 4

def get_frame(col, row):
    rect = pygame.Rect(col * CELL_W, row * CELL_H, CELL_W, CELL_H)
    frame = sheet.subsurface(rect).copy()
    frame.set_colorkey(BG_KEY)
    frame = pygame.transform.scale(frame, (CELL_W//3, CELL_H//3))
    return frame
current_frame = get_frame(0,0)
player_rect = current_frame.get_rect(center=(SCREEN_W//2, 445))

camera_x = 0
DEAD_ZONE = 120
CENTER_X = SCREEN_W // 2
LEFT_EDGE = CENTER_X - DEAD_ZONE
RIGHT_EDGE = CENTER_X + DEAD_ZONE
running = True
right = 0
anim_counter = 0
frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_RIGHT]): 
        player_rect.x +=2
        if anim_counter%15 == 0:
            if right != True:
                right = True
                frame = 0
            frame = (frame + 1) % 4
            current_frame = get_frame(frame, 3)
    if (keys[pygame.K_LEFT]): 
        player_rect.x -=2     
        if anim_counter%15 == 0:   
            if right != False:
                right = False
                frame = 0
            frame = (frame + 1) % 4
            current_frame = get_frame(frame, 2)
    if not (keys[pygame.K_LEFT]) and not (keys[pygame.K_RIGHT]) and (keys[pygame.K_UP]):
        current_frame = get_frame(0,1)
        right = 0
    if not (keys[pygame.K_LEFT]) and not (keys[pygame.K_RIGHT]) and not (keys[pygame.K_UP]) and keys[pygame.K_DOWN]:
        current_frame = get_frame(0,0)
        right = 0

    player_screen_x = player_rect.x - camera_x
    if player_screen_x > RIGHT_EDGE:
        camera_x += player_screen_x - RIGHT_EDGE
    elif player_screen_x < LEFT_EDGE:
        camera_x += player_screen_x - LEFT_EDGE
    anim_counter+=1
    
    camera_x = max(0, min(camera_x, background.get_width() - SCREEN_W))
    player_screen_x = player_rect.x - camera_x

    screen.blit(background, (-camera_x, 0))
    screen.blit(current_frame, (player_screen_x, player_rect.y))
    pygame.display.flip()
    clock.tick(60)


