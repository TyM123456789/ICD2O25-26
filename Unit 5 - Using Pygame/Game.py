import pygame

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Character Demo")

# Load sprites
body_sheet = pygame.image.load("Walking.png").convert_alpha()
arms_sheet = pygame.image.load("arms.png").convert_alpha()
SCALE = 2  # try 2, 3, or 4

# Frame setup
BODY_FRAMES = 10
ARMS_FRAMES = 17
ENEMY_FRAMES = 6

BW = body_sheet.get_width() // BODY_FRAMES
BH = body_sheet.get_height()
AW = arms_sheet.get_width() // ARMS_FRAMES
AH = arms_sheet.get_height()

body_frames = [
    pygame.transform.scale(
        body_sheet.subsurface((i * BW, 0, BW, BH)),
        (BW * SCALE, BH * SCALE)
    )
    for i in range(BODY_FRAMES)
]
arms_frames = [
    pygame.transform.scale(
        arms_sheet.subsurface((i * AW, 0, AW, AH)),
        (AW * SCALE, AH * SCALE)
    )
    for i in range(ARMS_FRAMES)
]
enemy_frames = [
    pygame.transform.scale(
        arms_sheet.subsurface((i * AW, 0, AW, AH)),
        (AW * SCALE, AH * SCALE)
    )
    for i in range(ENEMY_FRAMES)
]

# Player
x, y = WIDTH // 2, HEIGHT - (BH * SCALE) - 20
speed = 2.5
facing_right = True

# Physics
y_vel = 0
gravity = 0.5
jump_strength = -10
on_ground = True

# Animation
frame = 0
anim_timer = 0
anim_speed = 0.1

# Attack system
attack_state = 0  # 0 = idle, 1 = slash1, 2 = slash2, 3 = stab
attack_frame = 0
attack_timer = 0

attack_speed = 0.1
attack_reset_timer = 0
attack_reset_time = 0.6  # time before combo resets
attacking = False

#___ARMS___
#jump + walk
jumparm = [16]
walkarm = [0,1,2,3,4,5,6,7]

# Attack order (indices in arms sheet)
slash1 = [11, 12, 13]
slash2 = [14, 15]
stab = [8, 9, 10]
attack_sequence = slash1 + slash2 + stab

running = True
while running:
    dt = clock.tick(60) / 1000
    attack_just_finished = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not attacking:
            if event.button == 1:

                attack_state += 1
                if attack_state > 3:
                    attack_state = 1

                attacking = True

                attack_frame = 0
                attack_timer = 0
                attack_reset_timer = 0
    keys = pygame.key.get_pressed()
    moving = False
    if attacking:
        attack_reset_timer += dt
        if attack_reset_timer > attack_reset_time:
            attack_state = 0
            attacking = False
            attack_frame = 0
    # Movement
    if keys[pygame.K_a] and not keys[pygame.K_d]:
        x -= speed
        facing_right = False
        moving = True
    if keys[pygame.K_d] and not keys[pygame.K_a]:
        x += speed
        facing_right = True
        moving = True

    # Jump
    if keys[pygame.K_SPACE] and on_ground:
        y_vel = jump_strength
        on_ground = False

    # Gravity
    y_vel += gravity
    y += y_vel

    ground = HEIGHT - (BH * SCALE) - 20
    if y >= ground:
        y = ground
        y_vel = 0
        on_ground = True

    # Body animation
    if not on_ground:
        frame = 9

    elif moving:
        # 🔥 FIX: instantly switch to walk instead of waiting for timer
        if frame == 9 or frame == 0:
            frame = 1  # first walking frame immediately

        anim_timer += anim_speed
        if anim_timer >= 1:
            anim_timer = 0
            frame += 1
            if frame > 8:
                frame = 1

    else:
        frame = 0

    body = body_frames[frame]

    # Arms animation
    if attacking:
        attack_timer += dt

        # pick animation first
        if attack_state == 1:
            anim = slash1
        elif attack_state == 2:
            anim = slash2
        elif attack_state == 3:
            anim = stab
        else:
            anim = []

        # advance animation timer
        if attack_timer >= attack_speed:
            attack_timer = 0
            attack_frame += 1

            if attack_frame >= len(anim):
                attack_just_finished = True
                attack_frame = 0
                attacking = False
                # finish current animation FIRST
                attack_frame = len(anim) - 1

                # force final frame render once
                arms = arms_frames[anim[attack_frame]]

                # THEN switch state safely next frame
                if attack_state == 3:
                    attack_state = 0
                    attacking = False
                else:
                    attacking = False

        # ALWAYS assign arms safely
        if len(anim) > 0:
            arms = arms_frames[anim[attack_frame]]
        else:
            arms = arms_frames[0]
    else:
        # normal arms
        if not on_ground:
            arms = arms_frames[16]
        elif moving:
            arms = arms_frames[frame % 8]
        else:
            arms = arms_frames[0]
    

    # Flip
    if not facing_right:
        body = pygame.transform.flip(body, True, False)
        arms = pygame.transform.flip(arms, True, False)

    # Draw
    screen.fill((0,200,255))

    # Draw body first
    screen.blit(body, (x, y))

    # Draw arms on top (aligned)
    ARM_OFFSET_X = 0
    ARM_OFFSET_Y = -10

    if not facing_right:
        ARM_OFFSET_X = -12

    screen.blit(arms, (x + ARM_OFFSET_X, y + ARM_OFFSET_Y))

    pygame.display.flip()

pygame.quit()