from core.app_config import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_async_engine(
    config.DATABASE_URL,
    echo=config.DEBUG,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# FastAPI 의존성 주입용
async def get_db():
    async with SessionLocal() as session:
        yield session