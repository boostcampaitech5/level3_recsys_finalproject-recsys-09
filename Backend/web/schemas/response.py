from fastapi import Request
from pydantic import BaseModel
import os

class BaseResponse(BaseModel):
    request: Request
    ip: str = os.environ['HOST']
    port: str = os.environ['PORT']
    
    class Config:
        arbitrary_types_allowed = True
        

class InputResponse(BaseResponse):
    game_list: list
    

class OutputResponse(BaseResponse):
    games: dict