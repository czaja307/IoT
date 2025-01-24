from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from routers import product, tag, purchase, terminal

router = APIRouter()


@router.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


router.include_router(product.router, prefix="/products", tags=["products"])
router.include_router(tag.router, prefix="/tags", tags=["tags"])
router.include_router(purchase.router, prefix="/purchases", tags=["purchases"])
router.include_router(terminal.router, prefix="/terminals", tags=["terminals"])
