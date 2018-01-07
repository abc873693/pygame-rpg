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
        self.load(fileNmae, 42, 37, 4)
        self.position = (gameRecord.currentX, gameRecord.currentY)
        #self.direction = gameRecord.currentDirection

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

    def __init__(self,monsterData):
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
        fileNmae = 'images/monster/%s'  % (monsterData.imageName)
        self.load(fileNmae, 32, 32, 4)
        self.position = (monsterData.imageStartX, monsterData.imageStartY)
        self.direction = 1 #direction

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
    
    def getTextSize():
        return len(self.text)