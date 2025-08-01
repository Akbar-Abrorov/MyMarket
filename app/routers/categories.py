from fastapi import APIRouter, HTTPException
from app.schemas import Category
from app import crud

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[Category])
async def get_all_categories():
    return await crud.get_all_categories()

@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int):
    category = await crud.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
