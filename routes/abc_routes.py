from __future__ import annotations

from fastapi import APIRouter, HTTPException

from models.abc_models import User, UserCreate
from services.abc_services import UserService

router = APIRouter()
user_service = UserService()

USER_NOT_FOUND = "User not found"


@router.get("/users", response_model=list[User])
async def get_users():
    """Get all users"""
    return await user_service.get_all_users()


@router.get("/users/{user_id}", response_model=User, responses={404: {"description": USER_NOT_FOUND}})
async def get_user(user_id: str):
    """Get a user by ID"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return user


@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    return await user_service.create_user(user)


@router.delete("/users/{user_id}", responses={404: {"description": USER_NOT_FOUND}})
async def delete_user(user_id: str):
    """Delete a user"""
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return {"message": "User deleted successfully"}


# Delete this file if you don't want to use it. Use *_routes.py pattern to create new route files.
