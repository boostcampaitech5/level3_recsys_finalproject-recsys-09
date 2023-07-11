from fastapi import APIRouter

from api.routes import predictor, model_rec, openapi

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(model_rec.router, tags=["reommender"], prefix="/model")
router.include_router(openapi.router, tags=["openapi"], prefix="/gpt")