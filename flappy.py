import pygame, sys, random
import os

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Images/04B_19.TTF', 40)

def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_position - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rectangle.colliderect(pipe):
            return False
    if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 900:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rectangle = new_bird.get_rect(center=(100, bird_rectangle.centery))
    return new_bird, new_bird_rectangle

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rectangle = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rectangle)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rectangle = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rectangle)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rectangle = high_score_surface.get_rect(center=(288, 185))
        screen.blit(high_score_surface, high_score_rectangle)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def save_high_score(high_score):
    try:
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))
    except IOError as e:
        print(f"Error saving high score: {e}")


def load_high_score():
    if os.path.isfile("high_score.txt"):
        with open("high_score.txt", "r") as file:
            try:
                return round(float(file.read()))  # Convert to float, round, and then convert to int
            except ValueError:
                return 0
    return 0

# Initialize Pygame
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()

game_active = False
gravity = 0.17
bird_movement = 0
score = 0
high_score = load_high_score()

background_surface = pygame.image.load('Images/background-day.png').convert()
background_surface = pygame.transform.scale2x(background_surface)

bird_downflap = pygame.transform.scale2x(pygame.image.load('Images/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('Images/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('Images/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('Images/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# Define button positions and text
start_button_rect = pygame.Rect(200, 400, 180, 80)
quit_button_rect = pygame.Rect(200, 500, 180, 80)
start_button_text = game_font.render("Start", True, (0, 0, 0))
quit_button_text = game_font.render("Quit", True, (0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(high_score)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6

            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rectangle.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rectangle = bird_animation()

    screen.blit(background_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rectangle.centery += bird_movement
        screen.blit(rotated_bird, bird_rectangle)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01  # Increase the score over time
        score_display('main_game')
        high_score = update_score(score, high_score)

    else:
        # Draw buttons and their text on the home screen
        pygame.draw.rect(screen, (255, 255, 255), start_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), quit_button_rect)
        screen.blit(start_button_text, (225, 420))
        screen.blit(quit_button_text, (235, 520))

        # Display current and high scores
        current_score_text = game_font.render(f'Current Score: {int(score)}', True, (0, 0, 0))
        current_score_rect = current_score_text.get_rect(center=(288, 300))
        screen.blit(current_score_text, current_score_rect)

        high_score_text = game_font.render(f'High Score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect(center=(288, 350))
        screen.blit(high_score_text, high_score_rect)

        # Handle button clicks on the home screen
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        if start_button_rect.collidepoint(mouse_x, mouse_y):
            if mouse_clicked[0]:
                game_active = True
                pipe_list.clear()
                bird_rectangle.center = (100, 512)
                bird_movement = 0
                score = 0

        if quit_button_rect.collidepoint(mouse_x, mouse_y):
            if mouse_clicked[0]:
                save_high_score(high_score)
                pygame.quit()
                sys.exit()

    pygame.display.update()

    # Add error handling to catch any exceptions
    try:
        clock.tick(120)
    except Exception as e:
        print(f"An error occurred: {e}")

