from fastapi import APIRouter

from api.routes import predictor, model_cb, openapi, model_cf, model_hb, popular

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(model_cb.router, tags=["predictor"], prefix="/cb_model")
router.include_router(model_cf.router, tags=["predictor"], prefix="/cf_model")
router.include_router(openapi.router, tags=["predictor"], prefix="/gpt")
router.include_router(model_hb.router, tags=["predictor"], prefix="/hb_model")
router.include_router(popular.router, tags=["predictor"], prefix="/popular")