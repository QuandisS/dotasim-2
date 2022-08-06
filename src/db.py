import sqlite3
import itertools
from team import *

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


# Returns true if names is valid
def check_team_names(team1_name: str, team2_name: str) -> bool:
    cursor.execute("""SELECT name from Teams""")
    teams = list(itertools.chain(*cursor.fetchall()))
    if team1_name not in teams or team2_name not in teams:
        return False

    return True


def get_coach_stats(team_name: str) -> list[int]:
    t_name = []
    t_name.append(team_name)
    cursor.execute("""select Morale, Communication
                      from Teams t, CoachStats cs
                      where 
	                  t.Name = ? AND 
	                  cs.TeamId = t.Id""", t_name)
    return list(itertools.chain(*cursor.fetchall()))


def get_player_ids(team_name: str) -> list[int]:
    t_name = []
    t_name.append(team_name)
    cursor.execute("""select p.Id 
                      from Players p, Teams t 
                      where 
	                      t.name = ? AND 
	                      p.TeamId = t.Id """, t_name)
    return list(itertools.chain(*cursor.fetchall()))


def get_player_info(id: int) -> list[str, str, int, int, int, str]:
    p_id = []
    p_id.append(id)
    cursor.execute("""SELECT p.Nickname, p."Position", ps.Fight, ps.Farm, ps.Teamwork, ps.Signatures
                      from Players p, PlayerStats ps
                      WHERE
	                        p.Id = ? AND 
	                        p.Id = ps.PlayerId """, p_id)
    return list(itertools.chain(*cursor.fetchall()))


def get_hero_ids() -> list[int]:
    cursor.execute("""select h.Id
                      from Heroes h""")
    return list(itertools.chain(*cursor.fetchall()))


def get_hero_info(id: int) -> list[str, int, int, int, str]:
    h_id = []
    h_id.append(id)
    cursor.execute("""select h.Name, hs.FightK, hs.FarmK, hs.TeamworkK, h.Positions
                      from Heroes h, HeroStats hs
                      WHERE 
	                      h.Id = ? AND 
	                      hs.HeroId = h.Id """, h_id)
    return list(itertools.chain(*cursor.fetchall()))


def update_coach_stats(team: Team, wins: int, loses: int):
    t_name = []
    t_name.append(team.name)
    cursor.execute("""SELECT cs.Id 
                      from Teams t, CoachStats cs 
                      where 
	                  t.Id = cs.TeamId AND
	                  t.name = ?""", t_name)
    coach_stat_id = cursor.fetchone()[0]
    to_coach_stats = (wins, loses, coach_stat_id)
    cursor.execute("""UPDATE CoachStats 
                      set Wins = Wins + ?,
                      Loses = Loses + ?
                      WHERE Id = ?""", to_coach_stats)
    commit()


def update_player_stats(player: Player, wins_n: int, loses_n: int):
    player_name = []
    player_name.append(player.name)
    cursor.execute("""SELECT p.Id 
                     from Players p 
                     WHERE p.Nickname = ?""", player_name)
    player_id = cursor.fetchone()[0]

    to_stats = (wins_n, loses_n, player.kills, player.deaths, player.assists, player_id)
    cursor.execute("""update PlayerStats 
                      set Wins = Wins + ?,
                        Loses = Loses + ?,
                        Kills = Kills + ?,
                        Deaths = Deaths + ?,
                        Assists = Assists + ?
                      WHERE 
                        PlayerId = ?""", to_stats)
    commit()

def update_stats(teams: list[Team], wins: list[int]) -> None:
    for i in range(2):
        wins_n = wins[i]
        loses_n = wins[1 if i==0 else 0]
        update_coach_stats(teams[i], wins_n, loses_n)
        for player in teams[i].players:
            update_player_stats(player, wins_n, loses_n)


def update_hero_stats(teams: list[Team], won_team_id: int):
    for i in range(2):
        win = 1 if won_team_id == i else 0
        loss = 1 if won_team_id != i else 0
        for player in teams[i].players:
            h_name = []
            h_name.append(player.hero.name)
            cursor.execute("""select h.Id 
                              from Heroes h 
                              WHERE h.Name = ?""", h_name)
            h_id = cursor.fetchone()[0]
            to_hero_stats = (win, loss, h_id)
            cursor.execute("""update HeroStats 
                              set Wins = Wins + ?,
                                  Loses = Loses + ?
                              where HeroId = ?""", to_hero_stats)
    commit()