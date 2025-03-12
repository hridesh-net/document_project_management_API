from functools import wraps
from fastapi import HTTPException, status

def require_permission(permission: str):
    """
    Decorator to enforce that the 'current_user' (an instance of User)
    has the specified permission based on their assigned Role.
    The decorated endpoint must include a parameter named 'current_user'.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )

            if not current_user.role or not current_user.role.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User has no role or permissions assigned"
                )

            user_permissions = [perm.name for perm in current_user.role.permissions]
            print(f"user_permissions: {user_permissions}")
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator