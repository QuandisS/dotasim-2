import sqlite3
import itertools

bd = sqlite3.connect('../data/data.db')
cursor = bd.cursor()


def init():
    global cursor, bd
    bd = sqlite3.connect('../data/data.db')
    cursor = bd.cursor()


def commit():
    global bd
    bd.commit()

def get_teams_list():
    cursor.execute("SELECT Name FROM Teams")
    teams = list(itertools.chain(*cursor.fetchall()))
    return teams

def get_heroes_list():
    cursor.execute("SELECT Name FROM Heroes")
    heroes = list(itertools.chain(*cursor.fetchall()))
    return heroes


def get_heroes_of_position(position):
    cursor.execute("SELECT Name FROM Heroes WHERE Positions LIKE ?", ('%' + position + '%',))
    return list(itertools.chain(*cursor.fetchall()))


def add_player(team, nick, country, fight, farm, teamwork, signatures, position):
    cursor.execute("SELECT Id FROM Teams WHERE Name=:name", {"name": team})
    team_id = cursor.fetchone()[0]

    to_players = (nick, country, team_id, position)
    cursor.execute("""INSERT INTO Players(Nickname, Country, TeamId, Position)
                      VALUES(?, ?, ?, ?)""", to_players)

    cursor.execute("SELECT Id FROM Players WHERE Nickname=:nick", {"nick": nick})
    player_id = cursor.fetchone()[0]

    to_player_stat = (fight, farm, teamwork, signatures, team_id, player_id)
    cursor.execute("""INSERT INTO PlayerStats(Fight, Farm, Teamwork, Signatures, TeamId, PlayerId)
                      VALUES(?, ?, ?, ?, ?, ?)""", to_player_stat)

    commit()


def add_coach(team, nick, country, skill, morale, communication):
    cursor.execute("SELECT Id FROM Teams WHERE Name=:name", {"name": team})
    team_id = cursor.fetchone()[0]

    to_coaches = (nick, country, team_id)
    cursor.execute("""INSERT INTO Coaches(Nickname, Country, TeamId)
                      VALUES(?, ?, ?)""", to_coaches)

    cursor.execute("SELECT Id FROM Coaches WHERE Nickname=:name", {"name": nick})
    coach_id = cursor.fetchone()[0]

    to_coach_stats = (skill, morale, communication, team_id, coach_id)
    cursor.execute("""INSERT INTO CoachStats(Skill, Morale, Communication, TeamId, CoachId)
                      VALUES(?, ?, ?, ?, ?)""", to_coach_stats)

    commit()


def add_team(name, country):
    to_teams = (name, country)
    cursor.execute("""INSERT INTO Teams(Name, Country)
                      VALUES(?, ?)""", to_teams)

    commit()


def create_hero(name, positions, fight_k, farm_k, teamwork_k):
    to_heroes = (name, positions)
    cursor.execute("""INSERT INTO Heroes(Name, Positions)
                      VALUES(?, ?)""", to_heroes)

    cursor.execute("""SELECT Id FROM Heroes WHERE Name=:name""", {"name": name})
    hero_id = cursor.fetchone()[0]

    to_hero_stats = (hero_id, fight_k, farm_k, teamwork_k)
    cursor.execute("""INSERT INTO HeroStats(HeroId, FightK, FarmK, TeamworkK)
                      VALUES(?, ?, ?, ?)""", to_hero_stats)

    commit()


def end_connection():
    cursor.close()
    bd.close()
