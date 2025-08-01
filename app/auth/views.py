from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from datetime import timedelta
from app.auth import service, model
from app.auth.service import create_access_token, verify_admin_token, update_admin_credentials


router = APIRouter(prefix="/admin/auth", tags=["Admin Auth"])


@router.post("/login", response_model=model.AdminTokenResponse)
def login(data: model.AdminLoginRequest):
    if (
        data.username != service.ADMIN_CREDENTIALS["username"]
        or data.password != service.ADMIN_CREDENTIALS["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=service.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": data.username, "role": "admin"},
        expires_delta=access_token_expires,
    )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register_admin(data: model.AdminRegisterRequest):
    update_admin_credentials(data.username, data.password)
    return {"message": f"Admin registered with username '{data.username}'"}


@router.post("/logout")
def logout_admin(response: Response, request: Request, token_payload: dict = Depends(verify_admin_token)):
    response.delete_cookie("Authorization")
    return {"message": f"Admin '{token_payload['sub']}' logged out successfully"}


@router.post("/renew", response_model=model.AdminTokenResponse)
def renew_token(token_payload: dict = Depends(verify_admin_token)):
    new_token = create_access_token({"sub": token_payload["sub"], "role": token_payload["role"]})
    return {"access_token": new_token, "token_type": "bearer"}