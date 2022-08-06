import random as r

class Hero:
    def __init__(self, name: str, fight: int, farm: int, teamwork: int, positions: str):
        self.name = name
        self.fight = fight
        self.farm = farm
        self.teamwork = teamwork
        self.positions: list[str] = positions.split(sep=',')

class HeroPool:
    def __init__(self):
        self.heroes: list[Hero] = []

    def append_hero(self, hero: Hero):
        self.heroes.append(hero)

    def pick_hero(self, position: str):
        available_heroes = list(filter(lambda hero: position in hero.positions, self.heroes))
        chosen = r.choice(available_heroes)
        self.heroes.remove(chosen)
        return chosen