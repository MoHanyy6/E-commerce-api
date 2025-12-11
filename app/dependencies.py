from fastapi import Depends, HTTPException, status, Request

from sqlalchemy.orm import Session
from . import database, models, oauth

def require_role(*roles: str):
    """
    Dependency to check if the current user has one of the allowed roles.
    Usage: Depends(require_role("admin", "instructor"))
    """
    def role_checker(current_user: models.User = Depends(oauth.get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required privileges: {roles}"
            )
        return current_user
    return role_checker
