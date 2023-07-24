from fastapi import Form
from pydantic import BaseModel, validator
from typing import Optional
from core.output_process import search_games

class UserRequest(BaseModel):
    age: str
    platform: list
    players: str
    major_genre: list
    tag: list
    games: list

    @classmethod
    def as_form(
        cls,
        age: str = Form(...),
        young: Optional[str] = Form(None),
        platform: list  = Form(...),
        players: str = Form(...),
        genre: list = Form(...),
        tag: list = Form(...),
        search: list = Form(...)
    ):
        if young:
            age = young
        
        return cls(age=age, platform=platform, players=players, major_genre=genre, tag=tag, games=search)
    
    @validator('tag')
    def process_all_tag(cls, tag):
        if tag == ['all']:
           return []
        return tag
    

class FeedbackRequest(BaseModel):
    gptlike: list
    cblike: list
    cflike: list
    
    @classmethod
    def as_form(
        cls,
        gptlike: list = Form(...),
        cblike: list = Form(...),
        cflike: list = Form(...)
    ):
        return cls(gptlike=gptlike, cblike=cblike, cflike=cflike)


class CBRequest(BaseModel):
    age: str
    platform: list
    players: str
    major_genre: list
    tag: list
    games: list
    
    @validator('games')
    def process_game_iput(cls, games):
        return search_games(games)
        
    
class GPTRequest(BaseModel):
    age: str
    platform: list
    players: str
    games: list