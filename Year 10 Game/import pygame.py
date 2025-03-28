import pygame
import pygame.font
import pygame.mixer
import random

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Window Dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving and Interacting")

# Font
font = pygame.font.Font(None, 36)

# Rendering Text
text_surface = font.render("Score: 0", True, (255, 255, 255))
text_rect = text_surface.get_rect()
text_rect.topleft = (10, 10)

# Player
sprite_image = pygame.image.load("sprite.png").convert_alpha()
sprite_rect = sprite_image.get_rect()
sprite_rect.center = (width // 2, height - 50)
sprite_speed = 5

# Enemy
penguin_image = pygame.image.load("penguin.png").convert_alpha()
penguin_rect = penguin_image.get_rect()
penguin_rect.center = (width // 2, 50)
penguin_speed = 3



# Score
score = 0

# Game state
game_state = "MENU"

# Buttons
play_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 50)
quit_button = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)  # Adjusted for better placement
play_again_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 50)

# Menu State
def menu_state():
    screen.fill((0, 0, 0))  # Fixed screen fill
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)

    title_text = font.render("Penguin Collision", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(width // 2, height // 4))

    play_text = font.render("Play", True, (0, 0, 0))
    play_rect = play_text.get_rect(center=play_button.center)

    quit_text = font.render("Quit", True, (0, 0, 0))
    quit_rect = quit_text.get_rect(center=quit_button.center)

    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(quit_text, quit_rect)

# Playing State
def playing_state():
    global score, text_surface
    keys = pygame.key.get_pressed()
    # Player Movement
    if keys[pygame.K_RIGHT] and sprite_rect.right < width:
        sprite_rect.x += sprite_speed
    if keys[pygame.K_LEFT] and sprite_rect.left > 0:
        sprite_rect.x -= sprite_speed
    if keys[pygame.K_UP] and sprite_rect.top > 0:
        sprite_rect.y -= sprite_speed
    if keys[pygame.K_DOWN] and sprite_rect.bottom < height:
        sprite_rect.y += sprite_speed

    # Enemy Movement (AI tracking)
    if penguin_rect.centerx < sprite_rect.centerx:
        penguin_rect.x += penguin_speed
    elif penguin_rect.centerx > sprite_rect.centerx:
        penguin_rect.x -= penguin_speed
    if penguin_rect.centery < sprite_rect.centery:
        penguin_rect.y += penguin_speed
    elif penguin_rect.centery > sprite_rect.centery:
        penguin_rect.y -= penguin_speed

    # Collision Detection
    if sprite_rect.colliderect(penguin_rect):
        score += 1
        text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        penguin_rect.topleft = (random.randint(0, width - penguin_rect.width), random.randint(0, height // 2))

        collision_sound = pygame.mixer.Sound("applause.wav")
        collision_sound.play()

    # Drawing
    screen.fill((0, 0, 0))  # Clear screen (black)
    screen.blit(sprite_image, sprite_rect)
    screen.blit(penguin_image, penguin_rect)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

# Game Over State
def game_over_state():
    global score
    screen.fill((0, 0, 0))  # Fixed screen fill
    game_over_text = font.render("Game Over! Score: " + str(score), True)
pygame.quit()