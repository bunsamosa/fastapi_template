import os

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from jose import jwt


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")


class JWTBearer(HTTPBearer):
    """
    Handle JWT token authentication
    """

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Call to authenticate and get user details
        """
        credentials: HTTPAuthorizationCredentials | None = (
            await super().__call__(request)
        )

        # Validate credentials
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid credentials.")

        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme.",
            )

        try:
            user_metadata = jwt.decode(
                token=credentials.credentials,
                key=JWT_SECRET,
                algorithms=JWT_ALGORITHM,
                audience=JWT_AUDIENCE,
            )
        except Exception as exc:
            await request.app.logger.error(
                "JWT decode error",
                exc_info=exc,
            )
            user_metadata = {}

        if not user_metadata:
            raise HTTPException(status_code=401, detail="Invalid credentials.")

        return user_metadata


# Initialize auth handler
handler = Depends(JWTBearer())
