import pygame, random, os

from pathlib import Path
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_SPACE
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


path = Path(__file__).parent.absolute()
os.chdir(path)

@login_required
def banderogoose(request):
    pygame.init()

    #Constants
    HEIGHT = 900
    WIDTH  = 1600
    COLOR_BLUE  = (0, 0, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_RED   = (255, 0, 0)
    COLOR_Y     = (255, 255, 0)
    FPS     = pygame.time.Clock()
    FONT    = pygame.font.SysFont("Calibri", 35)
    FONT_BK = pygame.font.SysFont("Calibri", 35)

    #background
    main_display = pygame.display.set_mode((WIDTH, HEIGHT))
    bg           = pygame.transform.scale(pygame.image.load("images/background.png"), (WIDTH, HEIGHT))
    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move =  3

    IMAGE_PATH    = "images/Goose"
    PLAYER_IMAGES = os.listdir(IMAGE_PATH)

    #Player
    player = pygame.image.load("images/player.png").convert_alpha()      # player_rect = pygame.Rect(main_display.get_rect().center, 0, *player_size)
    player_rect        = player.get_rect()
    player_rect.center = main_display.get_rect().center
    player_moveDN = [0, 10]
    player_moveUP = [0, -10]
    player_moveR  = [10, 0]
    player_moveL  = [-10, 0]


    #Enemy_&_Bonus creation
    CREATE_ENEMY = pygame.USEREVENT +1
    pygame.time.set_timer(CREATE_ENEMY, 2000)
    CREATE_BONUS = CREATE_ENEMY + 1
    pygame.time.set_timer(CREATE_BONUS, 4500)
    CHANGE_IMAGE = CREATE_BONUS + 1
    pygame.time.set_timer(CHANGE_IMAGE, 150)
    CREATE_MISSILE = CHANGE_IMAGE + 1


    #lists
    enemies, bonuses, missiles = list(), list(), list()
    score = 0
    bag   = 0
    image_index = 0


    #enemy
    def create_enemy():
        # enemy_size = (30, 30)
        enemy = pygame.image.load("images/enemy.png").convert_alpha()
        enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height(), HEIGHT - enemy.get_height()), *enemy.get_size())
        enemy_move = [random.randint(-10, -5), 0]
        return [enemy, enemy_rect, enemy_move]

    #bonus
    def create_bonus():
        # bonus_size = (30, 30)
        bonus = pygame.image.load("images/bonus.png").convert_alpha()
        bonus_width = bonus.get_width()
        bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH - bonus_width), 0, *bonus.get_size())
        # bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH -bonus_width),
        #                          -bonus.get_height(),
        #                          *bonus.get_size())
        bonus_move = [0, random.randint(4, 8)]
        return [bonus, bonus_rect, bonus_move]

    #missile
    def create_missile():
        missile = pygame.image.load("images/missile_1.png").convert_alpha()
        missile_move = [12, 0]
        missile_rect = player.get_rect()
        missile_rect = player_rect.move(missile_move)
        return [missile, missile_rect, missile_move]


    #game_cycle
    playing = True
    while playing:
        #background_movement
        bg_X1 -= bg_move
        bg_X2 -= bg_move
        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))
        main_display.blit(player, player_rect)
        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-75, 35))
        main_display.blit(FONT_BK.render(str(bag), True, COLOR_RED), (100, 35))


        FPS.tick(120)
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGE:
                player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0


        #player_movement
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_moveDN)
        if keys[K_UP] and player_rect.top >= 0:
            player_rect = player_rect.move(player_moveUP)
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_moveR)
        if keys[K_LEFT] and player_rect.left >= 0:
            player_rect = player_rect.move(player_moveL)
        #missile_movement
        if keys[K_SPACE] and not bag <= 0:
            missiles.append(create_missile())
            bag -= 1
        

        #enemies_cycle
        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])
            #enemy_collect
            if player_rect.colliderect(enemy[1]):
                playing = False
                enemies.pop(enemies.index(enemy))

        #bonuses_cycle
        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])
            #bonus_collect
            if player_rect.colliderect(bonus[1]):
                score += 1
                bag += 1
                bonuses.pop(bonuses.index(bonus))

        #missiles_cycle
        for missile in missiles:
            missile[1] = missile[1].move(missile[2])
            main_display.blit(missile[0], missile[1])
            #missiles_collect
            if missile[1].colliderect(enemy[1]):
                enemies.pop(enemies.index(enemy))
                missiles.pop(missiles.index(missile))


        #enemies&bonuses removal from collection
        for enemy in enemies:
            if enemy[1].left < 0:
                enemies.pop(enemies.index(enemy))
        for bonus in bonuses:
            if bonus[1].bottom > HEIGHT:
                bonuses.pop(bonuses.index(bonus))
        for missile in missiles:
            if missile[1].right >= WIDTH:
                missiles.pop(missiles.index(missile))
                
        
        pygame.display.flip()
    
        if playing == False:
            pygame.quit()
            return redirect("main:root")
