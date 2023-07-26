from uuid import uuid4

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from auth.db import DATABASE
from auth.dependencies import validate_access_token, validate_refresh_token
from auth.schemas import UserOut, UserAuth, TokenSchema
from auth.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

router = APIRouter()


@router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    user = DATABASE.get(data.email, None)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    DATABASE[data.email] = user
    return user


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = DATABASE.get(form_data.username, None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(user['email'])
    refresh_token = create_refresh_token(user['email'])
    response_model = TokenSchema(access_token=access_token, refresh_token=refresh_token)
    return response_model


@router.post("/refresh_token/", response_model=TokenSchema)
async def refresh_token(payload=Depends(validate_refresh_token)):
    new_access_token = create_refresh_token(payload.get('sub'))
    return {"access_token": new_access_token, "refresh_token": refresh_token}


@router.get("/protected_route/")
async def protected_route(payload=Depends(validate_access_token)):
    user_identity = payload.get("sub")
    return {"message": f"Hello, {user_identity}! This is a protected route."}
