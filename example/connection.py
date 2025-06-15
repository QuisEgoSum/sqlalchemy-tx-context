import os

from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy_tx_context import SQLAlchemyTransactionContext

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)

engine = create_async_engine(DATABASE_URL, echo=True)
db = SQLAlchemyTransactionContext(engine)
