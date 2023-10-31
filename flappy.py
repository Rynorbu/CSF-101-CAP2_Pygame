import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def create_pipe():
	random_pipe_position = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_position))
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_position-300))
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
	new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rectangle = new_bird.get_rect(center = (100, bird_rectangle.centery))
	return new_bird, new_bird_rectangle

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255,255,255))
		score_rectangle = score_surface.get_rect(center = (288, 100))
		screen.blit(score_surface, score_rectangle)

	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
		score_rectangle = score_surface.get_rect(center = (288, 100))
		screen.blit(score_surface, score_rectangle)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
		high_score_rectangle = high_score_surface.get_rect(center = (288, 185))
		screen.blit(high_score_surface, high_score_rectangle)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score


#function to initialize (init()) pygame
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Images/04B_19.TTF',40)

# variables for the game
gravity = 0.17
bird_movement = 0
game_active = True
score = 0
high_score = 0


background_surface = pygame.image.load('Images/background-day.png').convert()
background_surface = pygame.transform.scale2x(background_surface)

bird_downflap = pygame.transform.scale2x(pygame.image.load('Images/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('Images/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('Images/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


pipe_surface = pygame.image.load('Images/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200) # event triggered every 1.2 seconds
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('Images/gameover.png').convert_alpha())
game_over_rectangle = game_over_surface.get_rect(center = (288,512))


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 6     # changed from 12 to 8 to reduce jumping speed....
 
			if event.key == pygame.K_SPACE and game_active == False:
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

	screen.blit(background_surface,(0,0))

	if game_active:
		# bird movement
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rectangle.centery += bird_movement
		screen.blit(rotated_bird, bird_rectangle)
		game_active = check_collision(pipe_list)


		# pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)


	else:
		screen.blit(game_over_surface, game_over_rectangle)
		high_score = update_score(score, high_score)
		score_display('game_over')

	pygame.display.update()
	clock.tick(120)