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

def getGameRecordByID(ID):
    Connect()
    sql = "SELECT * FROM `GameRecord` WHERE ID  = %d" % (ID) 
    cursor.execute(sql)
    fetch = cursor.fetchall()
    for data in fetch:
        result = GameRecordData(
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
    cursor.close()
    conn.close()
    return result

def getMonsterRecordByGameRecordID(gameRecordID):
    Connect()
    sql = "SELECT * FROM `GameRecord` WHERE GameRecordID  = %d" % (gameRecordID) 
    cursor.execute(sql)
    results = []
    fetch = cursor.fetchall()
    for data in fetch:
        results.append(GameRecordData(
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