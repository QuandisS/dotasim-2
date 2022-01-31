import sqlite3

bd = sqlite3.connect('../data/data.db')
cursor = bd.cursor()


def init():
    global cursor, bd
    bd = sqlite3.connect('../data/data.db')
    cursor = bd.cursor()


def commit():
    global bd
    bd.commit()


def create_hero(name, positions, fight_k, farm_k, teamwork_k):
    init()

    to_heroes = (name, positions)
    cursor.execute("""INSERT INTO Heroes(Name, Positions)
                      VALUES(?, ?)""", to_heroes)

    cursor.execute("""SELECT Id FROM Heroes WHERE Name='""" + name + """'""")
    hero_id = cursor.fetchone()[0]

    to_hero_stats = (hero_id, fight_k, farm_k, teamwork_k)
    cursor.execute("""INSERT INTO HeroStats(HeroId, FightK, FarmK, TeamworkK)
                      VALUES(?, ?, ?, ?)""", to_hero_stats)

    commit()


cursor.close()
bd.close()
