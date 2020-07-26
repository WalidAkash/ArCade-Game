import pygame
import random
import math
from pygame import mixer

pygame.init()

# create the game window
screen = pygame.display.set_mode((800, 600))

# set the icon and caption
pygame.display.set_caption('Space Fight')
icon = pygame.image.load('ubu.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('back.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# add spaceship image
playerImg = pygame.image.load('invaders.png')
playerX = float(380)
playerY = float(450)
playerX_change = 0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_enemies=6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 450
bulletX_change = 0
bulletY_change= 10
bullet_state = 'Ready'

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render('Score : '+ str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text= over_font.render('GAME OVER', True, (255,255,255))
    screen.blit(over_text,(200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='Fire'
    screen.blit(bulletImg, (x+16,y+10))

#Collision function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2))+(math.pow(enemyY-bulletY, 2)))
    if distance<27:
        return True
    else:
        return False

# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard movement: uses of left_key and right_key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                print('Left key is pressed')

            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                print('Right key is pressed')

            if event.key==pygame.K_SPACE:
                if bullet_state =='Ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print('Left or Right key is up')

    #player movement
    playerX += playerX_change

    #checking the player boundary
    if playerX < 0:
        playerX = 0
    if playerX > 736:
        playerX = 736

    #enemy movement
    for i in range(num_enemies):

        #game over
        if enemyY[i] >400:
            for j in range(num_enemies):
                enemyY[j]=2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i]<0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        if enemyX[i]>736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision is True:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 450
            bullet_state = 'Ready'
            score_value = score_value + 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


    #bullet movement
    if bulletY<=0:
        bulletY = 450
        bullet_state = 'Ready'
    if bullet_state is 'Fire':
        fire_bullet(bulletX, bulletY)
        bulletY-=bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
