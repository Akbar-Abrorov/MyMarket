from fastapi import APIRouter, Depends, HTTPException
from app.auth.service import verify_admin_token
from app.schemas import CategoryCreate, CategoryUpdate
from app.admin.category import crud

router = APIRouter(prefix="/admin/categories", tags=["Admin Categories"])

@router.get("/", dependencies=[Depends(verify_admin_token)])
async def list_categories():
    return await crud.get_all_categories()

@router.get("/{category_id}", dependencies=[Depends(verify_admin_token)])
async def get_category(category_id: int):
    category = await crud.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", dependencies=[Depends(verify_admin_token)])
async def create_category(data: CategoryCreate):
    return await crud.create_category(data)

@router.put("/{category_id}", dependencies=[Depends(verify_admin_token)])
async def update_category(category_id: int, data: CategoryUpdate):
    category = await crud.update_category(category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", dependencies=[Depends(verify_admin_token)])
async def delete_category(category_id: int):
    result = await crud.delete_category(category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}