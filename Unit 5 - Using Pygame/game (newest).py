#fix end screen buttons and change start screen logo (make eye blink, flash different background, etc.)
#playtest boss and make better

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
# phase 3 boss sprite — single image, no frames
phase3_img_raw = pygame.image.load("phase3.png").convert_alpha()

#spear
boss_spear = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load("the actual spear of long sigma.png"), (280,280)),
    225)

rect = boss_spear.get_bounding_rect()
trimmed = pygame.Surface(rect.size, pygame.SRCALPHA)
trimmed.blit(boss_spear, (0, 0), rect)
boss_spear = trimmed
white_spear = boss_spear.copy()
white_spear.fill((255,255,255), special_flags=pygame.BLEND_RGB_MAX)



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
# scale phase3 sprite the same way as the boss (1.5x on top of SCALE), then doubled
phase3_img = pygame.transform.scale(phase3_img_raw,
    (int(phase3_img_raw.get_width() * SCALE*2),
     int(phase3_img_raw.get_height() * SCALE*2)))
phase3_img_flipped = pygame.transform.flip(phase3_img, True, False)
P3W = phase3_img.get_width()
P3H = phase3_img.get_height()

SPEARW = boss_spear.get_width()
SPEARH = boss_spear.get_height()

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
GROUND = (44 - 1) * TILE - (BH * SCALE) #sixteen is the place on the ground, -1 because index
normal_bg = pygame.transform.scale(pygame.image.load("backgroundv.2.png"), (800*4, 600*4))
phase_3_bg = pygame.transform.scale(pygame.image.load("background but seig.png"), (800*4, 600*4))

def start_game():
    global p1, lasers, eye_lasers, spears, grid, tile_rects, map_height, map_width, BG, tiles
    global wave_num, wave_timer, enemies, upgrades, camera, time, hitboxes
    global dead, win, paused, in_Game, start_Screen, menu_state, Spawn_text, spawn_text_timer
    global just_Started, start_screen_frame, picture_frame_time

    p1 = Player()
    lasers = []
    eye_lasers = []
    spears = []

    BG = normal_bg
    tiles = [
        "",
        pygame.transform.scale(pygame.image.load("blue dark tile.png"), (TILE, TILE)),
        pygame.transform.scale(pygame.image.load("blue light tile.png"), (TILE, TILE))
    ]

    grid, tile_rects, map_height, map_width = get_grid("map.tile")
    wave_num = 1
    wave_timer = -1
    enemies = spawn_wave([], wave_num)
    upgrades = [Upgrade("medkit", 5)]
    camera = Camera(300, 0, 0)
    Spawn_text = []
    time = 0
    dead = False
    win = False
    paused = False
    hitboxes = False
    menu_state = 'main'
    in_Game = False
    start_Screen = True
    just_Started = False
    spawn_text_timer = 1.5
    start_screen_frame = 1
    picture_frame_time = 0
    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu music.mp3')
    pygame.mixer.music.play(loops=-1)

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
    enemy_list.append(Enemy(True, 0, 0, 2, patrol_left=0, patrol_right=0))
    return enemy_list

def spawn_wave(enemy_list, wave):
    if wave != 5:
        enemy_list = add_enemies(enemy_list, .5 + (.5*wave))
    elif wave == 5:
        enemy_list = add_boss(enemy_list)
    return enemy_list

def text_to_screen(text, font, color, x, y):
    textt = font.render(text, False, color)
    screen.blit(textt, (x, y))

#creates text that shows when upgrades spawn
def spawn_text(type, font, color):
    Spawn_text.append(font.render(f'A {type} has spawned!', False, color))

# ─────────────────────────────────────────────────────────────────────────────
# LASER CLASS
# ─────────────────────────────────────────────────────────────────────────────
class Laser:
    def __init__(self, x, angle=90, warning=True, permanent=False, sound=False,
                 horizontal=False, world_y=None, active_duration = 0.8, warning_duration = 0.45):
        self.x         = x
        self.angle     = angle
        self.warning   = warning
        self.permanent = permanent
        self.sound     = sound
        self.timer     = 0.0
        self.state     = "warning" if warning else "active"

        self.horizontal = horizontal
        self.world_y    = world_y

        self.warning_duration = warning_duration
        self.active_duration    = active_duration

        self.width         = 40
        self.dam             = 2/3

    def update(self, dt):
        self.timer += dt

        warn_dur   = self.warning_duration
        active_dur = self.active_duration

        if self.state == "warning":
            if self.sound:
                laser_charge_s.play()
            if self.timer >= warn_dur:
                if self.sound:
                    laser_charge_s.stop()
                self.state = "active"
                self.timer = 0.0

        elif self.state == "active":
            if self.sound:
                laser_sound.play()

            beam_rect = self._get_beam_rect()
            if beam_rect.colliderect(p1.get_rect()):
                p1.hp -= self.dam
                if p1.hp > 0:
                    play_sound("player hit")

            if not self.permanent and self.timer >= active_dur:
                if self.sound:
                    laser_sound.stop()
                self.state = "done"

    def _get_beam_rect(self):
        if self.horizontal:
            return pygame.Rect(0, self.world_y - self.width // 2,
                               map_width, self.width)

        if self.angle == 90:
            return pygame.Rect(self.x - self.width // 2, 0, self.width, map_height)

        rad = math.radians(self.angle)
        x_span = map_height / math.tan(rad) if math.tan(rad) != 0 else 0
        x_min = min(self.x, self.x + x_span)
        x_max = max(self.x, self.x + x_span)
        return pygame.Rect(x_min - self.BEAM_WIDTH // 2, 0,
                           (x_max - x_min) + self.BEAM_WIDTH, map_height)

    def _get_screen_endpoints(self, camera):
        if self.angle == 90:
            sx = int(self.x - camera.x)
            return (sx, 0), (sx, HEIGHT)

        rad = math.radians(self.angle)
        tan_a = math.tan(rad) if math.tan(rad) != 0 else 1e-9

        world_y_top    = camera.y
        world_y_bottom = camera.y + HEIGHT

        world_x_top    = self.x + world_y_top    / tan_a
        world_x_bottom = self.x + world_y_bottom / tan_a

        sx_top    = int(world_x_top    - camera.x)
        sx_bottom = int(world_x_bottom - camera.x)
        return (sx_top, 0), (sx_bottom, HEIGHT)

    def draw(self, surface, camera):
        if self.horizontal:
            screen_y = int(self.world_y - camera.y)
            if self.state == "warning":
                pulse = 0.5 + 0.5 * math.sin(self.timer * 10)
                color = (255, int(80 + 120 * pulse), 0)
                pygame.draw.line(surface, color,
                                 (0, screen_y), (WIDTH, screen_y),
                                 int(self.width / 2))
            elif self.state == "active":
                pygame.draw.line(surface, (255, 200, 200),
                                 (0, screen_y), (WIDTH, screen_y),
                                 self.width + 8)
                pygame.draw.line(surface, (255, 50, 50),
                                 (0, screen_y), (WIDTH, screen_y),
                                 self.width)
            return

        top_pt, bot_pt = self._get_screen_endpoints(camera)

        if self.state == "warning":
            pulse = 0.5 + 0.5 * math.sin(self.timer * 10)
            color = (255, int(80 + 120 * pulse), 0)
            pygame.draw.line(surface, color, top_pt, bot_pt, int(self.width / 2))
            pygame.draw.rect(surface, color,
                             pygame.Rect(bot_pt[0] - 6, HEIGHT - 16, 12, 16))

        elif self.state == "active":
            pygame.draw.line(surface, (255, 200, 200), top_pt, bot_pt, self.width + 8)
            pygame.draw.line(surface, (255, 50, 50),   top_pt, bot_pt, self.width)

# ─────────────────────────────────────────────────────────────────────────────
# EYE LASER CLASS
# ─────────────────────────────────────────────────────────────────────────────
class EyeLaser:
    def __init__(self, origin_x, origin_y, sound=True, warning_duration = 1, active_duration = 1):
        self.ox    = origin_x
        self.oy    = origin_y

        self.sound = sound
        self.timer = 0.0
        self.state = "warning"

        self.warning_duration = warning_duration
        self.active_duration = active_duration
        self.damage = 1
        self.width = 20

        self.target = p1.get_rect()

        self.target_x, self.target_y = self.target.centerx, self.target.centery



    def _get_beam_rect(self):
        x_min = min(self.ox, self.target_x)
        y_min = min(self.oy, self.target_y)
        x_max = max(self.ox, self.target_x)
        y_max = max(self.oy, self.target_y)
        return pygame.Rect(x_min - self.width, y_min - self.width,
                           (x_max - x_min) + self.width * 2,
                           (y_max - y_min) + self.width * 2)

    def update(self, dt):
        self.timer += dt
        if self.state == "warning":
            if self.sound:
                laser_charge_s.play()
            if self.timer >= self.warning_duration:
                laser_charge_s.stop()
                self.state = "active"
                self.timer = 0.0
        elif self.state == "active":
            if self.sound:
                laser_sound.play()
            if p1.get_rect().clipline((self.ox, self.oy), (self.target_x, self.target_y)):
                p1.hp -= self.damage
                if p1.hp > 0:
                    play_sound("player hit")
            if self.timer >= self.active_duration:
                if self.sound:
                    laser_sound.stop()
                self.state = "done"

    def draw(self, surface, camera):
        sx  = int(self.ox - camera.x)
        sy  = int(self.oy - camera.y)
        ex2 = int(self.target_x - camera.x)
        ey2 = int(self.target_y - camera.y)

        # Extend the visual line past the target so it looks like it pierces through
        dx = ex2 - sx
        dy = ey2 - sy
        dist = math.sqrt(dx**2 + dy**2) or 1
        ex2 = int(sx + (dx / dist) * 2000)
        ey2 = int(sy + (dy / dist) * 2000)

        if self.state == "warning":
            pulse = 0.5 + 0.5 * math.sin(self.timer * 12)
            color = (255, int(50 + 150 * pulse), int(200 * pulse))
            pygame.draw.line(surface, color, (sx, sy), (ex2, ey2), max(2, self.width // 3))
        elif self.state == "active":
            pygame.draw.line(surface, (255, 200, 200), (sx, sy), (ex2, ey2), self.width + 6)
            pygame.draw.line(surface, (255, 50, 200),  (sx, sy), (ex2, ey2), self.width)

class Spear:
    def __init__(self, x, count=1):
        # Spawns at the top of the screen in world coords
        self.x = x
        self.world_y = camera.y  # top of current view
        self.vy = -200           # launch upward first
        self.phase = "up"        # "up" → "down"
        self.up_timer = .5      # how long it travels upward before falling
        self.timer = 0.0
        self.width = 10
        self.height = 370
        self.done = False
        self.damage = 20
        self.hit = False
        self.speed_down = 500    # pixels per second falling

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2+2,
            int(self.world_y) - self.height // 2 - 200,
            self.width,
            self.height
        )

    def update(self, dt):
        if win:
            global spears
            spears = []
        self.timer += dt

        if self.phase == "up":
            self.world_y += self.vy * dt
            if self.timer >= self.up_timer:
                self.phase = "down"
                self.vy = self.speed_down
                self.timer = 0.0

        elif self.phase == "down":
            self.world_y += self.vy * dt

            # Damage player — only if they have no knockback active
            if abs(p1.kb_x) <= 0 and abs(p1.kb_y) <= 0 and not self.hit:
                if self.get_rect().colliderect(p1.get_rect()):
                    p1.hp -= self.damage
                    if p1.hp > 0:
                        play_sound("player hit")
                    # Apply knockback
                    p1.kb_x = p1.knockback_x if p1.x < self.x else -p1.knockback_x
                    p1.kb_y = -p1.knockback_y
                    self.hit = True
                    p1.hit = True
                    p1.last_hit = 0



            # Disappear when off screen (below camera view)
            if self.world_y > camera.y + HEIGHT + 100:
                self.done = True

    def draw(self, surface, camera):
        img = white_spear if self.phase == "up" else boss_spear
        draw_x = self.x - SPEARW // 2 - camera.x
        draw_y = int(self.world_y) - SPEARW // 2 - camera.y-200
        surface.blit(img, (draw_x, draw_y))

class Player:
    def __init__(self):
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.attacking:
            play_sound("slash")
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
            play_sound("pause_s")
            paused = not paused
            if paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            in_Game = not in_Game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.on_ground:
                play_sound("jump")
                self.y_vel = p1.jump
                self.on_ground = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                if self.y_vel < -3:
                    self.y_vel = -3

    def update(self, dt, keys, tile_rects):
        p1.stab_cooldown -=dt
        if p1.stab_cooldown <= 0:
            p1.stab_cooldown = 0
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

        self.x += dx + self.kb_x
            
        player_rect = self.get_rect()
        for tile_rect in tile_rects:
            if player_rect.colliderect(tile_rect):
                if (dx + self.kb_x) > 0:
                    self.x = tile_rect.left - (BW - 40) * SCALE - 40
                elif (dx + self.kb_x) < 0:
                    self.x = tile_rect.right - 40
                self.kb_x = 0

        if not self.on_ground:
            self.y_vel += self.gravity
        self.y += self.y_vel + self.kb_y
            
        self.on_ground = False 

        player_rect = self.get_rect() 

        for tile_rect in tile_rects:
            if player_rect.colliderect(tile_rect):
                if (self.y_vel + self.kb_y) > 0:
                    self.y = tile_rect.top - (BH * SCALE)
                    self.y_vel = 0
                    self.kb_y = 0
                    self.on_ground = True
                elif (self.y_vel + self.kb_y) < 0:
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

        self.kb_x *= 0.8
        self.kb_y *= 0.9
        if self.kb_x < .1 and self.kb_x > 0 or self.kb_x > -.1 and self.kb_x < 0:
            self.kb_x = 0
        if self.kb_y < .1 and self.kb_y > 0 or self.kb_y > -.1 and self.kb_y < 0:
            self.kb_y = 0
            
        if not self.on_ground:
            self.frame = 9
        elif self.moving:
            self.anim_timer += dt
            if self.anim_timer >= .13:
                self.anim_timer = 0
                self.frame = (self.frame % 8) + 1
        else:
            self.frame = 0

        if self.attacking:
            anim = [slash1, slash2, stab][self.attack_state - 1] 
            self.attack_timer += dt
            if self.attack_timer >= self.attack_speed:
                self.attack_timer = 0
                self.attack_frame += 1
                if self.attack_state == 3:
                    self.kb_x = p1.lunge_power if self.facing_right else -p1.lunge_power
                    self.kb_y = 1 if not self.on_ground else 0
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
            ax = self.x + body_width*1.5
        else:
            ax = self.x if self.attack_state != 3 else self.x - 10*SCALE
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
            self.y = 1667
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
            self.decel_frames = [1, 0]

            self.state = "accel"

            self.laser_round_state = "noo"
            self.phase = None
            self.p3_state = "none"
            self.phase3_entered = False

        else:
            self.phase = 1
            #enemy max hp
            self.max_hp = 400
            self.hp = self.max_hp
            self.dam = 20
            frames = [range(BOSS_FRAMES)]

            self.vx               = 0.0
            self.vy               = 0.0
            self.push_timer       = 0.0
            self.base_speed       = 200.0
            self.phase2_entered   = False
            self.retreating       = False
            self.start_x          = self.x
            self.start_y          = self.y
            self.laser_round      = 0
            self.max_laser_rounds = 5
            self.laser_round_state    = "idle"
            self.laser_cooldown_timer = 0.0
            self.speed_boosted        = False

            # ── Phase 3 state ────────────────────────────────────────────────
            self.phase3_entered        = False
            self.p3_state              = "none"
            self.p3_rain_timer         = 0.0
            self.p3_rain_interval      = 1.2
            # Boss hovers here while retreating, during rain, and during walls.
            # World y = TILE = 64px (map row 1 — one tile from the very top of map2)
            self.p3_wall_rows          = []
            self.p3_wall_timer         = 0.0
            self.p3_wall_interval      = 0.1
            self.p3_combat_timer       = 0.0
            self.p3_combat_interval    = .75
            self.p3_eye_laser          = None
            self.p3_target_laser       = None
            self.p3_teleport_timer     = 0.0
            self.p3_teleport_interval  = 1.5

    def take_hit(self, damage):
        if self.p3_state != "p3_retreat":
            self.hp -= damage
            p1.damage_dealt += damage

            if self.hp <= 0 and self.is_Boss and not self.phase3_entered:
                self.hp = self.max_hp
                self.phase = 3
                self.phase3_entered = True
                self.p3_state = "p3_retreat"
                lasers.clear()

            elif self.hp > 0:
                play_sound("enemy hit")
            elif not self.is_Boss or self.p3_state != "p3_retreat":
                p1.score += 1
                play_sound("die")
                if self.is_Boss:
                    lasers.clear()
                    eye_lasers.clear()
            elif  self.is_Boss and not self.phase3_entered:
                play_sound("die")
            self.hit = True
            self.last_hit = 0
    
    def get_rect(self):
        if not self.is_Boss:
            return pygame.Rect(self.x + 40, self.y + 3, (EW * SCALE) - 75, (EH * SCALE) + 5)
        else:
            if self.phase3_entered and self.p3_state != 'p3_retreat':
                return pygame.Rect(self.x + int(338*SCALE), self.y + int(330*SCALE), (EW+30) * SCALE, (EH+23) * SCALE)
            return pygame.Rect((self.x+70), self.y+70, BOSSW * SCALE-50, BOSSH * SCALE-50)

    def _spawn_lasers(self):
        global lasers
        lasers.clear()
        num_lasers = 20
        offset = random.randint(0,100)
        for i in range(1, num_lasers + 1):
            world_x = int(map_width * i / (num_lasers + 1))
            lasers.append(Laser(world_x+offset, angle=90, warning=True, permanent=False, sound=True))

    def _spawn_spears(self, count=8):
        """Spawn `count` spears spread across the visible screen width."""
        global spears
        padding = 80  # keep spears away from screen edges
        for i in range(count):
            # Spread evenly with a little random jitter
            base_x = camera.x + padding + (WIDTH - padding * 2) * i / max(count - 1, 1)
            jitter = random.randint(-40, 40)
            wx = int(base_x + jitter)
            spears.append(Spear(wx))

    def _p3_spawn_rain_batch(self):
        global lasers
        lasers = [l for l in lasers if l.state != "done" or l.permanent]
        num = 12
        offset = random.randint(-80, 80)
        for i in range(1, num + 1):
            wx = int(map_width * i / (num + 1)) + offset
            lasers.append(Laser(wx, angle=90, warning=True, permanent=False, sound=True))

    def _p3_spawn_wall_laser(self, row):
        world_y = row * TILE + TILE // 2
        # permanent=True — these wall lasers stay active forever, blocking the player from leaving
        lasers.append(Laser(0, horizontal=True, world_y=world_y,
                            warning=True, permanent=True, sound=False))

    def _p3_fire_eye_laser(self):
        eye_x = self.x + P3W // 2
        eye_y = self.y + P3H // 2
        self.p3_eye_laser = EyeLaser(eye_x, eye_y)
        eye_lasers.append(self.p3_eye_laser)

    def _p3_fire_targeted_laser(self):
        global lasers
        if random.random() < 0.5:
            l = Laser(p1.x + (BW * SCALE) // 2, angle=90,
                      warning=True, permanent=False, sound=True)
        else:
            l = Laser(0, horizontal=True, world_y=p1.y + (BH * SCALE) // 2,
                      warning=True, permanent=False, sound=True)
        lasers.append(l)
        self.p3_target_laser = l

    def _p3_teleport_to_platform(self):
        found = False
        while not found:
            coordinate_y = random.randint(1, len(grid) - 2)
            coordinate_x = random.randint(1, len(grid[coordinate_y]) - 2)  # skip border 2s 
            if (grid[coordinate_y][coordinate_x] == 1 and coordinate_y * 64 < 800):
                found = True

        hitbox_half_w = ((EW + 30) * SCALE) // 2
        tile_centre_x = coordinate_x * TILE + TILE // 2
        tile_top_y    = coordinate_y * TILE

        self.x = tile_centre_x - int(325 * SCALE) - hitbox_half_w
        self.y = tile_top_y    - int(430 * SCALE)

    def update(self, dt):
        global grid, tile_rects, map_height, map_width, lasers
        self.new_facing_right = self.facing_right
        if self.hit:
            self.last_hit += dt 
            if self.last_hit >= 0.5:
                self.hit = False
                self.last_hit = 0
        if not self.is_Boss:
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

            self.x = self.x + self.speed if self.new_facing_right else self.x - self.speed

            self.anim_timer += dt
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
            self.facing_right = True if self.x < p1.x else False

            if self.phase3_entered:
                self.p3 = self.p3_state

                if self.p3 == "p3_retreat":
                    target_x = map_width / 2 - P3W / 2
                    target_y = 0
                    dx = target_x - self.x
                    dy = target_y - self.y
                    dist = math.sqrt(dx*dx + dy*dy) or 1
                    speed = 300.0
                    self.x += (dx / dist) * speed * dt
                    self.y += (dy / dist) * speed * dt

                    if dist < 25:
                        global BG, tiles
                        grid, tile_rects, map_height, map_width = get_grid("map2.tile")
                        camera.shake(1.5,15,15)
                        tiles = [
                                "",
                                pygame.transform.scale(pygame.image.load("blue dark tile.png"), (TILE, TILE)),
                                pygame.transform.scale(pygame.image.load("blue light tile.png"), (TILE, TILE))
                            ]
                        BG = phase_3_bg
                        self.p3_state = "p3_rain"
                        self.p3_rain_timer = 0.0
                        lasers.clear()
                        self._p3_teleport_to_platform()


                elif self.p3 == "p3_rain":

                    self.p3_rain_timer += dt
                    if self.p3_rain_timer >= self.p3_rain_interval:
                        self.p3_rain_timer = 0.0
                        self._p3_spawn_rain_batch()

                    player_row = int(p1.y / TILE)
                    if player_row <= 10:
                        
                        laser_charge_s.stop()
                        laser_sound.stop()
                        lasers.clear()
                        
                        self.p3_state       = "p3_walls"
                        # Wall lasers cover rows 14-20; permanent so they block escape forever
                        self.p3_wall_rows   = list(range(14, 29))
                        self.p3_wall_timer  = 0.0

                elif self.p3 == "p3_walls":

                    self.p3_wall_timer += dt
                    if self.p3_wall_timer >= self.p3_wall_interval and self.p3_wall_rows:
                        self.p3_wall_timer = 0.0
                        row = self.p3_wall_rows.pop(0)
                        self._p3_spawn_wall_laser(row)

                    if not self.p3_wall_rows:
                        self.p3_state          = "p3_combat"
                        self.p3_combat_timer   = self.p3_combat_interval
                        self.p3_teleport_timer = self.p3_teleport_interval

                elif self.p3 == "p3_combat":
                    self.p3_teleport_timer -= dt
                    if self.p3_teleport_timer <= 0:
                        self._p3_teleport_to_platform()
                        self.p3_teleport_timer = self.p3_teleport_interval

                    self.p3_combat_timer -= dt
                    if self.p3_combat_timer <= 0:
                        self.attack = random.randint(1,4)
                        if self.attack == 1:
                            self._p3_fire_eye_laser()
                            self.p3_state = "p3_eye_fire"
                        elif self.attack == 2 or self.attack == 3:
                            self._spawn_spears()
                            self.p3_state = "p3_spear_fire"
                        else:
                            self._p3_fire_targeted_laser()
                            self.p3_state = "p3_targeted"

                elif self.p3 == "p3_eye_fire":
                    if self.p3_eye_laser and self.p3_eye_laser.state == "done":
                        self.p3_eye_laser = None
                        self.p3_state        = "p3_combat"
                        self.p3_combat_timer = self.p3_combat_interval

                elif self.p3 == "p3_spear_fire":
                    global spears
                    spears_done = True
                    for s in spears:
                        if not s.done:
                            spears_done = False
                    if spears_done:
                        spears = []
                        self.p3_state        = "p3_combat"
                        self.p3_combat_timer = self.p3_combat_interval

                elif self.p3 == "p3_targeted":
                    if self.p3_target_laser and self.p3_target_laser.state == "done":
                        self.p3_target_laser = None
                        self.p3_state         = "p3_combat"
                        self.p3_combat_timer  = self.p3_combat_interval

                # Always bob
                self.push_timer += dt
                self.y += math.sin(self.push_timer * 3) * 0.5

                return

            if self.hp <= self.max_hp//2 and not self.phase2_entered:
                self.phase          = 2
                self.phase2_entered = True
                self.retreating     = True

            if self.retreating:
                dx   = self.start_x - self.x
                dy   = self.start_y - self.y
                dist = math.sqrt(dx*dx + dy*dy) or 1

                retreat_speed = 200.0
                self.x += (dx / dist) * retreat_speed * dt
                self.y += (dy / dist) * retreat_speed * dt

                if dist < 20:
                    self.x, self.y         = self.start_x, self.start_y
                    self.retreating        = False
                    self.laser_round       = 0
                    self.laser_round_state = "warning"
                    self._spawn_lasers()

                self.anim_timer += dt
                if self.anim_timer >= 1 / 8:
                    self.anim_timer = 0
                    self.frame += 1

            elif self.laser_round_state in ("warning", "active", "cooldown"):

                if self.laser_round_state == "warning":
                    if all(l.state in ("active", "done") for l in lasers):
                        self.laser_round_state = "active"

                elif self.laser_round_state == "active":
                    if all(l.state == "done" for l in lasers):
                        self.laser_round += 1

                        if self.laser_round >= self.max_laser_rounds:
                            lasers.clear()
                            self.laser_round_state = "done"
                            if not self.speed_boosted:
                                self.base_speed    *= 1.5
                                self.speed_boosted = True
                        else:
                            self.laser_round_state    = "cooldown"
                            self.laser_cooldown_timer = 1.5

                elif self.laser_round_state == "cooldown":
                    self.laser_cooldown_timer -= dt
                    if self.laser_cooldown_timer <= 0:
                        self._spawn_lasers()
                        self.laser_round_state = "warning"

                self.push_timer += dt
                self.y = self.start_y + math.sin(self.push_timer * 3) * 12

                self.anim_timer += dt
                if self.anim_timer >= 1 / 8:
                    self.anim_timer = 0
                    self.frame += 1

            else:
                self.push_timer += dt

                speed_mult = 0.15 + 0.85 * abs(math.sin(self.push_timer * 1.5))

                dx   = p1.x - self.x
                dy   = p1.y - self.y-100
                dist = math.sqrt(dx*dx + dy*dy) or 1

                target_vx = (dx / dist) * self.base_speed * speed_mult
                target_vy = (dy / dist) * self.base_speed * speed_mult

                lerp = 0.07
                self.vx += (target_vx - self.vx) * lerp
                self.vy += (target_vy - self.vy) * lerp

                self.x += self.vx * dt
                self.y += self.vy * dt

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
            if self.phase3_entered and self.p3_state != "p3_retreat":
                img = phase3_img if self.facing_right else phase3_img_flipped
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
        elif self.x == 0 and self.y == 0 and enemies[-1].p3_state != "p3_retreat":
            spawn_text("medkit", spawn_font, GREEN)
            self.spawn(grid)
        elif enemies[-1].phase == 3 and self.y > 800 and enemies[-1].p3_state != "p3_retreat":
            spawn_text("medkit", spawn_font, GREEN)
            self.spawn(grid)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, (MW * SCALE), (MH * SCALE))

    def touch(self):
        play_sound("upgrade")
        if self.type == "medkit":
            p1.healed += min(self.medkit_heal, p1.max_hp - p1.hp)
            p1.hp = min(p1.hp + self.medkit_heal, p1.max_hp)
            self.spawn_timer = 10 if enemies[-1].phase != 3 else 20
        
        self.x, self.y = 0,0

    def spawn(self, grid):
        found = False
        while found == False:
            coordinate_y = random.randint(1,len(grid)-1)
            coordinate_x = random.randint(0, len(grid[coordinate_y])-1)
            if grid[coordinate_y][coordinate_x] == 0 and grid[coordinate_y+1][coordinate_x] != 0:
                if enemies[-1].phase != 3 or (coordinate_y * 64 < 800): 
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

        self.x = max(0, min(self.x, map_width - WIDTH))

        if self.shake_time > 0:
            self.shake_dist_x = random.randint(-self.intensity_x, self.intensity_x)
            self.shake_dist_y = random.randint(-self.intensity_y, self.intensity_y)
            self.shake_time = max(self.shake_time - dt, 0)
        else:
            self.shake_dist_x, self.shake_direction_y = 0,0
        
        self.x += self.shake_dist_x
        self.y += self.shake_dist_y

    def shake (self, length, intensity_x, intensity_y): 
        self.shake_time, self.intensity_x, self.intensity_y = length, intensity_x, intensity_y
    
# --- Game loop ---
running = True
start_game()

menu_buttons = {
    'main': [
        {"Rect": pygame.Rect(500,225,250,100), "Name": "Play"}, 
        {"Rect": pygame.Rect(500,350,250,100), "Name": "Ctrls"}, 
        {"Rect": pygame.Rect(500,475,250,100), "Name": "Quit"}
    ],
    'controls': [
        {"Rect": pygame.Rect(500,475,250,100), "Name": "Back"}
    ],
    'end': [
        {"Rect": pygame.Rect(50,475,300,100), "Name": "Return"},
        {"Rect": pygame.Rect(500,475,250,100), "Name": "Quit"}
    ]
}

button_text_offset_x = 20
button_text_offset_y = 15

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

            text_to_screen('Left: A', spawn_font, BLACK, 60, 240)
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

        dist_from_mouse_x = mouse_x - 610
        dist_from_mouse_y = mouse_y - 92

        offset_x = dist_from_mouse_x//120
        offset_y = dist_from_mouse_y//100

        pygame.draw.ellipse(screen,BLACK, (610+offset_x,92+offset_y,20,60))

    elif in_Game:
        past_x = p1.x
        past_y = p1.y
        
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

        if enemies[-1].hp > 0:
            for l in lasers:
                l.update(dt)
            lasers[:] = [l for l in lasers if l.state != "done" or l.permanent]

            for el in eye_lasers:
                el.update(dt)
            eye_lasers[:] = [el for el in eye_lasers if el.state != "done"]

            for s in spears:
                s.update(dt)
            spears[:] = [s for s in spears if not s.done]

        if p1.last_hit >= .5:
            p1.hit = False
            p1.last_hit = 0
        if p1.hit:
            p1.last_hit += dt
        elif p1.kb_x == 0:
            for e in enemies:
                if e.hp > 0:
                    if p1.get_rect().colliderect(e.get_rect()) and not (e.phase3_entered and e.p3_state != 'p3_retreat'):
                        p1.hit = True
                        p1.last_hit = 0
                        p1.hp-=e.dam
                        if p1.hp > 0:
                            play_sound("player hit")
                        if p1.x > e.x:
                            p1.kb_x = p1.knockback_x
                        else:
                            p1.kb_x = -p1.knockback_x
                        if p1.on_ground:
                            p1.kb_y = -p1.knockback_y
        attack_rect = p1.get_attack_rect()
        if attack_rect:
            for e in enemies:
                if e.hp > 0 and id(e) not in p1.hit_enemies and not (e.laser_round_state in ("warning", "active", "cooldown")):
                    if attack_rect.colliderect(e.get_rect()):
                        p1.hit_enemies.add(id(e))
                        if p1.attack_state == 3:
                            e.take_hit(20)
                        else:
                            e.take_hit(10)

        for u in upgrades:
            if p1.get_rect().colliderect(u.get_rect()):
                u.touch()

        if len(enemies) == p1.score and wave_timer == -1:
            wave_timer = 5

            lasers.clear()
            eye_lasers.clear()
            spears.clear()
            laser_charge_s.stop()
            laser_sound.stop()
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
            
        p1.max_speed = 0 if p1.max_speed == 128 else p1.max_speed
        p1.speed_x = abs(p1.x - past_x)
        p1.speed_y = abs(p1.y - past_y)
        p1.tot_speed = math.sqrt(p1.speed_x**2 + p1.speed_y**2)
        p1.max_speed = max(p1.max_speed, p1.tot_speed)

    elif not dead and not win:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                p1.handle_event(event)        
            if event.type == pygame.QUIT:
                running = False

    if ((in_Game) or (not in_Game and paused)) and not just_Started:

        screen.fill(SKY)

        if BG != phase_3_bg:
            screen.blit(BG, (0-camera.x*.5,-250-camera.y*.5))
        else:
            screen.blit(BG, (0-camera.x*.5,-350-camera.y*.5))

        for e in enemies:
            if e.hp > 0 and e.phase == 3:
                e.draw(screen, camera)

                if hitboxes:
                    pygame.draw.rect(screen, RED, e.get_rect().move(-camera.x, -camera.y), 2)

        draw_tiles(grid, camera)

        for e in enemies:
            if e.hp > 0 and e.phase != 3:
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

        for l in lasers:
            l.draw(screen, camera)

        for s in spears:
            s.draw(screen, camera)
            if hitboxes:
                pygame.draw.rect(screen, RED, s.get_rect().move(-camera.x, -camera.y), 2)

        for el in eye_lasers:
            el.draw(screen, camera)

        boss_list = [e for e in enemies if e.is_Boss]
        if boss_list:
            boss = boss_list[0]
            if boss.phase3_entered and boss.p3_state == "p3_rain":
                text_to_screen("CLIMB! CLIMB! CLIMB!", wave_timer_font, RED, 130, 250)

        text_to_screen(f'Lunge Cooldown: {p1.stab_cooldown:.1f}', my_font, BLACK, 30, 80)

        pygame.draw.rect(screen, GRAY, pygame.Rect(30,30,5*p1.max_hp,50))
        pygame.draw.rect(screen, GREEN if p1.hp > 60  else ORANGE if p1.hp > 30 else RED, pygame.Rect(30,30,5*p1.hp,50))
        pygame.draw.rect(screen, BLACK, pygame.Rect(30,30,5*p1.max_hp,50),5)
        text_to_screen(f'{int(p1.hp)}', my_font, BLACK, 40, 33)

        if wave_num == 5:
            pixelsperhp = 700/enemies[-1].max_hp
            pygame.draw.rect(screen, GRAY, pygame.Rect(50,470,700,80))
            pygame.draw.rect(screen, RED, pygame.Rect(50,470,int(pixelsperhp*enemies[-1].hp),80))
            pygame.draw.rect(screen, BLACK, pygame.Rect(50,470,int(700),80),5)
            phase_label = f'{int(enemies[-1].hp)}/{enemies[-1].max_hp}'
            text_to_screen(phase_label, spawn_font, BLACK, 60, 480)

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

        text_to_screen(f'{1/dt:.2f}', my_font, BLACK, 700, 30)

        if not in_Game and paused:
            text_to_screen(f"PAUSED", pause_font, BLACK, 250, 150)
    
    elif dead or win:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        screen.fill(GRAY)
        if dead:
            text_to_screen(f'GAME OVER', pause_font, BLACK, 170, 100)
        elif win:
            text_to_screen(f'YOU WIN!', pause_font, BLACK, 180, 100)
        stats_text = [
                      my_font.render(f'{f"    You lasted for {time:.1f} seconds":^40}', True, BLACK) if dead else 
                      my_font.render(f'{f"    It took you {time:.1f} seconds to win":^40}', True, BLACK) , 
                      my_font.render(f'{f"HP Left: {max(round(p1.hp,0),0)}":<25}{f"Amount Healed: {round(p1.healed,0)}":>20}', True, BLACK) if win else 
                      my_font.render(f'{f"Wave: {wave_num}":<27}{f"Amount Healed: {round(p1.healed,0)}":>20}', True, BLACK),
                      my_font.render(f'{f"Damage Dealt: {p1.damage_dealt}":<20}{f"Enemies Killed: {p1.score}":>24}', True, BLACK),  
                      my_font.render(f'{f"Slashes: {p1.slashes}":<20}{f"Lunges: {p1.stabs}":>31}', True, BLACK),
                      ]
        for index, stat in enumerate(stats_text):
            screen.blit(stat, (120, 220 + (40 * (index+1))))

        for button in menu_buttons["end"]:
            if button["Rect"].collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, RED, button["Rect"])
                text_to_screen(button["Name"], button_hover_font, BLACK, button["Rect"].x + 10, button["Rect"].y + 10)
                if click:
                    if button["Name"] == "Quit":
                        running = False
                    elif button["Name"] == "Return":
                        start_game()
                        continue
            else:
                pygame.draw.rect(screen, GRAY, button["Rect"])
                text_to_screen(button["Name"], button_font, BLACK, button["Rect"].x + 10, button["Rect"].y + 10)
            pygame.draw.rect(screen, BLACK, button["Rect"], 5)

    pygame.display.flip()
    
    if p1.hp <=0 and not dead:
        play_sound('player die')
        laser_charge_s.stop()
        laser_sound.stop()
        in_Game = False
        dead = True

pygame.quit()