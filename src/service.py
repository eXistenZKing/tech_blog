"""
Служебный модуль для добавления необходимых
для работы приложения записей при развертывании.
"""

# from fastapi import Depends
# from sqlalchemy import select

# from .models import UserRole
# from src.database import async_session, get_async_session


# async def init_db():
#     async with async_session() as session:
#         roles = await session.execute(select(UserRole))
#         if not roles.scalars().first():
#             async with session.begin():
#                 user_role = UserRole(name="Пользователь")
#                 admin_role = UserRole(name="Администратор")
#                 session.add(user_role)
#                 session.add(admin_role)
#             await session.commit()


# async def add_user(name: str, session=Depends(get_async_session)):
#     # Создаём объект User (инстанс модели)
#     new_user = UserRole(name=name)
#     # Добавляем объект в сессию
#     session.add(new_user)
#     # Сохраняем изменения в базе данных
#     await session.commit()
