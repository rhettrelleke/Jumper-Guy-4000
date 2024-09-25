import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
PLAYER_SIZE = 40
GRAVITY = 0.9
PLAYER_JUMP_SPEED = -18

score = 0

# Colors
BLACK = (0, 0, 0)
BLUE = (200, 0, 255)
WHITE = (255, 255, 255)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption('Jumper Guy 4000')

#background image
background_image = pygame.image.load('background2.webp').convert()

#player image
player_image = pygame.image.load('character.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 100))
# Player properties
ground_height = 100
ground_level = SCREEN_HEIGHT - 20
player_x = SCREEN_WIDTH // 2 - player_image.get_width() // 2
player_y = ground_level - player_image.get_height()
player_speed = 7
player_y_speed = 1
on_ground = True

obstacle_speed = 6.5  # Speed at which obstacles move to the left
obstacle_timer = 0
obstacle_interval = 110

obstacles = [
        pygame.Rect(300, ground_level - 150, 50, 50),
        pygame.Rect(500, ground_level - 150, 50, 100),
        # Add more obstacles as needed
        ]

def draw_replay_button():
    button_color = [0, 0, 255]  # Green color
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50)
    pygame.draw.rect(screen, button_color, button_rect)
    font = pygame.font.SysFont(None, 36)
    text = font.render('Replay', True, [255, 255, 255])  # Black text
    screen.blit(text, (button_rect.x + 10, button_rect.y + 10))

    return button_rect

def draw_quit_button():
    button_color = [255, 0, 0]  # Red color
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 100, 50)
    pygame.draw.rect(screen, button_color, button_rect)
    font = pygame.font.SysFont(None, 36)
    text = font.render('Quit', True, [255, 255, 255])  # Black text
    screen.blit(text, (button_rect.x + 10, button_rect.y + 10))

    return button_rect

def is_mouse_click_on_button(mouse_pos, button_rect):
    if button_rect.collidepoint(mouse_pos):
        return True
    return False

def reset_game():
    global player_x, player_y, game_over, obstacles, obstacle_timer, score
    # Reset game variables
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - PLAYER_SIZE
    game_over = False
    obstacles.clear()
    obstacle_timer = 0
    score = 0
    # Add any other game state resets here

def quit_game():
    pygame.quit
    sys.exit()

def create_random_obstacle():
    width = random.randint(30, 100)  # Random width
    height = random.randint(30, 100)  # Random height
    x_position = SCREEN_WIDTH + width  # Start off-screen
    y_position = ground_level - height  # Adjust for height

    return pygame.Rect(x_position, y_position, width, height)

def save_high_score(high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0  # Return 0 if file doesn't exist or content is not a valid number

def display_score(score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {int(score)}', True, WHITE)
    screen.blit(score_text, (10, 10))  # Position the score at the top-left corner

def display_high_score(high_score):
    font = pygame.font.SysFont(None, 36)
    high_score_text = font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
    screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))  # Adjust the position as needed

high_score = load_high_score()
# Game loop
running = True
clock = pygame.time.Clock()
game_over = False
while running:
    clock.tick(60)
    screen.blit(background_image, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if is_mouse_click_on_button(mouse_pos, replay_button_rect):
                reset_game()
            if is_mouse_click_on_button(mouse_pos, quit_button_rect):
                quit_game()

    if not game_over:

        score += clock.get_time() / 1000.0
        display_score(score)
        # Key Presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_SPACE] and on_ground:
            player_y_speed = PLAYER_JUMP_SPEED
            on_ground = False

        player_rect = player_image.get_rect(topleft=(player_x, player_y))

        screen.blit(player_image, (player_x, player_y))

        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacles.append(create_random_obstacle())
            obstacle_timer = 0

        for obstacle in obstacles[:]:
            obstacle.x -= obstacle_speed
            pygame.draw.rect(screen, [255, 255, 0], obstacle)
            if obstacle.right < 0:
                obstacles.remove(obstacle)

        # Check for collisions
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                game_over = True
                high_score = max(high_score, score)
                break

        # Gravity
        if not on_ground:
            player_y_speed += GRAVITY
            player_y += player_y_speed
            # Check for ground collision
            if player_y > ground_level - player_image.get_height():
                player_y = ground_level - player_image.get_height()
                on_ground = True
                player_y_speed = 0

        screen.blit(player_image, (player_x, player_y))


    else:
        #high_score = max(high_score, score)
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        screen.fill([0, 0, 0])
        font = pygame.font.SysFont(None, 55)
        text = font.render('Nice one nerd', True, [255, 0, 0])
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 55))
        display_score(score)
        display_high_score(high_score)
        replay_button_rect = draw_replay_button()
        quit_button_rect = draw_quit_button()

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
