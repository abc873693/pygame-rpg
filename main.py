import itertools
import sys
import time
import random
import math
import pygame
from pygame.locals import *
from utils import *
from models import *
from sqliteHelper import *


def calc_velocity(direction, vel=1.0):
    velocity = Point(0, 0)  # 速度
    if direction == 0:  # 上
        velocity.y = -vel
    elif direction == 1:  # 右上
        velocity.x = vel
        velocity.y = -vel
    elif direction == 2:  # 右
        velocity.x = vel
    elif direction == 3:  # 右下
        velocity.x = vel
        velocity.y = vel
    elif direction == 4:  # 下
        velocity.y = vel
    elif direction == 5:  # 右
        velocity.x = -vel
        velocity.y = vel
    elif direction == 6:  # 左
        velocity.x = -vel
    elif direction == 7:  # 右
        velocity.x = -vel
        velocity.y = -vel
    return velocity


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPG")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()

monsters = getAllCharacterType()
# 讀取遊戲紀錄
gameRecord = getGameRecordByID(1)
# 讀取腳色資料
characterType = getCharacterTypedByID(gameRecord.characterTypeID)

print(characterType.name)

print(monsters[0])

# 創建精靈組
player_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

# 初始化玩家精靈組
player = CharacterSprite(gameRecord, characterType)
player_group.add(player)

# 初始化food精靈組
for n in range(1, 10):
    food = MySprite()
    food.load("images/food_low.png", 35, 35, 1)
    food.position = random.randint(0, 780), random.randint(0, 580)
    food_group.add(food)

game_over = False
player_moving = False
player_health = 0
time = 0

while True:
    timer.tick(30)
    time = time + 1
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_UP] or keys[K_w]:
        player.direction = 0
        player_moving = True
    elif keys[K_e]:
        player.direction = 1
        player_moving = True
    elif keys[K_RIGHT] or keys[K_d]:
        player.direction = 2
        player_moving = True
    elif keys[K_c]:
        player.direction = 3
        player_moving = True
    elif keys[K_DOWN] or keys[K_s]:
        player.direction = 4
        player_moving = True
    elif keys[K_z]:
        player.direction = 5
        player_moving = True
    elif keys[K_LEFT] or keys[K_a]:
        player.direction = 6
        player_moving = True
    elif keys[K_q]:
        player.direction = 7
        player_moving = True
    else:
        player_moving = False

    if not game_over:
        # 根據角色的不同方向，使用不同的動畫幀
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns - 1
        if player.frame < player.first_frame:
            player.frame = player.first_frame

        if not player_moving:
            # 當停止按鍵（即人物停止移動的時候），停止更新動畫幀
            player.frame = player.first_frame = player.last_frame
        else:
            player.velocity = calc_velocity(player.direction, 3)
            player.velocity.x *= 3
            player.velocity.y *= 3

        # 更新玩家精靈組
        player_group.update(ticks, 50)

        # 移動玩家
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < -10:
                player.X = -10
            elif player.X > 800:
                player.X = 800
            if player.Y < -10:
                player.Y = -10
            elif player.Y > 600:
                player.Y = 600

        # 檢測玩家是否與食物衝突，是否吃到果實
        attacker = None
        attacker = pygame.sprite.spritecollideany(player, food_group)
        if attacker != None:
            if pygame.sprite.collide_circle_ratio(0.65)(player, attacker):
                player_health += 50
                food_group.remove(attacker)
        if player_health > 100:
            player_health = 100
        # 更新食物精靈組
        food_group.update(ticks, 50)

        if len(food_group) == 0:
            game_over = True
    # 清除畫面
    screen.fill((50, 50, 100))

    # 繪製精靈
    food_group.draw(screen)
    player_group.draw(screen)

    # 繪製玩家血量條
    pygame.draw.rect(screen, (50, 150, 50, 180),
                     Rect(300, 570, player_health * 2, 25))
    pygame.draw.rect(screen, (100, 200, 100, 180), Rect(300, 570, 200, 25), 2)

    if game_over:
        print('game over')

    pygame.display.update()
