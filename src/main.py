import db
import random as r
from colorama import *


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


def main():
    print("Welcome to DotaSim2 v0")
    while True:
        user_input = input(">> ")

        if user_input == "ch":
            create_hero()

if __name__ == '__main__':
    main()
