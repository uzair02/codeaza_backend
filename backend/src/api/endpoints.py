import fastapi

from src.api.routes.category import router as category_router

router = fastapi.APIRouter()
router.include_router(router=category_router)
