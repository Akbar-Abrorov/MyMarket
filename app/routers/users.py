from fastapi import APIRouter, HTTPException
from app.schemas import User, UserCreate, UserUpdate, UserOut
from app import crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
async def get_all_users():
    try:
        users = await crud.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting users: {str(e)}")


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    try:
        user = await crud.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user: {str(e)}")


@router.post("/", response_model=UserOut)
async def create_user(user_data: UserCreate):
    try:
        existing_users = await crud.get_all_users()
        for existing_user in existing_users:
            if existing_user["username"] == user_data.username:
                raise HTTPException(status_code=400, detail="Username already exists")

        new_user = await crud.create_user(user_data)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: UserUpdate):
    try:
        existing_user = await crud.get_user_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")



        if user_data.username:
            all_users = await crud.get_all_users()
            for user in all_users:
                if user["username"] == user_data.username and user["id"] != user_id:
                    raise HTTPException(status_code=400, detail="Username already exists")

        updated_user = await crud.update_user(user_id, user_data)
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")


@router.delete("/{user_id}")
async def delete_user(user_id: int):

    try:
        existing_user = await crud.get_user_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        result = await crud.delete_user(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully", "deleted_user_id": user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
