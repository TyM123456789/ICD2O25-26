import pygame, random, math
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Character Demo")
#setup sound
pygame.mixer.init()
jump = [pygame.mixer.Sound("jump.wav"), pygame.mixer.Sound("jump2.wav")]
hit_s = [pygame.mixer.Sound("hit1.wav"), pygame.mixer.Sound("hit2.wav")]
pause_s = [pygame.mixer.Sound("pause sound.wav"), pygame.mixer.Sound("pause2.wav")]
die_s = [pygame.mixer.Sound("die.wav"),pygame.mixer.Sound("die2.wav"), pygame.mixer.Sound("die3.wav")]
footstep_s = [pygame.mixer.Sound("footstep 1.wav")]
for sound in footstep_s:
    sound.set_volume(.04)
player_hit_s = []
slash_s = []
playing = False
# --- Load assets ---
body_sheet = pygame.image.load("Walking.png").convert_alpha()
arms_sheet = pygame.image.load("arms.png").convert_alpha()
enemy_sheet = pygame.image.load("Enemy.png").convert_alpha()

SCALE = 2

BODY_FRAMES = 10
ARM_FRAMES = 17
ENEMY_FRAMES = 7
BW = body_sheet.get_width() // BODY_FRAMES
BH = body_sheet.get_height()
AW = arms_sheet.get_width() // ARM_FRAMES
AH = arms_sheet.get_height()
EW = enemy_sheet.get_width() // ENEMY_FRAMES
EH = enemy_sheet.get_height()

#set up camera
camera_x = 0
camera_y=0
CAM_MARGIN_X = 300
hitboxes = False

#colors
WHITE = (255,255,255)
SKY = (0, 200, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (250,150,20)
GRAY = (130,130,130)
CYAN = (0,255,255)

#font
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
pause_font = pygame.font.SysFont('Comic Sans MS', 80)

#sets up frames
enemy_sheet.set_colorkey((0, 0, 0))
body_frames = [pygame.transform.scale(body_sheet.subsurface((i*BW,0,BW,BH)), (BW*SCALE,BH*SCALE)) for i in range(BODY_FRAMES)]
arms_frames = [pygame.transform.scale(arms_sheet.subsurface((i*AW,0,AW,AH)), (AW*SCALE,AH*SCALE)) for i in range(ARM_FRAMES)]
enemy_frames = [pygame.transform.scale(enemy_sheet.subsurface((i*EW,0,EW,EH)), (EW*SCALE,EH*SCALE)) for i in range(ENEMY_FRAMES)]

#flipped frames
body_frames_flipped = [pygame.transform.flip(f, True, False) for f in body_frames]
arms_frames_flipped = [pygame.transform.flip(f, True, False) for f in arms_frames]
enemy_frames_flipped = [pygame.transform.flip(f, True, False) for f in enemy_frames]

# Attack animation indices
slash1 = [11, 12, 13]
slash2 = [14, 15]
stab   = [8, 9, 10]


pausescreen = pygame.Surface((200, 150), pygame.SRCALPHA)

grid = []
with open("map.tile") as f:
    for line in f:
        row = [int(ch) for ch in line.strip()]
        grid.append(row)
TILE = 32 * SCALE
GROUND = (len(grid) - 1) * TILE - (BH * SCALE)
BG = pygame.transform.scale(pygame.image.load("background_game.png"), (800*4, 600*4))

tiles = [
    "",
    pygame.transform.scale(pygame.image.load("blue light tile.png"), (TILE, TILE)),
    pygame.transform.scale(pygame.image.load("blue dark tile.png"), (TILE, TILE))
]
# Calculate map dimensions in pixels
map_width = len(grid[0]) * TILE
map_height = len(grid) * TILE
def draw_tiles(surface, grid, camera_x, camera_y):
    x=0
    y=0
    for row_i, row in enumerate(grid):
        y=-camera_y
        for col_i, tile in enumerate(row):
            if tile != 0:
                x = col_i * TILE - camera_x
                y = row_i * TILE - camera_y
                screen.blit (tiles[tile], (x,y))

def get_tile_rects(grid):
    rects = []
    for row_i, row in enumerate(grid):
        for col_i, tile in enumerate(row):
            if tile != 0:
                rects.append(pygame.Rect(col_i * TILE, row_i * TILE, TILE, TILE))
    return rects

def play_sound(type):
    global playing
    if type == "die":
        die_s[random.randint(0, len(die_s) -1)].play()
    if type == "enemy hit":
        hit_s[random.randint(0, len(hit_s) -1)].play()
    # if type == "player hit":
    #     player_hit_s[random.randint(0, len(player_hit_s) -1)].play()
    if type == "pause_s":
        pause_s[random.randint(0, len(pause_s) -1)].play()
    if type == "jump":
        jump[random.randint(0, len(jump) -1)].play()
    if type =="footstep" and not playing:
        playing = True
        footstep_s[random.randint(0, len(footstep_s) -1)].play()
        playing = False
    # if type == "slash":
    #     slash_s[random.randint(0, len(slash_s) -1)].play()
class Player:
    def __init__(self): #__init__ means initialize self is the characyer
        self.x, self.y = WIDTH // 2, GROUND
        self.speed = 4
        self.max_speed = 0
        self.facing_right = True
        self.y_vel = 0
        self.on_ground = True
        self.moving = False
        self.hit = False
        self.last_hit = 0
        self.hit_enemies = set()
        self.kb_x = 0
        self.kb_y = 0
        self.max_hp = 100
        self.hp = self.max_hp
        self.harm = RED
        self.stab_cooldown = 0
        self.gravity = .7
        self.lunge_power = 10
        self.knockback_x=10
        self.knockback_y=7
        self.jump = -20

        self.frame = 0
        self.anim_timer = 0

        self.attacking = False
        self.attack_state = 0
        self.attack_frame = 0
        self.attack_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.attacking:
            play_sound("slash")
            # cycle between slash1 and slash2
            if self.attack_state == 1:
                self.attack_state = 2
            else:
                self.attack_state = 1
            self.attacking = True
            self.attack_frame = 0
            self.attack_timer = 0
            self.hit_enemies = set()

        # Stab
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and self.stab_cooldown <= 0.07:
            self.attack_state = 3
            self.attacking = True
            self.attack_frame = 0
            self.attack_timer = 0
            self.stab_cooldown = 1.2
            self.hit_enemies = set()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            global hitboxes
            hitboxes = not hitboxes
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            global in_Game
            play_sound("pause_s")
            in_Game = not in_Game

        # Jump Start
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.on_ground:
                play_sound("jump")
                self.y_vel = p1.jump  # Initial jump burst
                self.on_ground = False

                # Variable Jump: If they let go of Space while moving up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.y_vel < -3: # If still moving upward significantly
                    self.y_vel = -3 # "Cut" the jump velocity

    def update(self, dt, keys, tile_rects):
        #stab cooldown
        p1.stab_cooldown -=dt
        if p1.stab_cooldown < .07:
            p1.stab_cooldown = 0
        # --- 1. Horizontal Movement & Collision ---
        self.moving = False
        dx = 0
        if keys[pygame.K_a] and not (self.attacking and self.attack_state == 3 and self.facing_right):
            if self.frame == 2 or self.frame == 6:
                play_sound("footstep")
            dx -= self.speed
            self.facing_right = False
            self.moving = True
        if keys[pygame.K_d] and not (self.attacking and self.attack_state == 3 and not self.facing_right):
            if self.frame == 2 or self.frame == 6:
                play_sound("footstep")
            dx += self.speed
            self.facing_right = True
            self.moving = True

        # Apply X movement (including knockback)
        self.x += dx + self.kb_x
            
        # Check X collisions immediately
        player_rect = self.get_rect()
        for tile_rect in tile_rects:
            if player_rect.colliderect(tile_rect):
                if (dx + self.kb_x) > 0: # Moving Right
                    self.x = tile_rect.left - (BW - 40) * SCALE - 40
                elif (dx + self.kb_x) < 0: # Moving Left
                    self.x = tile_rect.right - 40
                self.kb_x = 0 # Stop horizontal momentum on wall hit

        # --- 2. Vertical Movement & Collision ---
        self.y_vel += self.gravity
        self.y += self.y_vel + self.kb_y
            
        # CRITICAL: Assume we are in the air until proven otherwise
        self.on_ground = False 

        # Re-check rect after X is settled
        player_rect = self.get_rect() 

        for tile_rect in tile_rects:
            if player_rect.colliderect(tile_rect):
                if (self.y_vel + self.kb_y) > 0:  # Falling Down
                    self.y = tile_rect.top - (BH * SCALE)
                    self.y_vel = 0
                    self.kb_y = 0
                    self.on_ground = True # Found the floor!
                elif (self.y_vel + self.kb_y) < 0:  # Hitting Ceiling
                    self.y = tile_rect.bottom
                    self.y_vel = 0
                    self.kb_y = 0
        if not self.on_ground:
            foot_check_rect = self.get_rect()
            foot_check_rect.y += 1 
            for tile_rect in tile_rects:
                if foot_check_rect.colliderect(tile_rect):
                    self.on_ground = True
                    break   

        # --- 3. Friction & Animation ---
        self.kb_x *= 0.8
        self.kb_y *= 0.9
        if self.kb_x < .1 and self.kb_x > 0 or self.kb_x > -.1 and self.kb_x < 0:
            self.kb_x = 0
        if self.kb_y < .1 and self.kb_y > 0 or self.kb_y > -.1 and self.kb_y < 0:
            self.kb_y = 0
            
        # Animation selection
        if not self.on_ground:
            self.frame = 9 # Falling frame
        elif self.moving:
            self.anim_timer += 0.15
            if self.anim_timer >= 1:
                self.anim_timer = 0
                self.frame = (self.frame % 8) + 1
        else:
            self.frame = 0

        # Advance attack frame
        if self.attacking:
            anim = [slash1, slash2, stab][self.attack_state - 1]
            self.attack_timer += dt
            if self.attack_timer >= 0.1:
                self.attack_timer = 0
                self.attack_frame += 1
                if self.attack_state == 3:
                    self.kb_x = p1.lunge_power if self.facing_right else -p1.lunge_power
                    self.kb_y = 1 if not self.on_ground else 0
                #reset
                if self.attack_frame >= len(anim):
                    self.attack_frame = 0
                    self.attacking = False
    def get_rect(self):
        return pygame.Rect(self.x+20*SCALE, self.y, (BW -40)* SCALE, BH * SCALE)

    def get_body(self):
        return body_frames[self.frame] if self.facing_right else body_frames_flipped[self.frame]

    def get_arms(self):
        if self.attacking:
            anim = [slash1, slash2, stab][self.attack_state - 1]
            idx = anim[min(self.attack_frame, len(anim)-1)]
        elif not self.on_ground:
            idx = 16
        elif self.moving:
            idx = self.frame % 8
        else:
            idx = 0
        return arms_frames[idx] if self.facing_right else arms_frames_flipped[idx]

    def get_attack_rect(self):
        if not self.attacking:
            return None
        body_width = (BW -40)* SCALE
        arm_width = 40*SCALE if self.attack_state == 3 else 25*SCALE
        arm_height = 15*SCALE if self.attack_state == 3 else 30*SCALE
        if self.facing_right:
            ax = self.x + body_width*1.5 # in front of player to the right
        else:
            ax = self.x if self.attack_state != 3 else self.x - 10*SCALE     # in front of player to the left
        ay = self.y + 10 * SCALE if self.attack_state != 3 else self.y + 20*SCALE
        return pygame.Rect(ax, ay, arm_width, arm_height)

    def draw(self, surface, camera_x, camera_y):
        offset_x = -12 if not self.facing_right else 0

        body = self.get_body()
        arms = self.get_arms()
        if self.last_hit <.1 and self.hit:
            harm_body = body.copy()
            harm_arms = arms.copy()
            harm_body.fill((self.harm), special_flags=pygame.BLEND_RGB_MAX)
            harm_arms.fill((self.harm), special_flags=pygame.BLEND_RGB_MAX)
            surface.blit(harm_body, (self.x - camera_x, self.y - camera_y))
            surface.blit(harm_arms, (self.x - camera_x + offset_x, self.y - 10 - camera_y))            
        else:   
            surface.blit(body, (self.x - camera_x, self.y - camera_y))
            surface.blit(arms, (self.x - camera_x + offset_x, self.y - 10 - camera_y))

class Enemy:
    def __init__(self, x, platform, patrol_left=200, patrol_right=500):
        self.x, self.y = x, platform-2*EH
        self.facing_right = True
        self.frame = 0
        self.anim_timer = 0
        self.speed = 0
        self.hp = 50
        self.hit = False
        self.last_hit = 0
        self.harm = WHITE

        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

        self.accel_frames = [0, 1]
        self.walk_frames  = [2, 3, 4, 5, 6]
        self.decel_frames = [1, 0]  # accel frames in reverse

        self.state = "accel"  # accel, walk, decel

    def take_hit(self, damage):
        self.hp -= damage
        if self.hp > 0:
            play_sound("enemy hit")
        else:
            play_sound("die")
        self.hit = True
        self.last_hit = 0
    def get_rect(self):
        return pygame.Rect(self.x+40, self.y+3, (EW * SCALE)-70, (EH * SCALE)+5)
    def update(self, dt):
        #hit timer
        if self.hit:
            self.last_hit += dt 
            if self.last_hit >= 0.5:
                self.hit = False
                self.last_hit = 0
        # Pick anim + speed based on state
        if self.state == "accel":
            self.speed = min(self.speed + 0.5, 3)
            anim = self.accel_frames
            if self.speed >= 3:
                self.state = "walk"
                self.frame = 0

        elif self.state == "walk":
            self.speed = 2
            anim = self.walk_frames
            # Start slowing down when close to boundary
            close_to_edge = (
                (self.facing_right and self.x >= self.patrol_right - 40) or
                (not self.facing_right and self.x <= self.patrol_left + 40)
            )
            if close_to_edge:
                self.state = "decel"
                self.frame = 0

        elif self.state == "decel":
            self.speed = max(self.speed - 0.5, 0)
            anim = self.decel_frames
            if self.speed == 0:
                self.facing_right = not self.facing_right
                self.state = "accel"
                self.frame = 0

        # Move
        self.x = self.x + self.speed if self.facing_right else self.x - self.speed

        # Animate
        self.anim_timer += 0.067 #67777
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.frame += 1
            if self.frame >= len(anim):
                self.frame = 0

    def draw(self, surface, camera_x, camera_y):
        if self.state == "accel":
            anim = self.accel_frames
        elif self.state == "walk":
            anim = self.walk_frames
        else:
            anim = self.decel_frames

        idx = anim[min(self.frame, len(anim) - 1)]
        img = enemy_frames[idx] if self.facing_right else enemy_frames_flipped[idx]

        if self.hit and self.last_hit < 0.1:
            img = img.copy()
            img.fill(self.harm, special_flags=pygame.BLEND_RGB_MAX)

        surface.blit(img, (self.x - camera_x, self.y - camera_y))

# --- Setup ---
p1 = Player()
#Enemy(random.randint(200,800), GROUND, patrol_left=random.randint(-100,200), patrol_right=random.randint(800,1000))
enemies = [
    Enemy(300, (len(grid) - 1) * TILE - (EH * SCALE), patrol_left=100, patrol_right=600),
    Enemy(200, (len(grid) - 1) * TILE - (EH * SCALE), patrol_left=0, patrol_right=700)
]
# --- Game loop ---
running = True
in_Game = True
tile_rects = get_tile_rects(grid)

while running:
    if in_Game:
        past_x = p1.x
        past_y = p1.y
        
        #delta time (converts frames to seconds by showing seconds per frame)
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            p1.handle_event(event)

        p1.update(dt, keys, tile_rects)
        if p1.x - camera_x < CAM_MARGIN_X:
            camera_x = p1.x - CAM_MARGIN_X
        elif p1.x - camera_x > WIDTH - CAM_MARGIN_X:
            camera_x = p1.x - (WIDTH - CAM_MARGIN_X)
        camera_y = p1.y - HEIGHT // 2

        # --- NEW: Clamp Camera to Map Edges ---
        # Keep X between 0 and (Map Width - Screen Width)
        camera_x = max(0, min(camera_x, map_width - WIDTH))

        for e in enemies:
            e.update(dt)

        screen.fill(SKY)
        # screen.blit(BG, (-.5*camera_x+TILE, -.5*camera_y))
        draw_tiles(screen, grid, camera_x, camera_y)

        if p1.last_hit >= .5:
            p1.hit = False
            p1.last_hit = 0
        if p1.hit:
            p1.last_hit += dt
        elif p1.kb_x == 0:
            for e in enemies:
                if e.hp > 0:
                    if p1.get_rect().colliderect(e.get_rect()):
                        play_sound("player hit")
                        p1.hit = True
                        p1.last_hit = 0
                        p1.hp-=10
                        # knock away from enemy
                        if p1.x > e.x:
                            p1.kb_x = p1.knockback_x   # knocked right
                        else:
                            p1.kb_x = -p1.knockback_x  # knocked left
                        if p1.on_ground:
                            p1.kb_y = -p1.knockback_y      # knocked upward      
        #attack hitbox
        attack_rect = p1.get_attack_rect()
        #if there was an attack, check for hits
        if attack_rect:
            for e in enemies:
                if e.hp > 0 and id(e) not in p1.hit_enemies:
                    if attack_rect.colliderect(e.get_rect()):
                        p1.hit_enemies.add(id(e))
                        if p1.attack_state == 3:
                            e.take_hit(20)
                        else:
                            e.take_hit(10)
                
        #calculates speed
        p1.max_speed = 0 if p1.max_speed == 128 else p1.max_speed
        p1.speed_x = abs(p1.x - past_x)
        p1.speed_y = abs(p1.y - past_y)
        p1.tot_speed = math.sqrt(p1.speed_x**2 + p1.speed_y**2)
        p1.max_speed = max(p1.max_speed, p1.tot_speed)
    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                p1.handle_event(event)        
            if event.type == pygame.QUIT:
                running = False

    # draws player and enemies
    for e in enemies:
        if e.hp > 0:
            e.draw(screen, camera_x, camera_y)
            if hitboxes:
                pygame.draw.rect(screen, RED, e.get_rect().move(-camera_x, -camera_y), 2)
    if hitboxes:
        pygame.draw.rect(screen, RED, p1.get_rect().move(-camera_x, -camera_y), 2)
    p1.draw(screen, camera_x, camera_y)
    if attack_rect and hitboxes:
        pygame.draw.rect(screen, CYAN, attack_rect.move(-camera_x, -camera_y), 2) if p1.attack_state != 3 else pygame.draw.rect(screen, GREEN, attack_rect.move(-camera_x, -camera_y), 2)

    #prints text
    cooldown = my_font.render(f'lunge cooldown: {p1.stab_cooldown:.1f} {p1.max_speed:.2f}', False, BLACK)
    screen.blit(cooldown, (30,80))
    hp = my_font.render(f'{p1.hp}', False, BLACK)
    pause = pause_font.render(f'PAUSED', True, BLACK)

    #healthbar (all me)
    pygame.draw.rect(screen, GRAY, pygame.Rect(30,30,5*p1.max_hp,50))
    pygame.draw.rect(screen, GREEN if p1.hp > 60  else ORANGE if p1.hp > 30 else RED, pygame.Rect(30,30,5*p1.hp,50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(30,30,5*p1.max_hp,50),5)
    screen.blit(hp, (40,33))
    if not in_Game:
        # screen.fill((255, 0, 0, 128))
        screen.blit(pause, (250,200))
    pygame.display.flip()
    if p1.hp <=0:
        break

pygame.quit()