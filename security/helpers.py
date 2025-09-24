import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)

from jose import jwt
from jose.exceptions import ExpiredSignatureError

from .schema import TokenData

from passlib.context import CryptContext

from pydantic import ValidationError
from typing import Annotated

from models.users import Patient, Doctor, Nurse, Admin, Pharmacist

from dotenv import load_dotenv

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        "me": "Read information about the current user.",
        "admin": "Admin privileges",
        "get-patient": "Get patient information",
        "get-patients": "Get all patients information",
        "get-doctor": "Get doctor information",
        "get-appointment": "Get appointment information",
    },
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that `plain_password` and `hashed_password` are equal"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Returns a hash of the `password`"""
    return pwd_context.hash(password)


async def get_user(username: str) -> Patient | Doctor | Nurse | Admin | Pharmacist | None:

    user_in_db = await Doctor.find_one(Doctor.contact_info.email == username)

    if user_in_db is None:
        user_in_db = await Patient.find_one(Patient.contact_info.email == username)

    if user_in_db is None:
        user_in_db = await Admin.find_one(Admin.contact_info.email == username)

    if user_in_db is None:
        user_in_db = await Nurse.find_one(Nurse.contact_info.email == username)

    if user_in_db is None:
        user_in_db = await Pharmacist.find_one(Pharmacist.contact_info.email == username)


    return user_in_db


async def authenticate_user(username: str, password: str):
    user = await get_user(username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes: list = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (ValidationError):
        raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": authenticate_value},
        )
    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return await user


async def get_current_active_user(
    current_user: Annotated[
        Patient | Doctor | Nurse | Admin | Pharmacist, Security(get_current_user, scopes=["me"])
    ],
):
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is inactive"
        )
    return current_user