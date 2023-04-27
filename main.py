import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

backgroundImg = pygame.image.load("background.jpg")

mixer.music.load("background.mp3")
mixer.music.play(-1)

playerImg = pygame.image.load("player.png")
playerX = 368
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 7

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(10, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(20)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = -0.7
bullet_state = "Ready"

score_value = 0
font = pygame.font.Font("Dibujos Animados.otf", 32)
textX = 10
textY = 10

game_over_font=pygame.font.Font("Dibujos Animados.otf",64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 32:
        return True
    return False

def game_over_text():
    over_text=game_over_font.render("Game Over",True,(255,255,255))
    screen.blit(over_text,(230,250))

running = True
while running:
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bullet_sound=mixer.Sound("bullet fire.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    for i in range(no_of_enemies):
        if enemyY[i]>=448:
            for j in range(no_of_enemies):
                enemyY[j]=4000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound=mixer.Sound("blast.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(10, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    show_score(textX, textY)

    pygame.display.update()
