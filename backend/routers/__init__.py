from fastapi import APIRouter

from routers import product, tag, purchase, terminal

router = APIRouter()
router.include_router(product.router, prefix="/products", tags=["products"])
router.include_router(tag.router, prefix="/tags", tags=["tags"])
router.include_router(purchase.router, prefix="/purchases", tags=["purchases"])
router.include_router(terminal.router, prefix="/terminals", tags=["terminals"])
