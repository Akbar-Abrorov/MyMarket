from fastapi import APIRouter, Depends, HTTPException
from app.auth.service import verify_admin_token
from app.schemas import ProductCreate, ProductUpdate
from app.admin.product import crud

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

@router.get("/", dependencies=[Depends(verify_admin_token)])
async def list_products():
    return await crud.get_all_products()

@router.get("/{product_id}", dependencies=[Depends(verify_admin_token)])
async def get_product(product_id: int):
    product = await crud.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", dependencies=[Depends(verify_admin_token)])
async def create_product(data: ProductCreate):
    return await crud.create_product(data)

@router.put("/{product_id}", dependencies=[Depends(verify_admin_token)])
async def update_product(product_id: int, data: ProductUpdate):
    product = await crud.update_product(product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", dependencies=[Depends(verify_admin_token)])
async def delete_product(product_id: int):
    result = await crud.delete_product(product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}