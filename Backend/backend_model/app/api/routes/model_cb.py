import json

import joblib
from fastapi import APIRouter, HTTPException

from services.predict import ContentBaseModel
from models.prediction import (
    RecommendedGame,
    ModelInput
)

router = APIRouter()


## Change this portion for other types of models
## Add the correct type hinting when completed
def get_recommendations(data_point):
    cb_model = ContentBaseModel(data_point)
    return cb_model.predict()


@router.post(
    "/predict",
    response_model=RecommendedGame,
    name="predict:get-input",
)
async def model_recommend(data_input: ModelInput):

    if not data_input:
        raise HTTPException(status_code=404, detail="'data_input' argument invalid!")
    try:
        recommendations = get_recommendations(data_input)

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Exception: {err}")

    return RecommendedGame(games=recommendations)