import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Character Demo")

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
CAM_MARGIN_X = 150
CAM_MARGIN_Y = 150

#colors
WHITE = (255,255,255)
SKY = (0, 200, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (250,150,20)
GRAY = (130,130,130)


#font
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

#sets up frames
enemy_sheet.set_colorkey((0, 0, 0))
body_frames = [pygame.transform.scale(body_sheet.subsurface((i*BW,0,BW,BH)), (BW*SCALE,BH*SCALE)) for i in range(BODY_FRAMES)]
arms_frames = [pygame.transform.scale(arms_sheet.subsurface((i*AW,0,AW,AH)), (AW*SCALE,AH*SCALE)) for i in range(ARM_FRAMES)]
enemy_frames = [pygame.transform.scale(enemy_sheet.subsurface((i*EW,0,EW,EH)), (AW*SCALE,AH*SCALE)) for i in range(ENEMY_FRAMES)]

#flipped frames
body_frames_flipped = [pygame.transform.flip(f, True, False) for f in body_frames]
arms_frames_flipped = [pygame.transform.flip(f, True, False) for f in arms_frames]
enemy_frames_flipped = [pygame.transform.flip(f, True, False) for f in enemy_frames]

# Attack animation indices
slash1 = [11, 12, 13]
slash2 = [14, 15]
stab   = [8, 9, 10]

GROUND = HEIGHT - (BH * SCALE) - 150


class Player:
    def __init__(self): #__init__ means initialize self is the characyer
        self.x, self.y = WIDTH // 2, GROUND
        self.speed = 4
        self.max_xspeed = 0
        self.facing_right = True
        self.y_vel = 0
        self.on_ground = True
        self.moving = False
        self.hit = False
        self.last_hit = 0
        self.hit_enemies = set()
        self.kb_x = 0
        self.kb_y = 0
        self.hp = 100
        self.harm = RED
        self.stab_cooldown = 0

        self.frame = 0
        self.anim_timer = 0

        self.attacking = False
        self.attack_state = 0
        self.attack_frame = 0
        self.attack_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.attacking:
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and self.stab_cooldown == 0:
            self.attack_state = 3
            self.attacking = True
            self.attack_frame = 0
            self.attack_timer = 0
            self.stab_cooldown = 1.5
            self.hit_enemies = set()
    def update(self, dt, keys):
        # Movement
        self.moving = False
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.x -= self.speed
            self.facing_right = False
            self.moving = True
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.x += self.speed
            self.facing_right = True
            self.moving = True

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.y_vel = -13.5
            self.on_ground = False

        # Gravity
        self.y_vel += 0.5
        self.y += self.y_vel
        if self.y >= GROUND:
            self.y = GROUND
            self.y_vel = 0
            self.on_ground = True

        # Knockback
        self.x += self.kb_x
        self.y += self.kb_y
        self.kb_x *= .8  # friction, lower = slides further
        self.kb_y *= .9
        if abs(self.kb_x) < 0.1: self.kb_x = 0
        if abs(self.kb_y) < 0.1: self.kb_y = 0

        if self.stab_cooldown > 0:
            self.stab_cooldown = max(0, self.stab_cooldown - dt)    

        # Body frame
        if not self.on_ground:
            self.frame = 9
        elif self.moving:
            if self.frame in (0, 9):
                self.frame = 1
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
                    self.kb_x = 10 if self.facing_right else -10
                    self.kb_y = 1 if not self.on_ground else 0
                #reset
                if self.attack_frame >= len(anim):
                    self.attack_frame = 0
                    self.attacking = False

    def get_rect(self):
        return pygame.Rect(self.x+40, self.y, (BW * SCALE)-80, BH * SCALE)

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
        arm_width = 40
        arm_height = 30
        if self.facing_right:
            ax = self.x + (BW * SCALE) - 20  # in front of player to the right
        else:
            ax = self.x - arm_width + 20     # in front of player to the left
        ay = self.y + 20
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
        self.x, self.y = x, platform-5
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
enemies = [Enemy(300, GROUND, patrol_left=100, patrol_right=600), Enemy(200, GROUND, patrol_left=0, patrol_right=700)]

# --- Game loop ---
running = True
while running:
    past_x = p1.x
    past_y = p1.y
    #delta time (converts frames to seconds by showing seconds per frame)
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        p1.handle_event(event)

    p1.update(dt, keys)

    target_x = p1.x - WIDTH // 2
    if p1.x - camera_x < CAM_MARGIN_X:
        camera_x = p1.x - CAM_MARGIN_X
    elif p1.x - camera_x > WIDTH - CAM_MARGIN_X:
        camera_x = p1.x - (WIDTH - CAM_MARGIN_X)
    camera_y = p1.y - HEIGHT // 2
    for e in enemies:
        e.update(dt)

    screen.fill((SKY))
    if p1.last_hit >= .5:
        p1.hit = False
        p1.last_hit = 0
    if p1.hit:
        p1.last_hit += dt
    elif p1.kb_x == 0:
        for e in enemies:
            if e.hp > 0:
                if p1.get_rect().colliderect(e.get_rect()):
                    p1.hit = True
                    p1.last_hit = 0
                    p1.hp-=10
                    # knock away from enemy
                    if p1.x > e.x:
                        p1.kb_x = 8   # knocked right
                    else:
                        p1.kb_x = -8  # knocked left
                    if p1.on_ground:
                        p1.kb_y = -6      # knocked upward      
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
    speed_x = max(p1.x - past_x, past_x - p1.x)
    speed_y = max(p1.y - past_y, past_y - p1.y)
    p1.max_xspeed = max(speed_x, p1.max_xspeed)
    
    # draws player and enemies
    for e in enemies:
        if e.hp > 0:
            e.draw(screen, camera_x, camera_y)
            pygame.draw.rect(screen, (255, 0, 0), e.get_rect().move(-camera_x, -camera_y), 2)
    pygame.draw.rect(screen, (255, 0, 0), p1.get_rect().move(-camera_x, -camera_y), 2)
    p1.draw(screen, camera_x, camera_y)
    if attack_rect:
        pygame.draw.rect(screen, (0, 255, 255), attack_rect.move(-camera_x, -camera_y), 2)

    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,GROUND - camera_y+128,WIDTH,200))

    #prints text
    # camera = my_font.render(f'camera x = {int(camera_x)} camera y = {int(camera_y)}', False, (0, 0, 0))
    # screen.blit(camera, (30,120))
    # speed = my_font.render(f'speed x = {int(speed_x)} speed y = {int(speed_y)} max x speed = {int(p1.max_xspeed)}', False, (0, 0, 0))
    # screen.blit(speed, (30,180))
    cooldown = my_font.render(f'lunge cooldown: {p1.stab_cooldown:.1f}', False, (0, 0, 0))
    screen.blit(cooldown, (30,80))
    hp = my_font.render(f'{p1.hp}', False, (0, 0, 0))

    #healthbar (all me)
    pygame.draw.rect(screen, GRAY, pygame.Rect(30,30,500,50))
    pygame.draw.rect(screen, GREEN if p1.hp > 60  else ORANGE if p1.hp > 30 else RED, pygame.Rect(30,30,5*p1.hp,50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(30,30,500,50),5)
    screen.blit(hp, (40,33))
    pygame.display.flip()
    if p1.hp <=0:
        break

pygame.quit()