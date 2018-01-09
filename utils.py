# utils.py

import sys
import time
import random
import math
import pygame
from pygame.locals import *


# prints text using the supplied font
def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    # req'd when function moved into MyLibrary
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x, y))


def calc_velocity(direction, vel=1.0):
    velocity = Point(0, 0)  # 速度
    if direction == 0:  # 下
        velocity.y = vel

    elif direction == 1:  # 左
        velocity.x = -vel

    elif direction == 2:  # 右
        velocity.x = vel

    elif direction == 3:  # 上
        velocity.y = -vel

    return velocity


def fibonacci(n, fib=[0, 1]):
    if n >= len(fib):
        for i in range(len(fib), n + 1):
            fib.append(fib[i - 1] + fib[i - 2])
    return fib[n]


def monsterCanAttack(player, monsterSpriteList):
    range = 32
    halfRange = range / 2
    x = player.X
    y = player.Y
    if player.direction == 3: #上
        for monsterSprite in monsterSpriteList:
            if((x - halfRange <= monsterSprite.X & monsterSprite.X <= x + range) & (y >= monsterSprite.Y & monsterSprite.Y >= y - range)):
                return monsterSprite
    elif player.direction == 0: #下
        for monsterSprite in monsterSpriteList:
            if((x - halfRange <= monsterSprite.X & monsterSprite.X <= x + range) & (y <= monsterSprite.Y & monsterSprite.Y <= y + range)):
                return monsterSprite
    elif player.direction == 1: #左
        for monsterSprite in monsterSpriteList:
            if((x >= monsterSprite.X & monsterSprite.X >= x - range) & (y <= monsterSprite.Y & monsterSprite.Y <= y + range)):
                return monsterSprite
    elif player.direction == 2: #右
        for monsterSprite in monsterSpriteList:
            if((x <= monsterSprite.X & monsterSprite.X <= x + range) & (y <= monsterSprite.Y & monsterSprite.Y <= y + range)):
                return monsterSprite
    return None
