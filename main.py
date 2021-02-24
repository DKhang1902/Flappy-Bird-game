import pygame, random

screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
run = True
floor_movement = 0
gravity = 0.08
bird_movement = 0
clock = pygame.time.Clock()
FPS = 120
active = True
list_of_pipes = []

pygame.mixer.pre_init(44100, -16, 1, 256)
pygame.init()

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
FLAPPING = pygame.USEREVENT + 1
pygame.time.set_timer(FLAPPING, 200)

bird_surface = pygame.image.load('flappy-bird-assets-master/sprites/yellowbird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center=(50, 256))

icon = pygame.image.load("220px-Flappy_Bird_icon.png")
pygame.display.set_icon(icon)

bg_surface = pygame.image.load('flappy-bird-assets-master/sprites/background-day.png').convert()
base_surface = pygame.image.load('flappy-bird-assets-master/sprites/base.png').convert()

pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png').convert()

score_font = pygame.font.Font("04b_19/04B_19__.TTF", 25)

game_over_surface = pygame.image.load('flappy-bird-assets-master/sprites/message.png').convert_alpha()
gameover_rect = game_over_surface.get_rect(center=(144,256))

hit_sound = pygame.mixer.Sound("flappy-bird-assets-master/audio/hit.wav")
flap_sound = pygame.mixer.Sound("flappy-bird-assets-master/audio/wing.wav")
point_sound = pygame.mixer.Sound("flappy-bird-assets-master/audio/point.wav")
death_sound = pygame.mixer.Sound("flappy-bird-assets-master/audio/die.wav")

def dispaly_score(score):
    score_surface = score_font.render(f"Score: {str(score)}", True, (255,255,255))
    score_rect = score_surface.get_rect(center=(144,50))
    screen.blit(score_surface, score_rect)


def check_score(pipes, old_score):
    scores = 0
    for pipe in pipes:
        if pipe.centerx <= 50:
            scores += 0.5
    if scores > old_score:
        point_sound.play()
    return int(scores)


def display_base(x_base_position):
    screen.blit(base_surface, (x_base_position, 425))
    screen.blit(base_surface, (x_base_position + 336, 425))


def create_pipe(list_of_y):
    y_position = random.choice(list_of_y)
    bottom_pipe = pipe_surface.get_rect(midtop=(300, y_position))
    top_pipe = pipe_surface.get_rect(midbottom=(300, y_position-160))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.top <= 0:
            flipped_image = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_image, pipe)
        else:
            screen.blit(pipe_surface, pipe)

def rotate(bird):
    rotate_bird = pygame.transform.rotozoom(bird, -bird_movement*7, 1)
    return rotate_bird


def check_collision(pipes):
    global active
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            active = False
            hit_sound.play()
    if bird_rect.bottom < 0 or bird_rect.top > 512:
        active = False
        death_sound.play()
count = 0
score = 0
while run:
    clock.tick(FPS)
    pipe_random_heights = [200, 250, 300, 350, 400]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and active:
                bird_movement = 0
                bird_movement -= 3.5
                flap_sound.play()
            if event.key == pygame.K_SPACE and active == False:
                active = True
                list_of_pipes.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
        if event.type == SPAWNPIPE:
            list_of_pipes.extend(create_pipe(pipe_random_heights))
        if event.type == FLAPPING:
            if count % 3 == 0:
                 bird_surface = pygame.image.load('flappy-bird-assets-master/sprites/yellowbird-midflap.png').convert()
                 count += 1
            elif count % 3 == 1:
                bird_surface = pygame.image.load('flappy-bird-assets-master/sprites/yellowbird-upflap.png').convert()
                count += 1
            elif count % 3 == 2:
                bird_surface = pygame.image.load('flappy-bird-assets-master/sprites/yellowbird-downflap.png').convert()
                count += 1

    screen.blit(bg_surface, (0, 0))
    display_base(floor_movement)
    floor_movement -= 1
    if floor_movement < -336:
        floor_movement = 0

    score = check_score(list_of_pipes, score)
    dispaly_score(score)

    if active == True:
    # Bird
        rotated_bird = rotate(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        bird_movement += gravity
        bird_rect.centery += bird_movement
        check_collision(list_of_pipes)
    # Pipes
        list_of_pipes = move_pipes(list_of_pipes)
        draw_pipe(list_of_pipes)
    else:
        screen.blit(game_over_surface, gameover_rect)

    pygame.display.update()

pygame.quit()
