# from typing import Annotated

# from fastapi import APIRouter, Depends, Response, status
# from sqlalchemy.ext.asyncio import AsyncSession

# from ..utils import get_user
# from ..exceptions import NotEnoughRightsException
# from src.auth.schemas import UserRead
# from src.auth.config import current_active_user
# from src.auth.models import User
# from src.database import get_async_session

# router = APIRouter(
#     prefix="/users",
#     tags=["Admin functions"]
# )


# # @router.patch("/{id}/set_admin", status_code=status.HTTP_200_OK)
# # async def user_set_administrator(
# #     admin: Annotated[UserRead, Depends(current_active_user)],
# #     user: Annotated[User, Depends(get_user)],
# #     session: AsyncSession = Depends(get_async_session)
# # ):
# #     if admin.role_name != "Администратор":
# #         raise NotEnoughRightsException
# #     stmt = user.role_name = "Администратор"
# #     session.add(stmt)
# #     await session.refresh()
# #     await session.commit()
# #     return Response(status_code=status.HTTP_200_OK)
