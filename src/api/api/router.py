from fastapi import APIRouter

from api.routes import auth, deposits, groups, links, tags, users, withdrawals


api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(groups.router)
api_router.include_router(deposits.router)
api_router.include_router(withdrawals.router)
api_router.include_router(tags.router)
api_router.include_router(links.router)
