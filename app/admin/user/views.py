from fastapi import APIRouter, Depends, HTTPException
from app.auth.service import verify_admin_token
from app.schemas import UserCreate, UserUpdate, UserOut
from app.admin.user import crud

router = APIRouter(prefix="/admin/users", tags=["Admin Users"])

@router.get("/", response_model=list[UserOut], dependencies=[Depends(verify_admin_token)])
async def list_users():
    return await crud.get_users()

@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(verify_admin_token)])
async def get_user(user_id: int):
    user = await crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserOut, dependencies=[Depends(verify_admin_token)])
async def create_user(user_data: UserCreate):
    existing_users = await crud.get_users()
    if any(u['username'] == user_data.username for u in existing_users):
        raise HTTPException(status_code=400, detail="Username already exists")
    return await crud.create_user(user_data)

@router.put("/{user_id}", response_model=UserOut, dependencies=[Depends(verify_admin_token)])
async def update_user(user_id: int, user_data: UserUpdate):
    user = await crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.username:
        all_users = await crud.get_users()
        for u in all_users:
            if u["username"] == user_data.username and u["id"] != user_id:
                raise HTTPException(status_code=400, detail="Username already exists")

    return await crud.update_user(user_id, user_data)

@router.delete("/{user_id}", dependencies=[Depends(verify_admin_token)])
async def remove_user(user_id: int):
    result = await crud.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully", "deleted_user_id": user_id}
