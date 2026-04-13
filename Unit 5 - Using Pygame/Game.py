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
enemy_sheet.set_colorkey((0, 0, 0))
print(f"sheet width: {enemy_sheet.get_width()}, EW: {EW}, EH: {EH}")
body_frames = [pygame.transform.scale(body_sheet.subsurface((i*BW,0,BW,BH)), (BW*SCALE,BH*SCALE)) for i in range(BODY_FRAMES)]
arms_frames = [pygame.transform.scale(arms_sheet.subsurface((i*AW,0,AW,AH)), (AW*SCALE,AH*SCALE)) for i in range(ARM_FRAMES)]
enemy_frames = [pygame.transform.scale(enemy_sheet.subsurface((i*EW,0,EW,EH)), (AW*SCALE,AH*SCALE)) for i in range(ENEMY_FRAMES)]

# Attack animation indices
slash1 = [11, 12, 13]
slash2 = [14, 15]
stab   = [8, 9, 10]

GROUND = HEIGHT - (BH * SCALE) - 20


class Player:
    def __init__(self): #__init__ means initialize self is the characyer
        self.x, self.y = WIDTH // 2, GROUND
        self.speed = 4
        self.facing_right = True
        self.y_vel = 0
        self.on_ground = True
        self.moving = False

        self.frame = 0
        self.anim_timer = 0

        self.attacking = False
        self.attack_state = 0
        self.attack_frame = 0
        self.attack_timer = 0
        self.attack_reset_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.attacking:
            self.attack_state = (self.attack_state % 3) + 1
            self.attacking = True
            self.attack_frame = 0
            self.attack_timer = 0
            self.attack_reset_timer = 0

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
            self.y_vel = -10
            self.on_ground = False

        # Gravity
        self.y_vel += 0.5
        self.y += self.y_vel
        if self.y >= GROUND:
            self.y = GROUND
            self.y_vel = 0
            self.on_ground = True

        # Attack timer
        if self.attacking:
            self.attack_reset_timer += dt
            if self.attack_reset_timer > 0.6:
                self.attacking = False
                self.attack_state = 0

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
                if self.attack_frame >= len(anim):
                    self.attack_frame = 0
                    self.attacking = False

    def get_body(self):
        img = body_frames[self.frame]
        return pygame.transform.flip(img, True, False) if not self.facing_right else img

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
        img = arms_frames[idx]
        return pygame.transform.flip(img, True, False) if not self.facing_right else img

    def draw(self, surface):
        offset_x = -12 if not self.facing_right else 0
        surface.blit(self.get_body(), (self.x, self.y))
        surface.blit(self.get_arms(), (self.x + offset_x, self.y - 10))

class Enemy:
    def __init__(self, x, patrol_left=200, patrol_right=500):
        self.x, self.y = x, GROUND
        self.facing_right = True
        self.frame = 0
        self.anim_timer = 0
        self.speed = 0

        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

        self.accel_frames = [0, 1]
        self.walk_frames  = [2, 3, 4, 5, 6]
        self.decel_frames = [1, 0]  # accel frames in reverse

        self.state = "accel"  # accel, walk, decel

    def update(self, dt):
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
        if self.facing_right:
            self.x += self.speed
        else:
            self.x -= self.speed

        # Animate
        self.anim_timer += 0.067 #67777
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.frame += 1
            if self.frame >= len(anim):
                self.frame = 0

    def draw(self, surface):
        if self.state == "accel":
            anim = self.accel_frames
        elif self.state == "walk":
            anim = self.walk_frames
        else:
            anim = self.decel_frames

        idx = anim[min(self.frame, len(anim) - 1)]
        img = enemy_frames[idx]
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, (self.x, self.y))


# --- Setup ---
p1 = Player()
enemies = [Enemy(300, patrol_left=100, patrol_right=600), Enemy(200, patrol_left=0, patrol_right=700)]

# --- Game loop ---
running = True
while running:
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        p1.handle_event(event)

    p1.update(dt, keys)
    for e in enemies:
        e.update(dt)

    screen.fill((0, 200, 255))
    p1.draw(screen)
    for e in enemies:
        e.draw(screen)
    pygame.display.flip()

pygame.quit()