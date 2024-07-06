from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.engine import Base
from sqlalchemy import ForeignKey, String, text, BigInteger
from typing import List
import enum
import datetime

class ChapterEnum(enum.Enum):
    chapter_1 = 'MicroGreen'
    chapter_2 = "Prorostki"
    chapter_3 = "Flover"
    chapter_4 = "BabuGreen"

class UserORM(Base):
    __tablename__ = 'user_table'
    
    id_user: Mapped[int] = mapped_column(BigInteger, primary_key = True)
    sum_order: Mapped[int] = mapped_column(default = 0)
    
    id_order: Mapped[List["OrderORM"]] = relationship(back_populates = 'id_user')
    id_admin: Mapped["AdminORM"] = relationship(back_populates = 'id_client')
     
class OrderORM(Base):
     __tablename__ = 'order_table'
     
     id_owner: Mapped[int] = mapped_column(BigInteger, ForeignKey("user_table.id_user"))
     id_order: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
     status_order: Mapped[str] = mapped_column(String(20))
     list_asortiment: Mapped[int] = mapped_column(ForeignKey("asortiment_table.id"))
     
     id_user: Mapped["UserORM"] = relationship(back_populates = 'id_order')
     list_position: Mapped[List["AsortimentORM"]] = relationship(
         back_populates = 'id_orders'
     )
     
class AdminORM(Base):
    __tablename__ = 'admin_table'
    
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name_user: Mapped[str] = mapped_column(String(20))
    id_user: Mapped[int] = mapped_column(BigInteger, ForeignKey("user_table.id_user"))
    password_user: Mapped[int]
    
    id_client: Mapped["UserORM"] = relationship(back_populates = 'id_admin')
    
class AsortimentORM(Base):
    __tablename__ = 'asortiment_table'
    
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name_position: Mapped[str] = mapped_column(String(20))
    description_position: Mapped[str] = mapped_column(String(123))
    massa_position: Mapped[int]
    chapter_position: Mapped[ChapterEnum]
    praice_position: Mapped[int]
    
    id_orders: Mapped[List["OrderORM"]] = relationship(
        back_populates = 'list_position'
    )