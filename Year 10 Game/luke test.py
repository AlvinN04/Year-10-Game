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
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("side scrolling")

# Font
font = pygame.font.Font(None, 36)

# Rendering text
text_surface = font.render("score:0", True, (255, 255, 255)) 
text_rect = text_surface.get_rect()
text_rect.topleft = (10, 10)  

# Player sprite
sprite_image = pygame.image.load("sprite.png").convert_alpha()
sprite_rect = sprite_image.get_rect()
sprite_rect.center = (width // 2, height - 50)
sprite_speed = 5

# Enemy sprite
penguin_image = pygame.image.load("penguin.png").convert_alpha()
penguin_rect = penguin_image.get_rect()
penguin_rect.center = (width // 2, 300)
penguin_speed = 1
penguin_width = penguin_rect.width
penguin_height = penguin_rect.height

#camrea
camrera_x = 0
camrera_y = 0

backround_image = pygame.image.load("backround").convert()
backround_rect = backround_image.get_rect()


# Score 
score = 0
font = pygame.font.Font(None, 36)

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
play_again_button = pygame.Rect(width // 2 - 100, height // 2, 200, 50)  # For game-over state
pause_button = pygame.Rect(width - 100, 10, 80, 40)  # Button to pause the game

def menu_state():
    screen.fill((0, 0, 0))  # Clear screen (black)
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)

    title_text = font.render("Jump", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(width // 2, height // 4))

    play_text = font.render("Play", True, (0, 0, 0))
    play_rect = play_text.get_rect(center=play_button.center)

    quit_text = font.render("Quit", True, (0, 0, 0))
    quit_rect = quit_text.get_rect(center=quit_button.center)

    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(quit_text, quit_rect)

def playing_state():
    global score

    keys = pygame.key.get_pressed()

    # Player Movement
    if keys[pygame.K_RIGHT]:
        sprite_rect.x += sprite_speed
    if keys[pygame.K_LEFT]:
        sprite_rect.x -= sprite_speed
    if keys[pygame.K_UP]:
        sprite_rect.y -= sprite_speed
    if keys[pygame.K_DOWN]:
        sprite_rect.y += sprite_speed

    # Boundary Checks for Player
    if sprite_rect.left < 0:
        sprite_rect.left = 0
    if sprite_rect.right > width:
        sprite_rect.right = width
    if sprite_rect.top < 0:
        sprite_rect.top = 0
    if sprite_rect.bottom > height:
        sprite_rect.bottom = height

    # Enemy Movement (simple auto movement)
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
        pygame.mixer.music.play()
        score += 1  # Increase score on collision

    # Drawing
    screen.fill((0, 0, 0))  # Clear screen (black)
    screen.blit(sprite_image, sprite_rect)  # Draw player sprite
    screen.blit(penguin_image, penguin_rect)  # Draw enemy sprite

    # Rendering the score text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def game_over_state():
    global score
    global camera_x, camera_y
    screen.fill((0, 0, 0))  # Clear screen (black)
    game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 4))
    screen.blit(game_over_text, game_over_rect)

    pygame.draw.rect(screen, (0, 255, 0), play_again_button)
    play_again_text = font.render("Play Again", True, (0, 0, 0))
    play_again_rect = play_again_text.get_rect(center=play_again_button.center)
    screen.blit(play_again_text, play_again_rect)

def pause_state():
    screen.fill((0, 0, 0))  # Clear screen (black)
    pause_text = font.render("PAUSED", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(width // 2, height // 4))
    screen.blit(pause_text, pause_rect)

    pygame.draw.rect(screen, (0, 255, 0), play_button)
    resume_text = font.render("Resume", True, (0, 0, 0))
    resume_rect = resume_text.get_rect(center=play_button.center)
    screen.blit(resume_text, resume_rect)

    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    quit_text = font.render("Quit", True, (0, 0, 0))
    quit_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU":
                if play_button.collidepoint(event.pos):
                    game_state = "PLAYING"
                    score = 0
                    penguin_rect.topleft = (100, 50)
                elif quit_button.collidepoint(event.pos):
                    running = False

            elif game_state == "GAME_OVER":
                if play_again_button.collidepoint(event.pos):
                    game_state = "PLAYING"
                    score = 0
                    penguin_rect.topleft = (100, 50)

            elif game_state == "PAUSE":
                if play_button.collidepoint(event.pos):  # Resume game
                    game_state = "PLAYING"
                elif quit_button.collidepoint(event.pos):  # Quit game
                    running = False

        # Press 'P' to pause or unpause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Toggle pause
                if game_state == "PLAYING":
                    game_state = "PAUSE"
                elif game_state == "PAUSE":
                    game_state = "PLAYING"

    if game_state == "MENU":
        menu_state()
    elif game_state == "PLAYING":
        playing_state()
    elif game_state == "GAME_OVER":
        game_over_state()
    elif game_state == "PAUSE":
        pause_state()

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
