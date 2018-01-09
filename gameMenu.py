import itertools
import sys
import time
import random
import math
import pygame
import colors
from utils import *
from models import *
from sqliteHelper import *


def enterMenu(pygame, screen, font, timer):
    mode = 0
    position = 0
    key_pressing = False
    textList = []
    textList.append(TextData(300, 300, '新遊戲', colors.white))
    textList.append(TextData(300, 350, '載入遊戲', colors.white))
    textList.append(TextData(300, 400, '排行榜', colors.white))
    textList.append(TextData(300, 450, '離開', colors.white))
    max = len(textList)

    while True:
        timer.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressing = True
                pass
            elif event.type == pygame.KEYUP:
                key_pressing = False
                if mode == 1:
                    position = position - 1
                    if(position < 0):
                        position = 0
                elif mode == 2:
                    position = position + 1
                    if(position > max - 1):
                        position = max - 1
                elif mode == -1:
                    return position
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pass
        elif keys[K_UP] or keys[K_w]:
            mode = 1
        elif keys[K_DOWN] or keys[K_s]:
            mode = 2
        elif keys[K_KP_ENTER]:
            mode = -1
        else:
            mode = 0
        # 清除畫面
        screen.fill((50, 50, 100))
        # 繪製
        for textData in textList:
            print_text(font, textData.x, textData.y,
                       textData.text, colors.white)
        # print(textList[position].getTextSize())
        pygame.draw.rect(screen, (100, 200, 100, 180),
                         Rect(textList[position].x, textList[position].y, (4 * 36), 50), 2)
        pygame.display.update()

# 新遊戲


def enterNewGame(pygame, screen, font, timer):
    font_small = pygame.font.Font("fonts/msjh.ttf", 24)
    # max = 3
    mode = 0
    position = 0
    key_pressing = False
    characterTypeList = getAllCharacterType(CharacterTypeData)
    # print(characterType.name)
    imageDataList = []
    textList = []
    textSmallList = []
    startX = 100
    startY = 100
    characterTypeGroup = pygame.sprite.Group()
    textList.append(TextData(100, 100, '請選擇角色', colors.white))
    i = 0
    for characterType in characterTypeList:
        offsetX = 150 * i
        gameRecordData = GameData(startX + offsetX ,startY ,3)
        characterTypeGroup.add(CharacterSprite(gameRecordData, characterType))
        textSmallList.append(TextData(startX + offsetX, startY +
                                 100, characterType.name, colors.white))
        textSmallList.append(TextData(startX + offsetX, startY + 130,
                                 'HP:' + str(characterType.initHP), colors.white))
        textSmallList.append(TextData(startX + offsetX, startY + 160,
                                 '攻擊力:' + str(characterType.initAttack), colors.white))
        i = i + 1
        if i == 3:
            startY = startY + 300
            i = 0

    max = len(textList)
    while True:
        print(position)
        timer.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressing = True
                pass
            elif event.type == pygame.KEYUP:
                key_pressing = False
                if mode == 1:
                    position = position - 1
                    if(position < 0):
                        position = 0
                elif mode == 2:
                    position = position + 1
                    if(position > max - 1):
                        position = max - 1
                elif mode == -1:
                    return position
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            print('K_ESCAPE')
            return -1
        elif keys[K_UP] or keys[K_w]:
            mode = 1
        elif keys[K_DOWN] or keys[K_s]:
            mode = 2
        elif keys[K_KP_ENTER]:
            print('Enter')
            return position
        else:
            mode = 0
        characterTypeGroup.update(ticks, 50)
        # 清除畫面
        screen.fill((50, 50, 100))
        characterTypeGroup.draw(screen)
        # 繪製
        for textData in textList:
            print_text(font, textData.x, textData.y,
                       textData.text, colors.white)
        for textData in textSmallList:
            print_text(font_small, textData.x, textData.y,
                       textData.text, colors.white)
        pygame.draw.rect(screen, (100, 200, 100, 180),
                         Rect(textList[position].x, textList[position].y, (4 * 36), 50), 2)
        pygame.display.update()

# 載入遊戲


def enterLoadGame(pygame, screen, font, timer):
    max = 3
    mode = 0
    position = 0
    key_pressing = False
    gameRecordList = getAllGameRecord()
    textList = []
    textList.append(TextData(100, 100, '載入遊戲', colors.white))
    max = len(gameRecordList)
    while True:
        print(position)
        timer.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressing = True
                pass
            elif event.type == pygame.KEYUP:
                key_pressing = False
                if mode == 1:
                    position = position - 1
                    if(position < 0):
                        position = 0
                elif mode == 2:
                    position = position + 1
                    if(position > max - 1):
                        position = max - 1
                elif mode == -1:
                    return position
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            return -1
        elif keys[K_UP] or keys[K_w]:
            mode = 1
        elif keys[K_DOWN] or keys[K_s]:
            mode = 2
        elif keys[K_KP_ENTER]:
            print('Enter')
            return position
        else:
            mode = 0
        # 清除畫面
        screen.fill((50, 50, 100))
        # 繪製
        for textData in textList:
            print_text(font, textData.x, textData.y,
                       textData.text, colors.white)
        pygame.draw.rect(screen, (100, 200, 100, 180),
                         Rect(textList[position].x, textList[position].y, (4 * 36), 50), 2)
        pygame.display.update()

# 排行榜


def enterLoadRank(pygame, screen, font, timer):
    max = 3
    mode = 0
    position = 0
    key_pressing = False
    gameRecordList = getAllGameRecord()
    # print sorted(gameRecordList, key=lambda gameRecordList: gameRecordList[].experience))
    startX = 200
    startY = 200
    textList = []
    textList.append(TextData(100, 100, '排行榜', colors.white))
    textList.append(TextData(100, 150, '名稱', colors.white))
    textList.append(TextData(300, 150, '角色', colors.white))
    textList.append(TextData(550, 150, '等級', colors.white))
    i = 0
    for gameRecord in gameRecordList :
        offsetY = 50 * i
        i = i+1
        textList.append(TextData(100, startY + offsetY, gameRecord.characterName, colors.white))

    textList.append(TextData(300, 200, '我是角色名稱', colors.white))
    textList.append(TextData(550, 200, str(
        gameRecordList[0].experience), colors.white))
    textList.append(TextData(550, 250, str(
        gameRecordList[1].experience), colors.white))
    textList.append(TextData(550, 300, str(
        gameRecordList[2].experience), colors.white))

    max = len(gameRecordList)
    while True:
        print(position)
        timer.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressing = True
                pass
            elif event.type == pygame.KEYUP:
                key_pressing = False
                if mode == 1:
                    position = position - 1
                    if(position < 0):
                        position = 0
                elif mode == 2:
                    position = position + 1
                    if(position > max - 1):
                        position = max - 1
                elif mode == -1:
                    return position
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            return -1
        elif keys[K_UP] or keys[K_w]:
            mode = 1
        elif keys[K_DOWN] or keys[K_s]:
            mode = 2
        elif keys[K_KP_ENTER]:
            print('Enter')
            return position
        else:
            mode = 0
        # 清除畫面
        screen.fill((50, 50, 100))
        # 繪製
        for textData in textList:
            print_text(font, textData.x, textData.y,
                       textData.text, colors.white)
        pygame.display.update()
