import pygame
import pygame.mixer
import pygame.font
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Window Dimensions
width = 800
height = 600
level_width = 800
level_height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Side Scrolling")

# Font
font = pygame.font.Font(None, 36)

# Background
background = pygame.image.load("background.jpg").convert()
background = pygame.transform.scale(background, (width, height))

# Player sprite
sprite_image = pygame.image.load("sprite.png").convert_alpha()
sprite_rect = sprite_image.get_rect()
sprite_rect.center = (width // 2, height - 50)
sprite_speed = 5

def gravity(sprite_rect):
    sprite_rect.y += 3.2  # Simulates falling

# Enemy sprite
penguin_image = pygame.image.load("penguin.png").convert_alpha()
penguin_rect = penguin_image.get_rect()
penguin_rect.center = (width // 2, 300)
penguin_speed = 1

# Score
score = 0

# Clock (frames per second)
clock = pygame.time.Clock()

# Sound
pygame.mixer.music.load("applause.wav")
pygame.mixer.music.set_volume(0.7)

# Game state
game_state = "MENU"

# Buttons
play_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 50)
quit_button = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
settings_button = pygame.Rect(width // 2 - 100, height // 2 + 150, 200, 50)
play_again_button = pygame.Rect(width // 2 - 100, height // 2, 200, 50)
pause_button = pygame.Rect(width - 100, 10, 80, 40)
back_button = pygame.Rect(width // 2 - 100, height // 2, 200, 50)

def menu_state():
    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    pygame.draw.rect(screen, (190, 190, 190), settings_button)

    title_text = font.render("Jump", True, (255, 255, 255))
    play_text = font.render("Play", True, (0, 0, 0))
    quit_text = font.render("Quit", True, (0, 0, 0))
    settings_text = font.render("Settings", True, (0, 0, 0))

    screen.blit(title_text, title_text.get_rect(center=(width // 2, height // 4)))
    screen.blit(play_text, play_text.get_rect(center=play_button.center))
    screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))
    screen.blit(settings_text, settings_text.get_rect(center=settings_button.center))

def settings_state():
    screen.fill((50, 50, 50))  
    settings_text = font.render("Settings", True, (255, 255, 255))
    back_text = font.render("Back", True, (0, 0, 0))

    screen.blit(settings_text, settings_text.get_rect(center=(width // 2, height // 4)))
    pygame.draw.rect(screen, (190, 190, 190), back_button)
    screen.blit(back_text, back_text.get_rect(center=back_button.center))

def playing_state():
    global score

    gravity(sprite_rect)
    keys = pygame.key.get_pressed()

    screen.blit(background, (0, 0))

    # Camera boundaries to prevent moving out of the level
    if camera_x > 0:
        camera_x = 0
    if camera_x < -level_width + width:
        camera_x = -level_width + width

    if camera_y > 0:
        camera_y = 0
    if camera_y < -level_height + height:
        camera_y = -level_height + height

    # Player movement
    if keys[pygame.K_RIGHT]:
        sprite_rect.x += sprite_speed
    if keys[pygame.K_LEFT]:
        sprite_rect.x -= sprite_speed
    if keys[pygame.K_UP]:
        sprite_rect.y -= sprite_speed
    if keys[pygame.K_DOWN]:
        sprite_rect.y += sprite_speed

    # Draw player and enemy
    screen.blit(sprite_image, sprite_rect)
    screen.blit(penguin_image, penguin_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def pause_state():
    screen.fill((0, 0, 0))  # Clear screen (black)
    
    pause_text = font.render("PAUSED", True, (255, 255, 255))
    screen.blit(pause_text, pause_text.get_rect(center=(width // 2, height // 4)))

    pygame.draw.rect(screen, (0, 255, 0), play_button)
    resume_text = font.render("Resume", True, (0, 0, 0))
    screen.blit(resume_text, resume_text.get_rect(center=play_button.center))

    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    quit_text = font.render("Quit", True, (0, 0, 0))
    screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU":
                if play_button.collidepoint(event.pos):
                    game_state = "PLAYING"
                elif quit_button.collidepoint(event.pos):
                    running = False
                elif settings_button.collidepoint(event.pos):
                    game_state = "SETTINGS"

            elif game_state == "SETTINGS":
                if back_button.collidepoint(event.pos):
                    game_state = "MENU"

            elif game_state == "PAUSE":
                if play_button.collidepoint(event.pos):
                    game_state = "PLAYING"
                elif quit_button.collidepoint(event.pos):
                    running = False

        # Press 'P' to pause or unpause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  
                if game_state == "PLAYING":
                    game_state = "PAUSE"
                elif game_state == "PAUSE":
                    game_state = "PLAYING"

    if game_state == "MENU":
        menu_state()
    elif game_state == "SETTINGS":
        settings_state()
    elif game_state == "PLAYING":
        playing_state()
    elif game_state == "PAUSE":
        pause_state()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
