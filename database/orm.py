from database.model import UserORM, OrderORM, AdminORM, AsortimentORM
from database.engine import session_orm, async_engine, Base
from sqlalchemy import select, text, insert, delete, update
from sqlalchemy.orm import selectinload
import asyncio


class AsyncORMfunctin():
    
    async def init_user(id_users: int): #регистрируем пользователя 
        new_user = UserORM(id_user = id_users)
        async with session_orm() as session:
            session.add(new_user)
            await session.commit()

    async def select_id_user(id_users: int): #проверка зарегестрирован ли пользователь
        async with async_engine.connect() as conn:
            stmt = await conn.execute(text("""SELECT id_user FROM user_table"""))
            stmt_return = stmt.scalars().all()
            for i in range(0, len(stmt_return)):
                if stmt_return[i] == id_users:
                    return True
                
    async def create_table(): #создание и удаление таблицы
        async with async_engine.connect() as conn:
            async_engine.echo = True
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
            
    async def select_sum_order(id_users: int): #проверка количества заказов у пользователя
        async with session_orm() as session:
            qure = (
                select(UserORM.sum_order)
                .select_from(UserORM)
                .filter(UserORM.id_user == id_users)
            )
            res = await session.execute(qure)
            result = (res.scalars().all())[0]
            return result
            
    async def select_admin_stare(id_users: int): #узнаем являеться ли пользователь админом 
        async with session_orm() as session:
            qure = (
                select(AdminORM.id_user)
                .select_from(AdminORM)
                .filter(AdminORM.id_user == id_users)
            )
            res = await session.execute(qure)
            result = res.scalars().all()
            return result
        
    async def select_password_user(id_users: int): #узнаем пароль для админа
        async with session_orm() as session:
            qure = (
                select(AdminORM.password_user)
                .select_from(AdminORM)
                .filter(AdminORM.id_user == id_users)
            )
            res = await session.execute(qure)
            result = res.scalars().all()
            return result[0]
        
    async def insert_new_position(name_pos: str, decpription_pos: str, mass_pos: int, chapter_pos, praice_pos: int): #добавляем новый товар
        async with session_orm() as session:
            qure = (
                insert(AsortimentORM)
                .values(
                    name_position = name_pos,
                    description_position = decpription_pos,
                    massa_position = mass_pos,
                    chapter_position = chapter_pos,
                    praice_position = praice_pos)
            )
            await session.execute(qure)
            await session.commit()
            
    async def select_id_position(chapter: str): #выборка id 
        async with session_orm() as session:
            qure = (
                select(AsortimentORM.id)
                .select_from(AsortimentORM)
                .where(AsortimentORM.chapter_position == chapter)
            )
            res = await session.execute(qure)
            result = res.scalars().all()
            return result
        
    async def select_name_position(chapter: str): #выборка имен позиций
        async with session_orm() as session:
            qure = (
                select(AsortimentORM.name_position)
                .select_from(AsortimentORM)
                .where(AsortimentORM.chapter_position == chapter)
            )
            res = await session.execute(qure)
            result = res.scalars().all()
            return result     
            
    async def insert_new_admin(id_users: int, passwords_users: int, name_users: str): #добавляем нового админа
        async with session_orm() as session:
            qure = (
                insert(AdminORM)
                .values(id_user = id_users,
                        password_user = passwords_users,
                        name_user = name_users)
            )
            await session.execute(qure)
            await session.commit()
            
    async def select_full_ifo_position(id_position: int): #выбираем по id все необходимые данные о товаре
        async with session_orm() as session:
            qure = (
                select(AsortimentORM.name_position, AsortimentORM.description_position, 
                       AsortimentORM.massa_position, AsortimentORM.praice_position)
                .select_from(AsortimentORM)
                .filter(AsortimentORM.id == id_position)
            )
            res = await session.execute(qure)
            result = res.all()
            return result[0]
        
    async def delete_position(id_position: int): #удаление позиции
        async with session_orm() as session:
            qure = (
                delete(AsortimentORM)
                .filter(AsortimentORM == id_position)
            )
            await session.execute(qure)
            await session.commit()
            
    async def select_admins_id(): #выбераем id админов
        async with session_orm() as session:
            qure = (
                select(AdminORM.id)
                .select_from(AdminORM)
            )
            res = await session.execute(qure)
            result = res.scalars().all()
            return result
    
    async def select_admins_name(): #выбераем имена админов
        async with session_orm() as session:
            qure = (
                select(AdminORM.name_user)
                .select_from(AdminORM)
            )
            res = await session.execute(qure)
            result = res.scalars().all()
            return result
        
    async def delet_admins(id_admin: int):
        async with session_orm() as session:
            qure = (
                delete(AdminORM)
                .filter(AdminORM.id == id_admin)
            )
            await session.execute(qure)
            await session.commit()
            
    async def update_name_position(id_position: int, new_name: str):
        async with session_orm() as session:
            qure = (
                update(AsortimentORM)
                .filter(AsortimentORM.id == id_position)
                .values(name_position = new_name)
            )
            await session.execute(qure)
            await session.commit()
    
    async def update_description_position(id_position, new_description):
        async with session_orm() as session:
            qure = (
                update(AsortimentORM)
                .filter(AsortimentORM.id == id_position)
                .values(description_position = new_description)
            )
            await session.execute(qure)
            await session.commit()
            
    async def update_mass_position(id_position, new_mass):
        async with session_orm() as session:
            qure = (
                update(AsortimentORM)
                .filter(AsortimentORM.id == id_position)
                .values(massa_position = new_mass)
            )
            await session.execute(qure)
            await session.commit()
            
    async def update_praice_position(id_position, new_praice):
        async with session_orm() as session:
            qure = (
                update(AsortimentORM)
                .filter(AsortimentORM.id == id_position)
                .values(praice_position = new_praice)
            )
            await session.execute(qure)
            await session.commit()
            
    async def insert_new_ordering(id_user, id_position):
        async with session_orm() as session:
            qure = (
                insert(OrderORM)
                .values(id_owner = id_user,
                        id_order = 12,
                        status_order = 'оплачен',
                        list_asortiment = id_position)
            )
            
            await session.execute(qure)
            await session.commit()