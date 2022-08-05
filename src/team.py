from player import Player

class Team:
    def __init__(self, name: str, morale: int, communication: int):
        self.name = name
        self.morale = morale
        self.communication = communication
        self.players: list[Player] = []

    def append_player(self, player: Player):
        self.players.append(player)

    def reset_gold(self):
        for player in self.players:
            player.gold = 0