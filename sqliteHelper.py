import sqlite3
from models import *

#==================================METHODS============================================


def Connect():
    global conn, cursor
    conn = sqlite3.connect('pythontut.db')
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `rank` (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, time INTEGER)")

def getAllCharacterType(self):
    Connect()
    cursor.execute("SELECT * FROM `CharacterType`")
    results = []
    fetch = cursor.fetchall()
    for data in fetch:
        results.append(CharacterTypeData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    return results


def getCharacterTypedByID(ID):
    Connect()
    sql = "SELECT * FROM `CharacterType` WHERE ID  = %d" % (ID) 
    cursor.execute(sql)
    fetch = cursor.fetchall()
    for data in fetch:
        result = CharacterTypeData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6])
    cursor.close()
    conn.close()
    return result


def getAllGameRecord():
    Connect()
    cursor.execute("SELECT * FROM `GameRecord`")
    results = []
    fetch = cursor.fetchall()
    for data in fetch:
        results.append(GameRecordData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
    cursor.close()
    conn.close()
    return results


def getRankGameRecord():
    Connect()
    cursor.execute("SELECT * FROM `GameRecord` ORDER BY `Experience` DESC")
    results = []
    fetch = cursor.fetchall()
    for data in fetch:
        results.append(GameRecordData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
    cursor.close()
    conn.close()
    return results


def getGameRecordByID(ID):
    Connect()
    sql = "SELECT * FROM `GameRecord` WHERE ID = %d" % (ID) 
    cursor.execute(sql)
    fetch = cursor.fetchall()
    for data in fetch:
        result = GameRecordData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
    cursor.close()
    conn.close()
    return result


def insertGameRecord(characterTypeID, characterName):
    conn = sqlite3.connect('pythontut.db')
    cursor = conn.cursor()
    characterType = getCharacterTypedByID(characterTypeID)
    sql = "INSERT INTO `GameRecord` (CharacterTypeID ,CharacterName ,CurrentHP ,Experience ,CurrentMapID ,CurrentX ,CurrentY ,CurrentDirection) VALUES(%d, '%s', %d, %d, %d, %d, %d, %d)" % (
        characterTypeID, characterName, characterType.initHP + characterType.bonusHP , 0, 0, 100, 100, 0)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

def updateGameRecord(gameRecordID, player):
    conn = sqlite3.connect('pythontut.db')
    cursor = conn.cursor()
    characterType = getCharacterTypedByID(characterTypeID)
    sql = "UPDATE `GameRecord` SET CurrentHP = %d ,Experience = %d ,CurrentX = %d ,CurrentY = %d ,CurrentDirection = %d WHERE ID = %d" % (
        player.gameRecordData.currentHP, player.getCurrentHP() , player.X , player.Y , player.direction, gameRecordID)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

def getMonsterRecordByGameRecordID(gameRecordID):
    Connect()
    sql = "SELECT * FROM `MonsterRecord` WHERE GameRecordID  = %d" % (
        gameRecordID)
    cursor.execute(sql)
    results = []
    fetch = cursor.fetchall()
    for data in fetch:
        results.append(GameRecordData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
    cursor.close()
    conn.close()
    return results

def deleteMonsterRecordByGameRecordID(gameRecordID):
    Connect()
    sql = "DELETE FROM `MonsterRecord` WHERE GameRecordID  = %d" % (
        gameRecordID)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def insertMonsterRecord(gameRecordID, monstergroup):
    conn = sqlite3.connect('pythontut.db')
    cursor = conn.cursor()
    for monsterSprite in monstergroup:
        sql = "INSERT INTO `MonsterRecord` (GameRecordID ,MosterID ,CurrentHP ,CurrentX ,CurrentY) VALUES(%d, '%d', %d, %d, %d)" % (
            gameRecordID, monsterSprite.monsterData.ID, monsterSprite.currentHP, monsterSprite.X, monsterSprite.Y)
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

def getAllMonster():
    Connect()
    cursor.execute("SELECT * FROM `Monster`")
    results = []
    fetch = cursor.fetchall()
    for data in fetch:
        results.append(MonsterData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    return resultspend(GameRecordData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
    cursor.close()
    conn.close()
    return results


def getAllMonster():
    Connect()
    cursor.execute("SELECT * FROM `Monster`")
    results = []
    fetch = cursor.fetchall()
    for data in fetch:
        results.append(MonsterData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    return results
