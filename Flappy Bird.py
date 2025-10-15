import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 400
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐥 Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
BROWN = (160, 82, 45)

# Game variables
gravity = 0.5
bird_movement = 0
game_active = True
score = 0
high_score = 0
pipe_speed = 4

# Load bird
bird_surface = pygame.Surface((34, 24))
bird_surface.fill((255, 255, 0))  # Yellow bird
bird_rect = bird_surface.get_rect(center=(100, HEIGHT // 2))

# Create pipes
pipe_surface = pygame.Surface((70, 400))
pipe_surface.fill(GREEN)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# Fonts
font = pygame.font.Font(None, 50)

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            SCREEN.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            SCREEN.blit(flip_pipe, pipe)

def create_pipe():
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > -50]

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= HEIGHT - 50:
        return False
    return True

def display_score():
    score_surface = font.render(f'Score: {int(score)}', True, (255, 255, 255))
    SCREEN.blit(score_surface, (10, 10))

def floor():
    pygame.draw.rect(SCREEN, BROWN, pygame.Rect(0, HEIGHT - 50, WIDTH, 50))

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, HEIGHT // 2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    SCREEN.fill(BLUE)

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        SCREEN.blit(bird_surface, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)

        # Score
        score += 0.01
        display_score()

    else:
        game_over_surface = font.render("Game Over!", True, WHITE)
        SCREEN.blit(game_over_surface, (100, HEIGHT // 2 - 50))
        restart_surface = font.render("Press SPACE to restart", True, WHITE)
        SCREEN.blit(restart_surface, (20, HEIGHT // 2))

    # Floor
    floor()

    pygame.display.update()
    clock.tick(60)
