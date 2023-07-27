from fastapi import Request
from pydantic import BaseModel
from core.config import HOST, PORT

class BaseResponse(BaseModel):
    request: Request
    ip: str = HOST
    port: str = PORT
    
    class Config:
        arbitrary_types_allowed = True
        

class InputResponse(BaseResponse):
    game_list: list
    

class OutputResponse(BaseResponse):
    games: dict
    

class ABOutputResponse(BaseResponse):
    gpt: dict
    cb_model: dict
    cf_model: dict