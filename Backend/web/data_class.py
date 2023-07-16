from pydantic import BaseModel

class RecommendedGame(BaseModel):
    games: list
    urls: list