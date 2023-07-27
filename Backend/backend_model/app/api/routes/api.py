from fastapi import APIRouter

from api.routes import openapi, model_hb, popular

router = APIRouter()
router.include_router(openapi.router, tags=["predictor"], prefix="/gpt")
router.include_router(model_hb.router, tags=["predictor"], prefix="/hb_model")
router.include_router(popular.router, tags=["predictor"], prefix="/popular")