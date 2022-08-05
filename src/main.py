import db
import random as r
from colorama import *
from team import *

def create_team():
    team_name = input("Team name: ")
    team_country = input("Team country (country code): ")
    nicknames = input("Nicknames (space between, coach last, [core, core, core, semi-sup, sup, coach]): ").split()
    players_countries = input("Countries (space between): ").split()

    if len(nicknames) != 6 or len(players_countries) != 6:
        print(Fore.RED + "[Wrong player or country number]" + Fore.RESET)
        return

    print("Adding team to database")
    db.add_team(team_name, team_country)
    print(Fore.GREEN + "[Team added successfully]" + Fore.RESET)

    print("Adding players to database")
    skill_sum = 0
    positions = ["Core", "Core", "Core", "Semi-Sup", "Sup"]
    for i in range(5):
        nick = nicknames[i]
        country = players_countries[i]
        position = positions[i]
        fight = r.randint(0, 100)
        farm = r.randint(0, 100)
        teamwork = r.randint(0, 100)
        skill_sum += fight + farm + teamwork
        heroes_of_position = db.get_heroes_of_position(position)
        signatures = ','.join(r.choices(heroes_of_position, k=3))

        db.add_player(team_name, nick, country, fight, farm, teamwork, signatures, position)

    # adding coach
    print("Adding coach to database")
    nick = nicknames[5]
    country = players_countries[5]
    skill = r.randint(0, 100)
    morale = r.randint(0, 100)
    communication = r.randint(0, 100)

    db.add_coach(team_name, nick, country, skill, morale, communication)

    print(Fore.GREEN + "[Players and Coach added successfully]" + Fore.RESET)


def create_hero():
    name = input("Hero name: ")
    print("[Write positions like this: Core, Semi-Sup, Sup]")
    positions = input("Positions: ")

    if positions == "Core":
        fight_k = r.uniform(1.3, 1.5)
    elif positions == "Core, Semi-Sup":
        fight_k = r.uniform(1.2, 1.4)
    elif positions == "Semi-Sup":
        fight_k = r.uniform(1.15, 1.2)
    elif positions == "Semi-Sup, Sup":
        fight_k = r.uniform(1.1, 1.15)
    elif positions == "Sup":
        fight_k = r.uniform(1, 1.1)
    else:
        print(Fore.RED + "[Wrong positions input]" + Fore.RESET)
        return

    farm_k = r.uniform(1, 1.5)
    teamwork_k = r.uniform(1, 1.5)

    print("Hero", name, "positions", positions)
    print("Fight", fight_k, "Farm", farm_k, "Teamwork", teamwork_k)

    print("Adding hero to database...")
    db.create_hero(name, positions, fight_k, farm_k, teamwork_k)
    print(Fore.GREEN + "[Successfully added]" + Fore.RESET)


def print_hero_list():
    print(db.get_heroes_list())


def print_hero_list_by_position(inp: str):
    if len(inp.split()) != 2:
        print(Fore.RED + "[Wrong argument count]" + Fore.RESET)
        return
    print(db.get_heroes_of_position(inp.split()[1]))


def print_team_list():
    print(db.get_teams_list())


def get_coefficient(param: int) -> float:
    return 1 + (param/100)


def start_quick_match():
    match_count = int(input("Match count: "))

    while True:
        team1_name = input("Team 1: ")
        team2_name = input("Team 2: ")

        if not db.check_team_names(team1_name, team2_name):
            print("invalid team name")
            continue

        team1 = Team(team1_name, *db.get_coach_stats(team1_name))
        team2 = Team(team2_name, *db.get_coach_stats(team2_name))

        team1_ids = db.get_player_ids(team1.name)
        for id in team1_ids:
           team1.append_player(Player(*db.get_player_info(id)))

        team2_ids = db.get_player_ids(team2.name)
        for id in team2_ids:
            team2.append_player(Player(*db.get_player_info(id)))

        for i in range(match_count):
            print("Match", i, "started")

            base_hp = [100, 100]
            teams_score = [0, 0]

            teams = [team1, team2]
            for team in teams:
                team.reset_gold()

            game_over = False
            clock = 0
            while not game_over:
                event = r.choices(['farm', 'fight'], weights=[0.83, 0.17], k=1)[0]
                if event == 'farm':
                    for team in teams:
                        for player in team.players:
                            player.gold += int(r.randint(10, 100) * get_coefficient(player.gold))
                clock += 1



def main():
    db.init()
    print("Welcome to DotaSim2 v0")
    while True:
        user_input = input(">> ")

        if user_input == "ch":
            create_hero()

        elif user_input == "ct":
            create_team()

        elif user_input == "hl":
            print_hero_list()

        elif user_input.split()[0] == 'hlp':
            print_hero_list_by_position(user_input)

        elif user_input == "tl":
            print_team_list()

        elif user_input == "q":
            db.end_connection()
            break

        elif user_input == "qm":
            start_quick_match()


if __name__ == '__main__':
    main()
