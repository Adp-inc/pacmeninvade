import pygame
from pygame import mixer
import random
import math
import time

# intitulize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode([800, 450])

#title and icon
pygame.display.set_caption('Invade of pacmen')
icon = pygame.image.load('Pacman.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('Ghost.png')
playerx = 370
playery = 350
playerx__change = 0

# bullet

# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bulletImg = pygame.image.load('dot.png')
bulletx = 0
bullety = 350
bulletx__change = 0
bullety_change = 1
bullet_state = "ready"

# enemy

enemyImg = []
enemyx = []
enemyy = []
enemyx__change = []
enemyy_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Pacman.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx__change.append(0.3)
    enemyy_change.append(40)

#start sound
mixer.music.load('game_start.wav')
mixer.music.play()
time.sleep(5)
# background
background = pygame.image.load('Pacman_background.jpg')
#background sound
mixer.music.load('intermission.wav')
mixer.music.play(-1)
#font
score_value = 0
font = pygame.font.Font('zeldadxt.ttf', 32)

textx = 10
texty = 10

#game over text
over_font = pygame.font.Font('Triforce.ttf' , 64)

def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (0,240,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0,240,255))
    screen.blit(over_text, (200, 225))
    
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) +
                         (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
        #game over
    if enemyy[i] > playery:
        for j in range(num_of_enemies):
                enemyy[j] = 2000
                death2_sound = mixer.Sound('death_1.wav')
                game_over_text()
                death2_sound.play()
                break
    # RGB - red, green, blue
    screen.fill((154, 247, 255))
    # backgrounhd image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx__change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx__change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('eat_ghost.wav')
                    bullet_sound.play()
                    # get the current x cordnate of player
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx__change = 0
    # 5 = 5 + -0.1 -> 5= 5 -0.1
    # 5= 5+0.1

    playerx += playerx__change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    #enemy movement    
    for i in range(num_of_enemies):
        

        
        enemyx[i] += enemyx__change[i]
        if enemyx[i] <= 0:
            enemyx__change[i] = 0.3
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx__change[i] = -0.3
        #collision
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 350
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
            death_sound = mixer.Sound('death_2.wav')
            death_sound.play()
        else:
            pass
        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 350
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change
    else:
        pass 

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
