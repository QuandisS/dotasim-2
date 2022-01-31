import db
import random as r
from colorama import *


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

def start_quick_match():
    

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


if __name__ == '__main__':
    main()
