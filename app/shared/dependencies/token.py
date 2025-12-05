from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer

from auth.infrastructure.repositories import TokenRepoImpl, TokenTypeFields

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login/")
http_bearer = HTTPBearer(auto_error=False)

def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    print(token)
    try:
        payload = TokenRepoImpl().decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return payload