import pygame
import sys



# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
PLAYER_SIZE = 50
GRAVITY = 0.3
PLAYER_JUMP_SPEED = -15

# Colors
BLACK = (0, 0, 0)
BLUE = (200, 0, 255)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Basic Platformer')

# Player properties
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_SIZE
player_speed = 5
player_y_speed = 1
on_ground = True

# Gravity
player_y_speed += GRAVITY
player_y += player_y_speed
if player_y >= SCREEN_HEIGHT - PLAYER_SIZE:
    player_y = SCREEN_HEIGHT - PLAYER_SIZE
    on_ground = True
    player_y_speed = 0

obstacles = [
    pygame.Rect(300, SCREEN_HEIGHT - 150, 50, 50),
    pygame.Rect(500, SCREEN_HEIGHT - 150, 50, 100),
    # Add more obstacles as needed
]

# Initialize Pygame
pygame.init()

# Game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
        # Drawing the obstacle
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    for obstacle in obstacles:
        pygame.draw.rect(screen, [255, 255, 0], obstacle)
        if player_rect.colliderect(obstacle):
            game_over = True
    else:
        screen.fill([0, 0, 0])
        font = pygame.font.SysFont(None, 55)
        text = font.render('Game Over', True, [255, 0, 0])
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))
    # Key Presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_SPACE] and on_ground:
            player_y_speed = PLAYER_JUMP_SPEED
            on_ground = False

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
