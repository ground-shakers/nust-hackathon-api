import os
from datetime import timedelta

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from dotenv import load_dotenv

from security.helpers import authenticate_user, create_access_token

from security.schema import Token, LoginResponse

load_dotenv()


router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)

    if user:
        access_token_expires = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        access_token = create_access_token(
            data={"sub": user.contact_info.email, "scopes": user.permissions},
            expires_delta=access_token_expires,
        )

        return LoginResponse(
            message="Login successful",
            token=Token(
                access_token=access_token,
                token_type="bearer",
            ),
            user_id=str(user.id),
            role=user.role,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )