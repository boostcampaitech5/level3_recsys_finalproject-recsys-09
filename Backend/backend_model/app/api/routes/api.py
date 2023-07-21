from fastapi import APIRouter

from api.routes import predictor, model_cb, openapi, model_cf

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(model_cb.router, tags=["predictor"], prefix="/cb_model")
router.include_router(model_cf.router, tags=["predictor"], prefix="/cf_model")
router.include_router(openapi.router, tags=["predictor"], prefix="/gpt")
