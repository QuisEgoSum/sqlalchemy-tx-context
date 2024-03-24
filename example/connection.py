from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy_tx_context import SQLAlchemyTransactionContext

connect_args = dict(
    max_cached_statement_lifetime=0,
    statement_cache_size=5000,
    server_settings={
        'application_name': 'test'
    }
)


engine = create_async_engine(
    'postgresql+asyncpg://test:test@127.0.0.1:5432/test',
    connect_args=connect_args,
    pool_size=1,
    max_overflow=0
)

db = SQLAlchemyTransactionContext(engine)


class Base(DeclarativeBase):
    __abstract__ = True
