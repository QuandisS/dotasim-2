from enum import Enum
from hero_pool import Hero

class Player:
    def __init__(self, name: str, position: str, fight: int, farm: int, teamwork: int, signatures: str):
        self.name = name
        self.position = position
        self.fight = fight
        self.farm = farm
        self.teamwork = teamwork
        self.signatures: list[str] = signatures.split(sep=',')
        self.kills = 0
        self.assists = 0
        self.deaths = 0
        self.gold = 0
        self.is_using_signature = False
        self.hero = None

    def assign_hero(self, hero: Hero):
        self.hero = hero
        self.is_using_signature = hero.name in self.signatures