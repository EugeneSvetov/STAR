from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:Pesochek06@localhost"

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()

meta = MetaData()


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Users(Base):
    __tablename__ = "Users"
    pk = Column(Integer, primary_key=True)
    name = Column(String)
    sentences = Column(String)
    favourites = Column(String)
    dislikes = Column(String)



