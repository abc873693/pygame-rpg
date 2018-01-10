import itertools
import sys
import time
import random
import math
import pygame
import colors
import sqliteHelper
from pygame.locals import *
from utils import *
from models import *
from sqliteHelper import *
from gameMenu import *
from TkinterHelper import *


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPG")
font = pygame.font.Font("fonts/msjh.ttf", 36)
font_small = pygame.font.Font("fonts/msjh.ttf", 14)
timer = pygame.time.Clock()


menu_state = 1
game_over = False
ID = 0
while menu_state != 0:
    # 主畫面
    if menu_state == 1:
        print('主畫面')
        position = enterMenu(pygame, screen, font, timer)
        print('position', position)
        menu_state = position + 2
        print('menu_state', menu_state)
    # 新遊戲
    elif menu_state == 2:
        print('新遊戲')
        ID = enterNewGame(pygame, screen, font, timer)
        if ID == -1:
            menu_state = 1
        else:
            editBox = TKEditBox('請輸入名字')
            editBox.loop()
            print(editBox.NAME.get())
            ID = sqliteHelper.insertGameRecord(ID, editBox.NAME.get())
            menu_state = 0
    # 載入遊戲
    elif menu_state == 3:
        print('載入遊戲')
        ID = enterLoadGame(pygame, screen, font, timer)
        print(ID)
        if ID == -1:
            menu_state = 1
        else:
            menu_state = 0
    # 排行榜
    elif menu_state == 4:
        print('排行榜')
        position = enterLoadRank(pygame, screen, font, timer)
        if position == -1:
            menu_state = 1
    # 離開
    elif menu_state == 5:
        menu_state = 0
        print('離開')
        game_over = True

monsters = getAllMonster()
# 讀取遊戲紀錄
gameRecord = getGameRecordByID(ID)
# 讀取腳色資料
characterType = getCharacterTypedByID(gameRecord.characterTypeID)


print(characterType.name)
print(monsters[0])

# 創建精靈組
player_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()

# 初始化玩家精靈組
player = CharacterSprite(gameRecord, characterType)
player_group.add(player)

# 初始化food精靈組
for n in range(1,20):
    food = MonsterSprite(monsters[1])
    # food.position = random.randint(0, 780), random.randint(0, 580)
    monster_group.add(food)
deleteMonsterRecordByGameRecordID(gameRecord.ID)
# 提示訊息
hintDataList = []
infoList = []
hpList = []

player_moving = False
player_HP = 0
player_currentHP = 0
hp_count = 0
time = 0
key_space_pressing = False
while not game_over:
    isAttack = False
    timer.tick(30)
    time = time + 1
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP:
            if key_space_pressing:
                key_space_pressing = False
    keys = pygame.key.get_pressed()

    if keys[K_SPACE]:

        if not key_space_pressing:
            print('attack')
            key_space_pressing = True
            isAttack = True

    if keys[K_ESCAPE]:
        game_over = True
        # sys.exit()

    elif keys[K_DOWN] or keys[K_s]:
        player.direction = 0
        player_moving = True

    elif keys[K_LEFT] or keys[K_a]:
        player.direction = 1
        player_moving = True

    elif keys[K_RIGHT] or keys[K_d]:
        player.direction = 2
        player_moving = True

    elif keys[K_UP] or keys[K_w]:
        player.direction = 3
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
            elif player.X > 780:
                player.X = 780
            if player.Y < -10:
                player.Y = -10
            elif player.Y > 580:
                player.Y = 580

        # 檢測玩家是否與食物衝突，是否吃到果實
        
        attacker = None
        attacker = monsterCanAttack(player, monster_group.sprites())
        if isAttack:
            if nearMonster != None:
                print(player.getAttack())
                attack = player.getAttack()
                nearMonster.currentHP -= attack
                hintDataList.append(HintData( player.gameRecord.characterName + '對怪物造成傷害' + str(attack)))
                if nearMonster.currentHP <= 0:
                    monster_group.remove(attacker)
                    hintDataList.append(
                        HintData(nearMonster.monsterData.name + '死亡'))
        if player.hurtCD > 0:
            player.hurtCD -=1
        player_HP = player.getMaxHP()
        player_currentHP = player.getCurrentHP()
        nearMonster = pygame.sprite.spritecollideany(player, monster_group)
        # print(nearMonster)
        print('CD' + str(player.hurtCD))
        if nearMonster != None:
            if pygame.sprite.collide_circle_ratio(0.65)(player, nearMonster):
                if player.hurtCD == 0:
                    player_currentHP -= int(nearMonster.monsterData.attack)
                    player.hurtCD = 50
                    hintDataList.append(HintData( nearMonster.monsterData.name + "對" + player.gameRecord.characterName + "造成傷害" + nearMonster.monsterData.attack ))         
        if player_currentHP != player_HP:
            hp_count = player_currentHP / player_HP
            hpList.append(TextData(350, 570, str(player_HP) + " / " + str(player_currentHP), colors.white))
        else:
            hp_count = 1
            hpList.append(TextData(350, 570, str(player_HP) + " / " + str(player_currentHP), colors.white))
        player.setCurrentHP(player_currentHP)
        # 更新精靈組
        monster_group.update(ticks, 50)

        # if len(monster_group) == 0:
        #     pass
        #     game_over = True

    # 人物當前資訊
    attack=player.getAttack()
    infoList.append(
        TextData(50, 500, player.characterTypeData.name, colors.white))
    infoList.append(
        TextData(30, 550, "LV." + str(player.gameRecord.getlevel()), colors.white))
    infoList.append(TextData(110, 550, "Attack:" + str(attack), colors.white))

    # 清除畫面
    screen.fill((50, 50, 100))

    # 繪製精靈
    monster_group.draw(screen)
    player_group.draw(screen)

    # 繪製玩家資訊
    for textData in infoList:
        print_text(font, textData.x, textData.y, textData.text, colors.white)

    # 繪製玩家血量條
    pygame.draw.rect(screen, (100, 200, 100, 180), Rect(300, 570, 200, 25), 2)
    print('hintDataList' + str( len(hintDataList)))
    
    # 顯示提示
    end = 0
    hintcount = 0
    if len(hintDataList) <= 10:
        end = 0
    else:
        end = len(hintDataList) - 10
    for i in range(end,len(hintDataList)):
        print_text(font_small, 560, 390+(hintcount+1) * 18, hintDataList[i].text)
        hintcount+=1
        if hintcount == 10:
            hintcount = 0
       
    if player_currentHP == player_HP :
        pygame.draw.rect(screen, (100, 200, 100, 180), Rect(300, 570, 200, 25), 0)
    else:
        pygame.draw.rect(screen, (50, 150, 50, 180),
                        Rect(300, 570, 200 * hp_count, 25), 0)
    print_text(font_small,350, 570, str(player.getMaxHP()) + " / " + str(player.getCurrentHP()),colors.white)

    if game_over:
        print_text(font,290,250,"Game Over!!!")
    pygame.display.update()

pygame.time.delay(1500)