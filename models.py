import pygame
import random
import sqliteHelper
from pygame.locals import *


# CharacterSprite class extends pygame.sprite.Sprite
class CharacterSprite(pygame.sprite.Sprite):

    def __init__(self, gameRecord, characterTypeData):
        pygame.sprite.Sprite.__init__(self)  # extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0, 0.0)
        self.gameRecord = gameRecord
        self.characterTypeData = characterTypeData
        fileNmae = 'images/character/%s' % (characterTypeData.imageName)
        self.load(fileNmae, 32, 32, 3)
        self.position = (gameRecord.currentX, gameRecord.currentY)
        self.direction = gameRecord.currentDirection
        self.hurtCD = 0

    # X property
    def _getx(self): return self.rect.x

    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property
    def _gety(self): return self.rect.y

    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft

    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    def getAttack(self):
        return (self.characterTypeData.initAttack + self.gameRecord.getlevel() * self.characterTypeData.bonusAttack)
        
    def getMaxHP(self):
        return (self.characterTypeData.initHP + self.gameRecord.getlevel() * self.characterTypeData.bonusHP)

    def getCurrentHP(self):
        return self.gameRecord.currentHP

    def setCurrentHP(self,HP):
        self.gameRecord.currentHP = HP

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        # update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        # build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
            "," + str(self.last_frame) + "," + str(self.frame_width) + \
            "," + str(self.frame_height) + "," + str(self.columns) + \
            "," + str(self.rect)


class MonsterSprite(pygame.sprite.Sprite):

    def __init__(self, monsterData):
        pygame.sprite.Sprite.__init__(self)  # extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0, 0.0)
        self.monsterData = monsterData
        self.currentHP = monsterData.HP
        fileNmae = 'images/monster/%s' % (monsterData.imageName)
        self.load(fileNmae, 32, 32, 3)
        self.position = (monsterData.imageStartX, monsterData.imageStartY)
        self.direction = 1  # direction
        self.move()

    # X property
    def _getx(self): return self.rect.x

    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property
    def _gety(self): return self.rect.y

    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft

    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        # update animation frame number
        self.move()
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        # build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def move(self):
        randint = random.randrange(0, 100)
        monster_direction = randint % 4
        if monster_direction == 0:
            food_moving = True
        elif monster_direction == 1:
            food_moving = True
        elif monster_direction == 2:
            food_moving = True
        elif monster_direction == 3:
            food_moving = True

        # 根據角色的不同方向，使用不同的動畫幀
        self.first_frame = monster_direction * self.columns
        self.last_frame = self.first_frame + self.columns - 1
        if self.frame < self.first_frame:
            self.frame = self.first_frame

        self.velocity = calc_velocity(monster_direction, 3)
        self.velocity.x *= 1
        self.velocity.y *= 1

        self.X += self.velocity.x
        self.Y += self.velocity.y
        if self.X < -10:
            self.X = -10
        elif self.X > 780:
            self.X = 780
        if self.Y < -10:
            self.Y = -10
        elif self.Y > 580:
            self.Y = 580

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
            "," + str(self.last_frame) + "," + str(self.frame_width) + \
            "," + str(self.frame_height) + "," + str(self.columns) + \
            "," + str(self.rect)

# Point class


class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self): return self.__x

    def setx(self, x): self.__x = x
    x = property(getx, setx)

    # Y property
    def gety(self): return self.__y

    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"


class CharacterTypeData():

    def __init__(self, ID, Name, ImageName, InitHP, InitAttack,  BonusHP, BonusAttack):
        self.ID = ID
        self.name = Name
        self.imageName = ImageName
        self.initHP = InitHP
        self.initAttack = InitAttack
        self.bonusHP = BonusHP
        self.bonusAttack = BonusAttack


class GameRecordData():

    def __init__(self, ID, CharacterTypeID, CharacterName, CurrentHP, Experience,  CurrentMapID, CurrentX, CurrentY, CurrentDirection):
        self.ID = ID
        self.characterTypeID = CharacterTypeID
        self.characterName = CharacterName
        self.currentHP = CurrentHP
        self.experience = Experience
        self.currentMapID = CurrentMapID
        self.currentX = CurrentX
        self.currentY = CurrentY
        self.currentDirection = CurrentDirection

    def getChracterType(self):
        return sqliteHelper.getCharacterTypedByID(self.characterTypeID)

    def getlevel(self):
        sum = 0
        fac = [0, 1]
        level = 0
        level += 1
        sum += 1
        while self.experience >= sum:
            level += 1
            max = len(fac)
            fac.append(fac[max - 1] + fac[max - 2])
            sum += fac[max]
        return level


class GameData():
    # 為了選角用
    def __init__(self, CurrentX, CurrentY, CurrentDirection):
        self.currentX = CurrentX
        self.currentY = CurrentY
        self.currentDirection = CurrentDirection


class MonsterData():

    def __init__(self, ID, Name, ImageName, HP, Attack, ImageStartX, ImageStartY):
        self.ID = ID
        self.name = Name
        self.imageName = ImageName
        self.HP = HP
        self.attack = Attack
        self.imageStartX = ImageStartX
        self.imageStartY = ImageStartY


class MonsterRecordData():

    def __init__(self, ID, GameRecordID, MosterID, CurrentHP, CurrentX, CurrentY):
        self.ID = ID
        self.gameRecordID = GameRecordID
        self.imageName = MosterID
        self.currentHP = CurrentHP
        self.currentX = CurrentX
        self.currentY = CurrentY


class TextData():
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color

    def getTextSize(self):
        return len(self.text)

class HintData():
    def __init__(self, text):
        self.text = text
        self.color = color
        self.time = 0

    def setText(self, text,time):
        self.text = text
        self.time = time

    def getTextSize(self):
        return len(self.text)


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
