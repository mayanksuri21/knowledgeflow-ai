import jwt
import requests
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import get_settings
from .logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

security = HTTPBearer()


class ClerkAuth:
    def __init__(self):
        self.jwks_url = f"{settings.CLERK_JWT_ISSUER}/.well-known/jwks.json" if settings.CLERK_JWT_ISSUER else None
        self._jwks: Optional[Dict[str, Any]] = None

    def _get_jwks(self) -> Dict[str, Any]:
        if not self._jwks:
            if not self.jwks_url:
                raise ValueError("CLERK_JWT_ISSUER is not set")
            response = requests.get(self.jwks_url)
            response.raise_for_status()
            self._jwks = response.json()
        return self._jwks

    def _get_public_key(self, kid: str) -> Any:
        jwks = self._get_jwks()
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return jwt.algorithms.RSAAlgorithm.from_jwk(key)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token key"
        )

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")
            if not kid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token header"
                )
            public_key = self._get_public_key(kid)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=settings.CLERK_JWT_ISSUER,
                options={"verify_aud": False}
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )


clerk_auth = ClerkAuth()
