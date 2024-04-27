from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    Response model indicating the result of the user registration attempt. It will return a success status and either a user ID for successful registrations or error details for failures.
    """

    success: bool
    user_id: Optional[str] = None
    error_message: Optional[str] = None


async def register_user(email: str, password: str) -> RegisterUserResponse:
    """
    Register a new user with an email and password.

    Args:
    email (str): The email address of the new user. This will be used as their login identifier and must be unique across the user base.
    password (str): The password for the new user. This password will be hashed before being stored in the database to ensure security.

    Returns:
    RegisterUserResponse: Response model indicating the result of the user registration attempt. It will return a success status and either a user ID for successful registrations or error details for failures.
    """
    try:
        existing_user = await prisma.models.User.prisma().find_unique(
            where={"email": email}
        )
        if existing_user:
            return RegisterUserResponse(
                success=False, error_message="Email already in use."
            )
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = await prisma.models.User.prisma().create(
            data={"email": email, "password": hashed_password.decode("utf-8")}
        )
        return RegisterUserResponse(success=True, user_id=user.id)
    except Exception as e:
        return RegisterUserResponse(success=False, error_message=str(e))
