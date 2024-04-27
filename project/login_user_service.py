import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    The response model for a successful login attempt, primarily including the session token.
    """

    session_token: str
    message: str


async def login_user(email: str, password: str) -> UserLoginResponse:
    """
    Authenticate a user, returning a session token.

    This function checks if the provided email and password match an existing user.
    If successful, it generates a session token for the user.

    Args:
        email (str): The user's email address used for logging in.
        password (str): The user's password associated with their account.

    Returns:
        UserLoginResponse: The response model for a successful login attempt, primarily including the session token.

    Example:
        response = await login_user('user@example.com', 'password123')
        print(response)
        > UserLoginResponse(session_token="generated_token", message="Login successful")
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        session_token = "example_generated_session_token_for_demo"
        return UserLoginResponse(
            session_token=session_token, message="Login successful"
        )
    else:
        return UserLoginResponse(session_token="", message="Invalid login credentials")
