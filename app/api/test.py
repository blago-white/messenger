# from fastapi import APIRouter
# from fastapi import Depends
#
# from app.models.user import User
# from app.api.depencies import get_current_user
#
# router = APIRouter()
#
#
# @router.get("/me")
# async def me(
#     user: User = Depends(get_current_user),
# ):
#     return {
#         "id": str(user.id),
#         "username": user.username,
#         "name": user.name,
#     }
#
#
# app.include_router(
#     router,
#     prefix="/test",
#     tags=["test"]
# )
