from enum import Enum

class Player:
    def __init__(self, name: str, position: str, fight: int, farm: int, teamwork: int):
        self.name = name
        self.position = position
        self.fight = fight
        self.farm = farm
        self.teamwork = teamwork
        self.kills = 0
        self.assists = 0
        self.deaths = 0
        self.gold = 0