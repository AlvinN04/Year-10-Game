import pygame
import pygame.font
import pygame.mixer
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Window Dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sprites, Text, and Sound")

# Perry (Player)
sprite_image = pygame.image.load("sprite.png").convert_alpha()  
sprite_rect = sprite_image.get_rect()
sprite_rect.center = (width // 2, height - 50)
sprite_speed = 5

# Dr (Enemy)
penguin_image = pygame.image.load("penguin.png").convert_alpha()  
penguin_rect = penguin_image.get_rect()
penguin_rect.topleft = (100, 50)
penguin_speed = 3

#Camera
camera_x = 0
camera_y = 0

backround_image = pygame.image.load("backround").convert()
backround_rect = backround_image.get_rect()


# Score
score = 0
font = pygame.font.Font(None, 36)

# Sound
collision_sound = pygame.mixer.Sound("applause.wav")

#Game State
game_state = "MENU"

#Buttons
play_button = pygame.Rect(width // 2- 100, height // 2- 50, 200,50)
quit_button = pygame.Rect(width// 2- 100, height //2 + 50, 200, 50)
play_again_button = pygame.Rect(width// 2- 100, height // 2, 200, 50) #for game over state

def menu_state ():
    screen.fill((0,0,0))
pygame.penguinaw.rect(screen, (0, 255,0), play_button)
pygame.penguinaw.rect (screen, (255, 0,0), quit_button)

title_text = font.render("Perry v Dr", True, (255,255,255))
title_rect = title_text.get_rect(center=(width// 2, height // 4))

play_text = font.render("Play", True, (0,0,0))
play_rect= title_text.get._rect(center= quit_button.center)

quit_text = font.render("Quit", True, (0,0,0))
quit_rect = quit_text.get_rect(center= quit_button.center)

screen.blit(title_text, title_rect)
screen.blit(play_text, play_rect)
screen.blit(quit_text, quit_rect)

def playing_state():

    keys = pygame.key.get_pressed()

    # Perry Movement
    if keys[pygame.K_RIGHT]:
        sprite_rect.x += sprite_speed
    if keys[pygame.K_LEFT]:
        sprite_rect.x -= sprite_speed

    # Dr Movement
    if penguin_rect.centerx< sprite_rect.centerx:
        penguin_rect.x += penguin_speed
    elif penguin_rect.centerx> sprite_rect.centerx:
        penguin_rect.x-=penguin_speed

    if penguin_rect.centery < sprite_rect.centery:
        penguin_rect.y += penguin_speed
    elif penguin_rect.centery > sprite_rect.centery:
        penguin_rect.y-= penguin_speed

    # Boundary Checks
    if sprite_rect.left < 0:
        sprite_rect.left = 0
    if sprite_rect.right > width:
        sprite_rect.right = width

    # Collision Detection
    if sprite_rect.colliderect(penguin_rect):
        score += 1
        collision_sound.play()
        # Reset Dr position
        penguin_rect.topleft = (100, 50)

    # Score Text
    text_surface = font.render("Score: " + str(score), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (10, 10)

    # Drawing
    screen.fill((0, 0, 0))  # Clear screen
    screen.blit(sprite_image, sprite_rect)
    screen.blit(penguin_image, penguin_rect)
    screen.blit(text_surface, text_rect)

def game_over_state():
    global score, penguin_rect
    screen.fill((0,0,0))
    game_over_text = font.render("Game Over! SCORE:" + str(score), True, (255,255,255))
    game_over_rect = game_over_text.get_rect(center= (width//2, height// 4))
    screen.blit(game_over_text, game_over_rect)

    pygame.penguinaw.rect(screen, (0,255,0), play_again_button)
    play_again_text = font.render("Play Again", True,(0,0,0))
    play_again_rect= play_again_text.get_rect(center= play_again_button.center)
    screen.blit(play_again_text, play_again_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU":
                if play_button.collidepoint(event.pos):
                    game_state = "PLAYING"
                    score=0
                    penguin_rect.topleft = (100,50)
                elif quit_button.collidepoint(event.pos):
                    running = False
            elif game_state == "GAME_OVER":
                if play_again_button.collidepoint(event.pos):
                    game_state = "PLAYING"
                    score= 0
                    penguin_rect.topleft = (100,50)

        if game_state == "MENU":
            menu_state()
        elif game_state == "PLAYING":
            playing_state
        elif game_state == "GAME_OVER":
            game_over_state()
    pygame.display.flip()

pygame.quit()