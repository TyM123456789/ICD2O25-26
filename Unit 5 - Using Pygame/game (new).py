#start screen started, fix "Play" and add controls, phase 3

import pygame, random, math
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("EYE SEE YOU")
#setup sound
pygame.mixer.init()
jump = [pygame.mixer.Sound("jump.wav"), pygame.mixer.Sound("jump2.wav")]
hit_s = [pygame.mixer.Sound("hit1.wav"), pygame.mixer.Sound("hit2.wav")]
pause_s = [pygame.mixer.Sound("pause sound.wav"), pygame.mixer.Sound("pause2.wav")]
die_s = [pygame.mixer.Sound("die.wav"),pygame.mixer.Sound("die2.wav"), pygame.mixer.Sound("die3.wav")]
upgrade_s = [pygame.mixer.Sound("upgrade1.wav"), pygame.mixer.Sound("upgrade2.wav")]
player_hit_s = [pygame.mixer.Sound("player hit.wav"), pygame.mixer.Sound("player hit2.wav")]
slash_s = [pygame.mixer.Sound("SWORD 1.mp3"), pygame.mixer.Sound("SWORD 3 (non-brutal).mp3")]
stab_s = [pygame.mixer.Sound("SWORD 2 (brutal).mp3"), pygame.mixer.Sound("SWORD 4 (metal).mp3")]
player_die_s = [pygame.mixer.Sound("player die.wav")]
laser_charge_s = pygame.mixer.Sound("laser charge.mp3")
laser_sound = pygame.mixer.Sound("laser shoot.mp3")
laser_sound.set_volume(.5)


pygame.mixer.music.set_volume(0.5)
# --- Load assets ---
body_sheet = pygame.image.load("Walking.png").convert_alpha()
arms_sheet = pygame.image.load("arms.png").convert_alpha()
enemy1_sheets = [pygame.image.load("Enemy.png").convert_alpha(), pygame.image.load("the scary guy.png").convert_alpha()]
medkit_sheet = pygame.image.load("medkit.png").convert_alpha()
boss_sheet = pygame.image.load("the REAL RELA eye 1.png").convert_alpha()

SCALE = 2

BODY_FRAMES = 10
ARM_FRAMES = 17
ENEMY_FRAMES = 7
MEDKIT_FRAMES = 5
BOSS_FRAMES = 8
BW = body_sheet.get_width() // BODY_FRAMES
BH = body_sheet.get_height()
AW = arms_sheet.get_width() // ARM_FRAMES
AH = arms_sheet.get_height()
EW = enemy1_sheets[0].get_width() // ENEMY_FRAMES
EH = enemy1_sheets[0].get_height()
MW = medkit_sheet.get_width() // MEDKIT_FRAMES
MH = medkit_sheet.get_height()
BOSSW = boss_sheet.get_width() // BOSS_FRAMES
BOSSH = boss_sheet.get_height()

#colors
WHITE = (255,255,255)
SKY = (1, 183, 238)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (250,150,20)
GRAY = (130,130,130)
CYAN = (0,255,255)

#font
comic_sans = 'Comic Sans MS'
arial = 'Arial'

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
spawn_font = pygame.font.SysFont('Comic Sans MS', 40)
wave_timer_font = pygame.font.SysFont('Comic Sans MS', 60)
pause_font = pygame.font.SysFont('Comic Sans MS', 80)
button_font = pygame.font.Font('GalaferaMedium.ttf', 80)
button_hover_font = pygame.font.Font('GalaferaMediumItalic.ttf', 80)
title_font = pygame.font.Font('GalaferaMedium.ttf', 105)

#sets up frames
enemy1_sheets[0].set_colorkey((0, 0, 0))
body_frames = [pygame.transform.scale(body_sheet.subsurface((i*BW,0,BW,BH)), (BW*SCALE,BH*SCALE)) for i in range(BODY_FRAMES)]
arms_frames = [pygame.transform.scale(arms_sheet.subsurface((i*AW,0,AW,AH)), (AW*SCALE,AH*SCALE)) for i in range(ARM_FRAMES)]
enemy_frames = [
    [pygame.transform.scale(enemy1_sheets[x].subsurface((i*EW,0,EW,EH)), (EW*SCALE,EH*SCALE)) for i in range(ENEMY_FRAMES)]
    for x,y in enumerate(enemy1_sheets)
    ]
medkit_frames = [pygame.transform.scale(medkit_sheet.subsurface((i*MW,0,MW,MH)), (MW*SCALE,MH*SCALE)) for i in range(MEDKIT_FRAMES)]
boss_frames = [pygame.transform.scale(boss_sheet.subsurface((i*BOSSW,0,BOSSW,BOSSH)), (BOSSW*SCALE*1.5,BOSSH*SCALE*1.5)) for i in range(BOSS_FRAMES)]
boss_frames = [pygame.transform.flip(f, True, False) for f in boss_frames]


#flipped frames
body_frames_flipped = [pygame.transform.flip(f, True, False) for f in body_frames]
arms_frames_flipped = [pygame.transform.flip(f, True, False) for f in arms_frames]
boss_frames_flipped = [pygame.transform.flip(f, True, False) for f in boss_frames]
enemy_frames_flipped = [[pygame.transform.flip(x, True, False) for x in f]for f in enemy_frames]

# Attack animation indices
slash1 = [11, 12, 13]
slash2 = [14, 15]
stab   = [8, 9, 10]

TILE = 32 * SCALE
GROUND = (36 - 1) * TILE - (BH * SCALE) #sixteen is the place on the ground, -1 because index
BG = pygame.transform.scale(pygame.image.load("backgroundv.2.png"), (800*4, 600*4))

tiles = [
    "",
    pygame.transform.scale(pygame.image.load("blue dark tile.png"), (TILE, TILE)),
    pygame.transform.scale(pygame.image.load("blue light tile.png"), (TILE, TILE))
]

wave_timer = -1
wave_num = 5

def get_grid(map):
    grid = []
    with open(map) as f:
        for line in f:
            row = [int(ch) for ch in line.strip()]
            grid.append(row)
    tile_rects = get_tile_rects(grid)
    map_height = len(grid) * TILE
    map_width = len(grid[0]) * TILE
    return grid, tile_rects, map_height, map_width

def draw_tiles(grid, camera):
    x=0
    y=0
    camera_rect = camera.get_rect()
    for row_i, row in enumerate(grid): 
        y=-camera.y
        for col_i, tile in enumerate(row):
            if tile != 0:
                x = col_i * TILE - camera.x
                y = row_i * TILE - camera.y

                screen.blit (tiles[tile], (x,y))

def get_tile_rects(grid):
    rects = []
    for row_i, row in enumerate(grid):
        for col_i, tile in enumerate(row):
            if tile != 0:
                rects.append(pygame.Rect(col_i * TILE, row_i * TILE, TILE, TILE))
    return rects

def play_sound(type):
    if type == "die":
        die_s[random.randint(0, len(die_s) -1)].play()
    if type == "enemy hit":
        hit_s[random.randint(0, len(hit_s) -1)].play()
    if type == "player hit":
        player_hit_s[random.randint(0, len(player_hit_s) -1)].play()
    if type == "pause_s":
        pause_s[random.randint(0, len(pause_s) -1)].play()
    if type == "jump":
        jump[random.randint(0, len(jump) -1)].play()
    if type == "upgrade":
        upgrade_s[random.randint(0, len(upgrade_s)-1)].play()
    if type == "slash":
        slash_s[random.randint(0, len(slash_s) -1)].play()
    if type == "stab":
        stab_s[random.randint(0, len(stab_s) -1)].play()
    if type == "player die":
        player_die_s[random.randint(0, len(player_die_s) -1)].play()


def add_enemies(enemy_list, amount):
    #if you input a decimal amount, the extra decimal will be the chance for a second enemy to spawn
    if amount - int(amount) != 0:
        chance = (amount - int(amount))*100
    else:
        chance = 0
    amount = int(amount)
    for index, rows in enumerate(grid):
        extra = random.randint(0,100) <= chance and chance != 0
        if extra:
            amount +=1
        for x in range(amount):
            if "1" in str(rows):
                enemy_list.append(Enemy(False, random.randint(0,len(enemy1_sheets)-1), random.randint(int(len(rows)*.4),int(len(rows)*.6))*TILE, (index+2) * TILE - (EH * SCALE), patrol_left=random.randint(int(len(rows)*.1),int(len(rows)*.4))*TILE, patrol_right=random.randint(int(len(rows)*.6),int(len(rows)*.9))*TILE))
        if extra:
            amount -= 1
    return enemy_list

def add_boss(enemy_list):
    enemy_list.append(Enemy(True, boss_frames, 0, 2, patrol_left=0, patrol_right=0))
    return enemy_list

def spawn_wave(enemy_list, wave):
    if wave != 5:
        enemy_list = add_enemies(enemy_list, .5 + (.5*wave))
    elif wave_num == 5:
        enemy_list = add_boss(enemy_list)
    return enemy_list

def text_to_screen(text, font, color, x, y):
    textt = font.render(text, False, color)
    screen.blit(textt, (x, y))

Spawn_text = []
spawn_text_timer = 1.5

#creates text that shows when upgrades spawn
def spawn_text(type, font, color):
    Spawn_text.append(font.render(f'A {type} has spawned!', False, color))


# ─────────────────────────────────────────────────────────────────────────────
# LASER CLASS
# Represents a vertical laser beam that telegraphs before firing.
# Lasers are stored in the global `lasers` list and drawn after all world
# objects but before the UI so they always appear on top of terrain/enemies.
# ─────────────────────────────────────────────────────────────────────────────
class Laser:
    WARNING_DURATION = .7
    ACTIVE_DURATION  = 1.5
    BEAM_WIDTH       = 40
    DAMAGE           = 1

    def __init__(self, x, angle=90, warning=True, permanent=False, sound=True):
        self.x       = x
        self.angle   = angle      # 90 = vertical, other angles tilt the beam
        self.warning = warning    # False = skip straight to active
        self.permanent = permanent # True = never turns off
        self.sound   = sound
        self.timer   = 0.0
        self.state   = "warning" if warning else "active"

    def update(self, dt):
        self.timer += dt

        if self.state == "warning":
            if self.sound:
                laser_charge_s.play()
            if self.timer >= self.WARNING_DURATION:
                laser_charge_s.stop()
                self.state = "active"
                self.timer = 0.0

        elif self.state == "active":
            if self.sound:
                laser_sound.play()

            beam_rect = self._get_beam_rect()
            if beam_rect.colliderect(p1.get_rect()):
                p1.hp -= self.DAMAGE
                if p1.hp > 0:
                    play_sound("player hit")

            if not self.permanent and self.timer >= self.ACTIVE_DURATION:
                if self.sound:
                    laser_sound.stop()
                self.state = "done"

    def _get_beam_rect(self):
        # For a vertical laser this is the same as before.
        # For angled lasers we use a bounding box — good enough for collision.
        if self.angle == 90:
            return pygame.Rect(self.x - self.BEAM_WIDTH // 2, 0, self.BEAM_WIDTH, map_height)
        
        # Compute where the angled line intersects the top and bottom of the map
        rad = math.radians(self.angle)
        # How far does x shift as we travel the full map height?
        x_span = map_height / math.tan(rad) if math.tan(rad) != 0 else 0
        x_min = min(self.x, self.x + x_span)
        x_max = max(self.x, self.x + x_span)
        return pygame.Rect(x_min - self.BEAM_WIDTH // 2, 0, 
                           (x_max - x_min) + self.BEAM_WIDTH, map_height)

    def _get_beam_points(self, camera):
        # Returns (top_screen_x, bottom_screen_x) for drawing the angled beam
        rad = math.radians(self.angle)
        x_span = map_height / math.tan(rad) if math.tan(rad) != 0 else 0
        top_x    = int(self.x - camera.x)
        bottom_x = int(self.x + x_span - camera.x)
        return top_x, bottom_x

    def draw(self, surface, camera):
        top_x, bottom_x = self._get_beam_points(camera)

        if self.state == "warning":
            pulse = 0.5 + 0.5 * math.sin(self.timer * 10)
            color = (255, int(80 + 120 * pulse), 0)
            pygame.draw.line(surface, color, (top_x, 0), (bottom_x, HEIGHT), int(self.BEAM_WIDTH / 2))
            pygame.draw.rect(surface, color, pygame.Rect(bottom_x - 6, HEIGHT - 16, 12, 16))

        elif self.state == "active":
            pygame.draw.line(surface, (255, 200, 200), (top_x, 0), (bottom_x, HEIGHT), self.BEAM_WIDTH + 8)
            pygame.draw.line(surface, (255, 50, 50),   (top_x, 0), (bottom_x, HEIGHT), self.BEAM_WIDTH)

class Player:
    def __init__(self): #__init__ means initialize self is the characyer
        self.x, self.y = WIDTH // 2, GROUND
        self.speed = 4
        self.max_speed = 0
        self.facing_right = True
        self.y_vel = 0
        self.on_ground = False
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
        self.damage_dealt = 0
        self.healed = 0


        self.slashes = 0
        self.stabs = 0
        self.score = 0
        self.attacking = False
        self.attack_state = 0
        self.attack_frame = 0
        self.attack_timer = 0
        self.attack_speed = .1

    def handle_event(self, event):
        #event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.attacking:
            play_sound("slash")
            # cycle between slash1 and slash2
            if self.attack_state == 1:
                self.slashes +=1
                self.attack_state = 2
            else:
                self.slashes+=1
                self.attack_state = 1
            self.attacking = True
            self.attack_frame = 0
            self.attack_timer = 0
            self.hit_enemies = set()

        # Stab
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and self.stab_cooldown <= 0.07:
            play_sound("stab")
            self.stabs+=1
            self.attack_state = 3
            self.attacking = True
            self.attack_frame = 0
            self.attack_timer = 0
            self.stab_cooldown = 1.2
            self.hit_enemies = set()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            global hitboxes
            hitboxes = not hitboxes
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not win and not dead:
            global in_Game, paused, grid, tile_rects, map_height, map_width
            #grid, tile_rects, map_height, map_width = get_grid("map2.tile")
            play_sound("pause_s")
            paused = not paused
            if paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            in_Game = not in_Game

        # Jump Start
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.on_ground:
                play_sound("jump")
                self.y_vel = p1.jump  # Initial jump burst
                self.on_ground = False

                # Variable Jump: If they let go of Space while moving up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                if self.y_vel < -3: # If still moving upward significantly
                    self.y_vel = -3 # "Cut" the jump velocity

    def update(self, dt, keys, tile_rects):
        #stab cooldown
        p1.stab_cooldown -=dt
        if p1.stab_cooldown <= 0:
            p1.stab_cooldown = 0
        # --- 1. Horizontal Movement & Collision ---
        self.moving = False
        dx = 0
        if keys[pygame.K_a] and not (self.attacking and self.attack_state == 3 and self.facing_right) and not keys[pygame.K_d]:
            dx -= self.speed
            self.facing_right = False
            self.moving = True
        if keys[pygame.K_d] and not (self.attacking and self.attack_state == 3 and not self.facing_right) and not keys[pygame.K_a]:
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
        if not self.on_ground:
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
            self.anim_timer += dt
            if self.anim_timer >= .13:
                self.anim_timer = 0
                self.frame = (self.frame % 8) + 1
        else:
            self.frame = 0

        # Advance attack frame
        if self.attacking:
            anim = [slash1, slash2, stab][self.attack_state - 1] 
            self.attack_timer += dt
            #attack animation speed
            if self.attack_timer >= self.attack_speed:
                self.attack_timer = 0
                self.attack_frame += 1
                if self.attack_state == 3:
                    #pushes the player in direction their facing
                    self.kb_x = p1.lunge_power if self.facing_right else -p1.lunge_power
                    #pushing the player up when lunging on the ground helps increase distance but is otherwise unnecessary (this one line was coded by me)
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
        #changes hitboxes if lunging vs if slashing
        arm_width = 40*SCALE if self.attack_state == 3 else 25*SCALE
        arm_height = 15*SCALE if self.attack_state == 3 else 30*SCALE
        if self.facing_right:
            ax = self.x + body_width*1.5 # in front of player to the right
        else:
            ax = self.x if self.attack_state != 3 else self.x - 10*SCALE     # in front of player to the left
        ay = self.y + 10 * SCALE if self.attack_state != 3 else self.y + 20*SCALE
        return pygame.Rect(ax, ay, arm_width, arm_height)

    def draw(self, surface, camera):
        offset_x = -12 if not self.facing_right else 0

        body = self.get_body()
        arms = self.get_arms()
        if self.last_hit <.1 and self.hit:
            harm_body = body.copy()
            harm_arms = arms.copy()
            harm_body.fill((self.harm), special_flags=pygame.BLEND_RGB_MAX)
            harm_arms.fill((self.harm), special_flags=pygame.BLEND_RGB_MAX)
            surface.blit(harm_body, (self.x - camera.x, self.y - camera.y))
            surface.blit(harm_arms, (self.x - camera.x + offset_x, self.y - 10 - camera.y))            
        else:   
            surface.blit(body, (self.x - camera.x, self.y - camera.y))
            surface.blit(arms, (self.x - camera.x + offset_x, self.y - 10 - camera.y))

class Enemy:
    def __init__(self, is_Boss, type, x, platform, patrol_left=200, patrol_right=500):
        self.is_Boss = is_Boss
        if not self.is_Boss:
            self.x, self.y = x, platform-2*EH
        else:
            self.x = WIDTH - BOSSW/2 +600
            self.y = 1280
        self.facing_right = True
        self.frame = 0
        self.anim_timer = 0
        self.speed = 0
        self.hit = False
        self.last_hit = 0
        self.harm = WHITE
        self.dam = 10
        self.max_speed = random.randint(15,25)/10
        self.prev_state = "accel"

        self.type = type

        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

        if not is_Boss:
            self.hp = 50
            self.dam = 10
            self.accel_frames = [0, 1]
            self.walk_frames  = [0, 2, 3, 4, 5, 6]
            self.decel_frames = [1, 0]  # accel frames in reverse

            self.state = "accel"  # accel, walk, decel
            self.laser_round_state = "noo" #nromal enemies cant fire lasers
        else:
            self.phase = 1
            self.max_hp = 800
            self.hp = self.max_hp
            self.dam = 20
            frames = [range(BOSS_FRAMES)]

            self.vx               = 0.0    # current horizontal velocity (px/s)
            self.vy               = 0.0    # current vertical velocity (px/s)
            self.push_timer       = 0.0    # drives the oscillating speed rhythm
            self.base_speed       = 200.0  # max speed; increases after laser phase
            self.phase2_entered   = False  # True once phase 2 setup has run
            self.retreating       = False  # True while boss flies back to spawn
            self.start_x          = self.x # original spawn X (used for retreat)
            self.start_y          = self.y # original spawn Y
            self.laser_round      = 0      # how many laser rounds have completed
            self.max_laser_rounds = 5     # total laser rounds before speed boost
            # "idle"     → not yet in laser phase
            # "warning"  → lasers are showing the warning line
            # "active"   → lasers are firing
            # "cooldown" → brief pause between rounds
            # "done"     → all rounds finished, back to chasing
            self.laser_round_state    = "idle"
            self.laser_cooldown_timer = 0.0  # timer between laser rounds
            self.speed_boosted        = False # True once we've applied the boost


    def take_hit(self, damage):
        self.hp -= damage
        p1.damage_dealt += damage
        if self.hp > 0:
            play_sound("enemy hit")
        else:
            p1.score+=1
            play_sound("die")
        self.hit = True
        self.last_hit = 0
    
    def get_rect(self):
        if not self.is_Boss:
            return pygame.Rect(self.x + 40, self.y + 3, (EW * SCALE) - 75, (EH * SCALE) + 5)
        else:
            return pygame.Rect((self.x+70), self.y+70, BOSSW * SCALE-50, BOSSH * SCALE-50)

    # ── Boss helper: spawn evenly-spaced lasers across the full map ──────────
    def _spawn_lasers(self):
        """Create vertical Laser objects spread across the map width.
        The gaps between lasers are the safe zones the player must dodge into."""
        global lasers
        lasers.clear()
        num_lasers = 20  # number of beams per round
        # Divide the map into (num_lasers + 1) equal segments so the beams
        # land at the segment boundaries, leaving wide safe corridors between them.
        offset = random.randint(0,100)
        for i in range(1, num_lasers + 1):
            world_x = int(map_width * i / (num_lasers + 1))
            lasers.append(Laser(world_x+offset, angle=90, warning=True, permanent=False, sound=True))

    def update(self, dt):

        self.new_facing_right = self.facing_right
        #hit timer
        if self.hit:
            self.last_hit += dt 
            if self.last_hit >= 0.5:
                self.hit = False
                self.last_hit = 0
        if not self.is_Boss:
            # Pick anim + speed based on state (this part is probably half ai generated because i got bored)

            close_to_player = abs(self.y - p1.y) < 150 and abs(self.x - p1.x) < 600

            if not close_to_player and self.state == "following":
                self.state = "accel"
            if self.state == "decel":
                self.speed = max(self.speed - 0.5, 0)
                anim = self.decel_frames
                if self.speed == 0:
                    if self.prev_state == "following":
                        self.new_facing_right = self.x < p1.x
                        self.state = "following"
                    else:
                        self.new_facing_right = not self.facing_right
                        self.state = "accel"
                    self.frame = 0

            elif close_to_player:
                self.state = "following"
                self.speed = self.max_speed * 1.25 if self.x != p1.x else 0
                anim = self.walk_frames
                self.new_facing_right = self.x < p1.x
                if self.facing_right != self.new_facing_right:
                    self.prev_state = "following"
                    self.state = "decel"
                    self.frame = 0

            elif self.state == "accel":
                self.speed = min(self.speed + 0.5, self.max_speed)
                anim = self.accel_frames
                if self.speed >= 3:
                    self.state = "walk"
                    self.frame = 0
                close_to_edge = (
                (self.new_facing_right and self.x >= self.patrol_right - 40) or
                (not self.new_facing_right and self.x <= self.patrol_left + 40)
                )
                if close_to_edge:
                    self.prev_state = "accel"
                    self.state = "decel"
                    self.frame = 0
                elif self.speed >= self.max_speed:
                    self.state = "walk"
                    self.frame = 0

            elif self.state == "walk":
                self.speed = self.max_speed
                anim = self.walk_frames
                close_to_edge = (
                    (self.new_facing_right and self.x >= self.patrol_right - 40) or
                    (not self.new_facing_right and self.x <= self.patrol_left + 40)
                )
                if close_to_edge:
                    self.prev_state = "walk"
                    self.state = "decel"
                    self.frame = 0

            elif self.state == "following":
                self.speed = self.max_speed * 1.25 if self.x != p1.x else 0
                anim = self.walk_frames
                self.new_facing_right = self.x < p1.x
                if self.facing_right != self.new_facing_right:
                    self.prev_state = "following"
                    self.state = "decel"
                    self.frame = 0

            # Move
            self.x = self.x + self.speed if self.new_facing_right else self.x - self.speed

            # Animate
            self.anim_timer += dt #67777
            if self.anim_timer >= 1/3:
                if self.facing_right != self.new_facing_right:
                    self.anim_timer = 0
                    self.frame = 0
                else:
                    self.anim_timer = 0
                    self.frame += 1
                    if self.frame >= len(anim):
                        self.frame = 1
            self.facing_right = self.new_facing_right
        else:
            # ── Boss always faces the player ─────────────────────────────────
            self.facing_right = True if self.x < p1.x else False



            # ── Phase 2 entry: triggered at half health ───────────────────────
            if self.hp <= self.max_hp//2 and not self.phase2_entered:
                self.phase          = 2
                self.phase2_entered = True
                self.retreating     = True   # start flying back to origin

            # ── RETREAT: boss flies back to its starting position ─────────────
            if self.retreating:
                dx   = self.start_x - self.x
                dy   = self.start_y - self.y
                dist = math.sqrt(dx*dx + dy*dy) or 1

                # Move quickly back; 200 px/s feels purposeful without teleporting
                retreat_speed = 200.0
                self.x += (dx / dist) * retreat_speed * dt
                self.y += (dy / dist) * retreat_speed * dt

                # Close enough → snap and start the first laser round
                if dist < 20:
                    self.x, self.y         = self.start_x, self.start_y
                    self.retreating        = False
                    self.laser_round       = 0
                    self.laser_round_state = "warning"
                    self._spawn_lasers()   # fill global `lasers` list

                # Animate during retreat
                self.anim_timer += dt
                if self.anim_timer >= 1 / 8:
                    self.anim_timer = 0
                    self.frame += 1

            # ── LASER PHASE: manage rounds of laser attacks ───────────────────
            elif self.laser_round_state in ("warning", "active", "cooldown"):
                global lasers

                if self.laser_round_state == "warning":
                    # Wait for every laser to leave warning (i.e., it has fired or finished)
                    if all(l.state in ("active", "done") for l in lasers):
                        self.laser_round_state = "active"

                elif self.laser_round_state == "active":
                    # Wait for every laser beam to finish firing
                    if all(l.state == "done" for l in lasers):
                        self.laser_round += 1

                        if self.laser_round >= self.max_laser_rounds:
                            # All rounds done: clear beams, speed up, resume chasing
                            lasers.clear()
                            self.laser_round_state = "done"
                            if not self.speed_boosted:
                                # Significant speed boost makes the final chase dangerous
                                self.base_speed    *= 1.5
                                self.speed_boosted = True
                        else:
                            # Short pause before spawning the next laser round
                            self.laser_round_state    = "cooldown"
                            self.laser_cooldown_timer = 1.5

                elif self.laser_round_state == "cooldown":
                    self.laser_cooldown_timer -= dt
                    if self.laser_cooldown_timer <= 0:
                        # Spawn fresh lasers and go back to warning state
                        self._spawn_lasers()
                        self.laser_round_state = "warning"

                # Boss bobs gently in place during the laser attack instead of chasing
                self.push_timer += dt
                self.y = self.start_y + math.sin(self.push_timer * 3) * 12

                # Animate
                self.anim_timer += dt
                if self.anim_timer >= 1 / 8:
                    self.anim_timer = 0
                    self.frame += 1

            # ── NORMAL MOVEMENT: Phase 1 chasing and post-laser Phase 2 ───────
            else:
                self.push_timer += dt

                # abs(sin) produces a natural 0→1→0 oscillation.
                # Offset by 0.15 so the boss never fully stops — it always
                # drifts a little, then surges, then drifts again, like it's
                # pushing itself through a thick medium.
                speed_mult = 0.15 + 0.85 * abs(math.sin(self.push_timer * 1.5))

                # Direction vector from boss to player
                dx   = p1.x - self.x
                dy   = p1.y - self.y-100
                dist = math.sqrt(dx*dx + dy*dy) or 1

                # Compute the velocity we'd like to have this frame
                target_vx = (dx / dist) * self.base_speed * speed_mult
                target_vy = (dy / dist) * self.base_speed * speed_mult

                # Smoothly interpolate current velocity toward the target.
                # A small lerp factor (0.07) gives the floaty, inertia-heavy
                # feel of something pushing through air rather than snapping to speed.
                lerp = 0.07
                self.vx += (target_vx - self.vx) * lerp
                self.vy += (target_vy - self.vy) * lerp

                # Apply velocity
                self.x += self.vx * dt
                self.y += self.vy * dt

                # Animate
                self.anim_timer += dt
                if self.anim_timer >= 1 / 8:
                    self.anim_timer = 0
                    self.frame += 1

    def draw(self, surface, camera):
        if not self.is_Boss:
            anim = self.walk_frames

            idx = anim[min(self.frame, len(anim) - 1)]
            img = enemy_frames[self.type][idx] if self.facing_right else enemy_frames_flipped[self.type][idx]

            if self.hit and self.last_hit < 0.1:
                img = img.copy()
                img.fill(self.harm, special_flags=pygame.BLEND_RGB_MAX)

            surface.blit(img, (self.x - camera.x, self.y - camera.y))
        else:
            img = boss_frames[self.frame%BOSS_FRAMES - 1] if self.facing_right else boss_frames_flipped[self.frame%BOSS_FRAMES - 1]

            if self.hit and self.last_hit < 0.1:
                img = img.copy()
                img.fill(self.harm, special_flags=pygame.BLEND_RGB_MAX)

            surface.blit(img, (self.x - camera.x, self.y - camera.y))

class Upgrade:
    def __init__(self, type, spawn_timer):
        self.type = type
        self.frame = 0
        self.anim_timer = 0
        self.spawn_timer = spawn_timer

        self.x = 0
        self.y = 0

        #medkit
        self.medkit_heal = 40
        if self.type == "medkit":
            self.spawn_timer += 10

    def update(self,dt, grid):
        self.anim_timer += dt
        if self.anim_timer >= .2:
            self.frame +=1
            self.anim_timer = 0

        if self.spawn_timer >0:
            self.spawn_timer -= dt
        elif self.x == 0 and self.y == 0:
            spawn_text("medkit", spawn_font, GREEN)
            self.spawn(grid)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, (MW * SCALE), (MH * SCALE))

    def touch(self):
        play_sound("upgrade")
        if self.type == "medkit":
            p1.healed += min(self.medkit_heal, p1.max_hp - p1.hp)
            p1.hp = min(p1.hp + self.medkit_heal, p1.max_hp)
            self.spawn_timer = 10
        
        self.x, self.y = 0,0

    def spawn(self, grid):
        found = False
        while found == False:
            coordinate_y = random.randint(1,len(grid)-1)
            coordinate_x = random.randint(0, len(grid[coordinate_y])-1)
            if grid[coordinate_y][coordinate_x] == 0 and grid[coordinate_y+1][coordinate_x] != 0:
                found = True
        self.x = coordinate_x*TILE + 5
        self.y = coordinate_y*TILE

    def draw(self, surface, camera):
        img = medkit_frames[self.frame%MEDKIT_FRAMES - 1]
        surface.blit(img, (self.x - camera.x, self.y - camera.y))

class Camera:
    def  __init__(self, margin_x, x, y):
        self.margin_x = margin_x
        self.x = x
        self.y = y

        self.shake_time = 0

        self.shake_direction_x = 'right'
        self.shake_direction_y = 'up'

        self.max_shake_x = 20
        self.max_shake_y = 20
        self.shake_dist_x = 0
        self.shake_dist_y = 0
    def update(self, dt):
        if p1.x - self.x < self.margin_x:
            self.x = p1.x - self.margin_x
        elif p1.x - self.x > WIDTH - self.margin_x:
            self.x = p1.x - (WIDTH - self.margin_x)
        self.y = p1.y - HEIGHT // 2

        # --- NEW: Clamp Camera to Map Edges ---
        # Keep X between 0 and (Map Width - Screen Width)
        self.x = max(0, min(self.x, map_width - WIDTH))

        if self.shake_time > 0:
            self.shake_dist_x = random.randint(-self.intensity_x, self.intensity_x)
            self.shake_dist_y = random.randint(-self.intensity_y, self.intensity_y)
            self.shake_time = max(self.shake_time - dt, 0)
        else:
            self.shake_dist_x, self.shake_direction_y = 0,0
        
        self.x += self.shake_dist_x
        self.y += self.shake_dist_y

    def shake (self, length, intensity_x, intensity_y): self.shake_time, self.intensity_x, self.intensity_y = length, intensity_x, intensity_y

    def get_rect(self):
        global WIDTH, HEIGHT
        return pygame.Rect(self.x, self.y, (WIDTH), (HEIGHT))
    

# --- Setup ---
p1 = Player()

# Global list of active laser beams (populated by the boss in phase 2)
lasers = []

hitboxes = False

#get grid, tilerecrs, height, width
grid, tile_rects, map_height, map_width = get_grid("map.tile")

#this was actually written by me!!
enemies = spawn_wave([],wave_num)
camera = Camera(300, 0, 0)
upgrades = [Upgrade("medkit", 5)]

# --- Game loop ---
running = True
in_Game = False
start_Screen = True
just_Started = False
menu_state = 'main'
win = False
dead = False
paused = False
time = 0
start_screen_frame = 1
picture_frame_time = 0

menu_buttons = {
    'main': [
        {"Rect": pygame.Rect(500,225,250,100), "Name": "Play"}, 
        {"Rect": pygame.Rect(500,350,250,100), "Name": "Ctrls"}, 
        {"Rect": pygame.Rect(500,475,250,100), "Name": "Quit"}
    ],
    'controls': [
        {"Rect": pygame.Rect(500,475,250,100), "Name": "Back"}
    ]
}

button_text_offset_x = 20
button_text_offset_y = 15

pygame.mixer.music.load('menu music.mp3')
pygame.mixer.music.play(loops=-1)

while running:
    dt = clock.tick(60) / 1000
    if just_Started: 
        just_Started = not just_Started
        pygame.mixer.music.stop()
        pygame.mixer.music.load('bg music.mp3')
        pygame.mixer.music.play(loops=-1)
    
    if start_Screen:
        TITLE = pygame.Rect(50,50,700,150)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():      
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        screen.blit(pygame.transform.scale(BG, (800, 600)), (0,0))
        if menu_state == 'main':
            for button in menu_buttons[menu_state]:
                if button["Rect"].collidepoint(mouse_x, mouse_y) and click:
                    if button["Name"] == "Play":
                        start_Screen = False
                        in_Game = True
                        just_Started = True
                    
                    elif button["Name"] == "Ctrls":
                        menu_state = 'controls'

                    elif button["Name"] == "Quit":
                        running = False

            screen.blit(pygame.transform.scale(boss_frames[start_screen_frame % BOSS_FRAMES - 1],(BOSSW*4.3,BOSSH*4.3)), 
                        (90, 160))

            picture_frame_time +=1
            if picture_frame_time % 20 == 0:
                start_screen_frame +=1

        elif menu_state == 'controls':

            text_to_screen('Left: E', spawn_font, BLACK, 60, 240)
            text_to_screen('Right: D', spawn_font, BLACK, 60, 290)
            text_to_screen('Jump: W', spawn_font, BLACK, 60, 340)
            text_to_screen('Pause: ESC', spawn_font, BLACK, 60, 390)
            text_to_screen('Toggle Hitboxes: H', spawn_font, BLACK, 60, 440)

            text_to_screen('Slash: SPACE', spawn_font, BLACK, 250, 240)
            text_to_screen('Lunge: LSHIFT', spawn_font, BLACK, 250, 290)

            for button in menu_buttons[menu_state]:
                if button["Rect"].collidepoint(mouse_x, mouse_y) and click:
                    if button["Name"] == "Back":
                        menu_state = 'main'

        for button in menu_buttons[menu_state]:
            if button["Rect"].collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, RED, button["Rect"])
                text_to_screen(button["Name"], button_hover_font, BLACK, button["Rect"].x+button_text_offset_x, button["Rect"].y+button_text_offset_y)
                pygame.draw.rect(screen, BLACK, button["Rect"], 7)
            else:
                pygame.draw.rect(screen, GRAY, button["Rect"]) 
                text_to_screen(button["Name"], button_font, BLACK, button["Rect"].x+button_text_offset_x, button["Rect"].y+button_text_offset_y)
            pygame.draw.rect(screen, BLACK, button["Rect"], 5)
        
        pygame.draw.rect(screen, GRAY, TITLE)
        text_to_screen("EYE SEE YOU", title_font, BLACK, TITLE.x+20, TITLE.y+30)

        pygame.draw.ellipse(screen,BLACK, (610,92,20,60))

    elif in_Game:
        past_x = p1.x
        past_y = p1.y
        
        #delta time (converts frames to seconds by showing seconds per frame)
        time += dt
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            p1.handle_event(event)

        p1.update(dt, keys, tile_rects)

        for u in upgrades:
            u.update(dt, grid)
        
        camera.update(dt)

        for e in enemies:
            e.update(dt)

        # Update every active laser beam; each Laser handles its own
        # warning → active → done state transitions and player collision.
        for l in lasers:
            l.update(dt)

        screen.fill(SKY)

        screen.blit(BG, (0-camera.x*.5,-250-camera.y*.5))

        draw_tiles(grid, camera)

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
                        p1.hp-=e.dam
                        if p1.hp > 0:
                            play_sound("player hit")
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
                if e.hp > 0 and id(e) not in p1.hit_enemies and not (e.laser_round_state in ("warning", "active", "cooldown")):
                    if attack_rect.colliderect(e.get_rect()):
                        p1.hit_enemies.add(id(e))
                        #does more damage if lunging vs slashing
                        if p1.attack_state == 3:
                            e.take_hit(20)
                        else:
                            e.take_hit(10)

        for u in upgrades:
            if p1.get_rect().colliderect(u.get_rect()):
                u.touch()

        if len(enemies) == p1.score and wave_timer == -1:
            wave_timer = 5
        elif len(enemies) == p1.score and wave_timer > 0:
            wave_timer -=dt
        if wave_timer <=0 and len(enemies) == p1.score:
            wave_num+=1
            if wave_num > 5:
                in_Game = False
                win = True
            else:
                enemies = spawn_wave(enemies, wave_num)

            wave_timer = -1
            
                
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

    #drawing ___
    if ((in_Game) or (not in_Game and paused)) and not just_Started:
        # draws player and enemies
        for e in enemies:
            if e.hp > 0:
                e.draw(screen, camera)
                if hitboxes:
                    pygame.draw.rect(screen, RED, e.get_rect().move(-camera.x, -camera.y), 2)
        
        for u in upgrades:
            if u.x != 0 or u.y != 0:
                u.draw(screen, camera)
                if hitboxes:
                    pygame.draw.rect(screen, GREEN, u.get_rect().move(-camera.x, -camera.y), 2)
        p1.draw(screen, camera)

        if hitboxes:
            pygame.draw.rect(screen, RED, p1.get_rect().move(-camera.x, -camera.y), 2)

        if attack_rect and hitboxes:
            pygame.draw.rect(screen, CYAN, attack_rect.move(-camera.x, -camera.y), 2) if p1.attack_state != 3 else pygame.draw.rect(screen, GREEN, attack_rect.move(-camera.x, -camera.y), 2)

        # ── Draw laser beams ─────────────────────────────────────────────────
        # Drawn AFTER all world objects (tiles, enemies, player, upgrades) so
        # they always appear on top, but BEFORE the UI overlay so the HUD stays
        # readable over the beams.
        for l in lasers:
            l.draw(screen, camera)

        #prints text
        text_to_screen(f'Lunge Cooldown: {p1.stab_cooldown:.1f}', my_font, BLACK, 30, 80)

        #healthbar (all me)
        pygame.draw.rect(screen, GRAY, pygame.Rect(30,30,5*p1.max_hp,50))
        pygame.draw.rect(screen, GREEN if p1.hp > 60  else ORANGE if p1.hp > 30 else RED, pygame.Rect(30,30,5*p1.hp,50))
        pygame.draw.rect(screen, BLACK, pygame.Rect(30,30,5*p1.max_hp,50),5)
        text_to_screen(f'{int(p1.hp)}', my_font, BLACK, 40, 33)


        if wave_num == 5:
            pixelsperhp = 700/enemies[-1].max_hp
            #boss healthbar (all me)
            pygame.draw.rect(screen, GRAY, pygame.Rect(50,470,700,80))
            pygame.draw.rect(screen, RED, pygame.Rect(50,470,int(pixelsperhp*enemies[-1].hp),80))
            pygame.draw.rect(screen, BLACK, pygame.Rect(50,470,int(700),80),5)
            text_to_screen(f'{int(enemies[-1].hp)}/{enemies[-1].max_hp}', spawn_font, BLACK, 60, 480)


        if wave_timer != -1:
            if wave_num not in (4,5):
                text_to_screen(f'Time until Wave {wave_num+1}: {int(wave_timer)}', wave_timer_font, BLACK, 100, 200)
            elif wave_num == 5:
                text_to_screen(f'YOU WON!', wave_timer_font, BLACK, 250, 200)
            else:
                text_to_screen(f'BOSS INCOMING: {int(wave_timer)}', wave_timer_font, BLACK, 100, 200)

        text_to_screen(f'Wave: {wave_num}', my_font, BLACK, 30, 115)
        text_to_screen(f'Score: {p1.score}', my_font, BLACK, 30, 150)


        if len(Spawn_text) >= 1 and spawn_text_timer > 0:
            screen.blit(Spawn_text[0], (200,500))
            spawn_text_timer -= dt
        elif len(Spawn_text) != 0 and spawn_text_timer <=0:
            del Spawn_text[0]
            spawn_text_timer = 1.5

        text_to_screen(f'{1/dt:.2f} {camera.shake_time}', my_font, BLACK, 700, 30)

        if not in_Game and paused:
            text_to_screen(f"PAUSED", pause_font, BLACK, 250, 150)
    
    elif dead or win:
        screen.fill(GRAY)
        if dead:
            text_to_screen(f'GAME OVER', pause_font, BLACK, 170, 100)
        elif win:
            text_to_screen(f'YOU WIN!', pause_font, BLACK, 180, 100)
        stats_text = [
                      #line 1
                      my_font.render(f'{f'    You lasted for {time:.1f} seconds':^40}', True, BLACK) if dead else 
                      my_font.render(f'{f'    It took you {time:.1f} seconds to win':^40}', True, BLACK) , 
                      #line 2
                      my_font.render(f'{f'HP Left: {max(p1.hp,0)}':<25}{f'Amount Healed: {p1.healed}':>20}', True, BLACK) if win else 
                      my_font.render(f'{f'Wave: {wave_num}':<27}{f'Amount Healed: {p1.healed}':>20}', True, BLACK),
                      #line 3
                      my_font.render(f'{f'Damage Dealt: {p1.damage_dealt}':<20}{f'Enemies Killed: {p1.score}':>24}', True, BLACK),  
                      #line 4
                      my_font.render(f'{f'Slashes: {p1.slashes}':<20}{f'Lunges: {p1.stabs}':>31}', True, BLACK),
                      ]
        for index, stat in enumerate(stats_text):
            screen.blit(stat, (120, 220 + (40 * (index+1))))

    pygame.display.flip()
    
    if p1.hp <=0 and not dead:
        play_sound('player die')
        in_Game = False
        dead = True