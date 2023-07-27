import numpy as np

from pydantic import BaseModel

class RecommendedGame(BaseModel):
    games: list


class ModelInput(BaseModel):
    age: str
    platform: list
    players: str
    major_genre: list
    tag: list
    games: list

    def get_games(self):
        return self.games