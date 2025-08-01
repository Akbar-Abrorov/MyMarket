from fastapi import APIRouter, HTTPException
from app.schemas import Product
from app import crud

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_all_products():
    return await crud.get_all_products()

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    product = await crud.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
