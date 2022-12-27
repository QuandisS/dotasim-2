import time
import db
from colorama import *
from team import *
from hero_pool import *

app_ver = 'v1t0b0'


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
    return 1 + (param / 100)


def has_support(players: list[Player]) -> bool:
    for player in players:
        if player.position in ['Sup', 'Semi-Sup']:
            return True
    return False


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
        for h_id in team1_ids:
            team1.append_player(Player(*db.get_player_info(h_id)))

        team2_ids = db.get_player_ids(team2.name)
        for h_id in team2_ids:
            team2.append_player(Player(*db.get_player_info(h_id)))

        teams_score = [0, 0]
        match_results = []
        match_wins = [0, 0]
        teams = [team1, team2]

        for i in range(match_count):
            if match_wins[0] > (match_count / 2):
                break
            elif match_wins[1] > (match_count / 2):
                break
            print(Fore.CYAN + "=================" + Fore.RESET)
            print("Match", i, "started")

            base_hp = [100, 100]
            match_teams_score = [0, 0]

            hero_pool = HeroPool()
            hero_ids = db.get_hero_ids()
            for h_id in hero_ids:
                hero_pool.append_hero(Hero(*db.get_hero_info(h_id)))

            signatures_picked_count = [0, 0]
            for j in range(2):
                for player in teams[j].players:
                    player.assign_hero(hero_pool.pick_hero(player.position))
                    if player.is_using_signature:
                        signatures_picked_count[j] += 1

            for k in range(2):
                print("Pick: ", Fore.GREEN + teams[k].name + Fore.RESET, "signatures: ", signatures_picked_count[k])

            for team in teams:
                team.reset_gold()

            game_over = False
            clock = 0
            while not game_over:
                event = r.choices(['farm', 'fight'], weights=[0.83, 0.17], k=1)[0]
                if event == 'farm':
                    for team in teams:
                        for player in team.players:
                            player.gold += (int(r.randint(10, 200)
                                                * get_coefficient(player.farm)
                                                * player.hero.farm
                                                * (1.2 if player.is_using_signature else 1)))
                else:
                    print("==========")
                    print("Fight on", clock, "minute")
                    print("Networth: ", team1.name, Fore.LIGHTYELLOW_EX + str(team1.get_networth()) + Fore.RESET)
                    print("Networth: ", team2.name, Fore.LIGHTYELLOW_EX + str(team2.get_networth()) + Fore.RESET)

                    teams_fight_squad = [[], []]
                    for m in range(2):
                        for player in teams[m].players:
                            if (r.randint(10, 60)
                                * get_coefficient(player.teamwork)
                                * player.hero.teamwork
                                * get_coefficient(teams[m].communication)) > 50:
                                teams_fight_squad[m].append(player)

                    print(team1.name, "players: ", len(teams_fight_squad[0]))
                    print(team2.name, "players: ", len(teams_fight_squad[1]))

                    while len(teams_fight_squad[0]) != 0 and len(teams_fight_squad[1]) != 0:
                        team1_pick: Player = r.choice(teams_fight_squad[0])
                        team2_pick: Player = r.choice(teams_fight_squad[1])

                        team1_kill_score = r.randint(10, 100) \
                                           * get_coefficient(team1_pick.fight) \
                                           * team1_pick.hero.fight

                        team2_kill_score = r.randint(10, 100) \
                                           * get_coefficient(team2_pick.fight) \
                                           * team2_pick.hero.fight

                        # Signatures
                        if team1_pick.is_using_signature:
                            team1_kill_score += r.randint(1, 30)

                        if team2_pick.is_using_signature:
                            team2_kill_score += r.randint(1, 30)

                        # Gold
                        gold_dif = team1_pick.gold - team2_pick.gold
                        if gold_dif > 0:
                            team1_kill_score += gold_dif * 0.001
                        else:
                            team2_kill_score += abs(gold_dif) * 0.001

                        # Morale
                        hp_dif = base_hp[0] - base_hp[1]
                        if hp_dif > 0:
                            team2_kill_score += r.randint(1, 20) * get_coefficient(team2.morale) + hp_dif * 0.1
                        else:
                            team1_kill_score += r.randint(1, 20) * get_coefficient(team1.morale) + abs(hp_dif) * 0.1

                        # Sup
                        if has_support(teams_fight_squad[0]):
                            team1_kill_score += r.randint(1, 10) * get_coefficient(team1.communication)
                        if has_support(teams_fight_squad[1]):
                            team2_kill_score += r.randint(1, 10) * get_coefficient(team2.communication)

                        # Kill
                        if team1_kill_score > team2_kill_score:
                            match_teams_score[0] += 1
                            team1_pick.gold += r.randint(10, 500)
                            team1_pick.kills += 1
                            for player in teams_fight_squad[0]:
                                if player != team1_pick:
                                    player.assists += 1
                            team2_pick.deaths += 1
                            teams_fight_squad[1].remove(team2_pick)

                        elif team1_kill_score < team2_kill_score:
                            match_teams_score[1] += 1
                            team2_pick.gold += r.randint(10, 500)
                            team2_pick.kills += 1
                            for player in teams_fight_squad[1]:
                                if player != team2_pick:
                                    player.assists += 1
                            team1_pick.deaths += 1
                            teams_fight_squad[0].remove(team1_pick)

                    if len(teams_fight_squad[0]) == 0:
                        damage = int(r.randint(1, 30) * (1 + len(teams_fight_squad[1]) * 0.1))
                        base_hp[0] -= damage
                        print("Team ", team2.name, "won the fight with advantage of ",
                              str(len(teams_fight_squad[1]) - len(teams_fight_squad[0])))
                        print(team1.name, base_hp[0], Fore.LIGHTRED_EX + "-" + str(damage) + Fore.RESET)
                        print(team2.name, base_hp[1])
                    else:
                        damage = int(r.randint(1, 30) * (1 + len(teams_fight_squad[0]) * 0.1))
                        base_hp[1] -= damage
                        print("Team ", team1.name, "won the fight with advantage of ",
                              str(len(teams_fight_squad[0]) - len(teams_fight_squad[1])))
                        print(team1.name, base_hp[0])
                        print(team2.name, base_hp[1], Fore.LIGHTRED_EX + "-" + str(damage) + Fore.RESET)

                    print("==========")

                if base_hp[0] <= 0:
                    game_over = True
                    match_result = Fore.LIGHTBLUE_EX + team1.name + Fore.RESET + " lost. kills: " + str(
                        match_teams_score[0]) + "\n" + \
                                   Fore.LIGHTGREEN_EX + team2.name + Fore.RESET + " wins. kills: " + str(
                        match_teams_score[1]) + "\n" + \
                                   "Match length: " + str(clock) + " minutes" + "\n" + \
                                   "Networth: " + str(team1.get_networth() - team2.get_networth()) + "\n"
                    print(match_result)
                    print(Fore.CYAN + "==========" + Fore.RESET)
                    match_results.append(match_result)
                    teams_score[0] += match_teams_score[0]
                    teams_score[1] += match_teams_score[1]
                    match_wins[1] += 1
                    db.update_hero_stats(teams, 1)

                elif base_hp[1] <= 0:
                    game_over = True
                    match_result = Fore.LIGHTBLUE_EX + team1.name + Fore.RESET + " wins. kills: " + str(
                        match_teams_score[0]) + "\n" + \
                                   Fore.LIGHTGREEN_EX + team2.name + Fore.RESET + " lost. kills: " + str(
                        match_teams_score[1]) + "\n" + \
                                   "Match length: " + str(clock) + " minutes" + "\n" + \
                                   "Networth: " + str(team1.get_networth() - team2.get_networth()) + "\n"
                    print(match_result)
                    print(Fore.CYAN + "==========" + Fore.RESET)
                    match_results.append(match_result)
                    teams_score[0] += match_teams_score[0]
                    teams_score[1] += match_teams_score[1]
                    match_wins[0] += 1
                    db.update_hero_stats(teams, 0)

                clock += 1
                time.sleep(0.5)

        print(Fore.LIGHTRED_EX + "Game Ended")
        print("Matches info:")
        print("\n".join(match_results))
        print("Overall:")
        print(Fore.LIGHTBLUE_EX + '%-15s' % team1.name + Fore.RESET, ":", match_wins[0], "   kills: ", teams_score[0])
        print(Fore.LIGHTGREEN_EX + '%-15s' % team2.name + Fore.RESET, ":", match_wins[1], "   kills: ", teams_score[1])
        print("KDA:")

        for team in teams:
            print(team.name)
            for player in team.players:
                kda_stroke = '%-15s' % player.name
                kda_stroke += str(player.kills) + "/" + str(player.deaths) + "/" + str(player.assists)
                print(kda_stroke)
            print()

        all_players = []
        all_players.extend(team1.players)
        all_players.extend(team2.players)
        all_players.sort(key=lambda player: player.kills + player.assists, reverse=True)
        mvp: Player = all_players[0]
        print("MVP", Fore.LIGHTYELLOW_EX + mvp.name + Fore.RESET)

        db.update_stats(teams, match_wins)


def main():
    db.init()
    print("Welcome to DotaSim2 patch:", app_ver)
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
