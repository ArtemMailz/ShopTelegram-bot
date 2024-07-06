from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv('.env')
DB_TIPS = os.getenv('DB_TIP')
DB_DIALECT = os.getenv('DB_DIALECT')
DB_NAME_USER = os.getenv('DB_NAME_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')

async_engine = create_async_engine(
    f"{DB_TIPS}+{DB_DIALECT}://{DB_NAME_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
    echo = False,
    future = True
)

session_orm = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f'{getattr(self, col)}')
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
