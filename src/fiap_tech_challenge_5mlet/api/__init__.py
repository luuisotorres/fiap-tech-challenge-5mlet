from .routes import router as api_router
from .auth_routes import router as auth_router

__all__ = [
    'api_router',
    'auth_router'
]
