from collections.abc import AsyncGenerator

import pytest

from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


@pytest.fixture
async def sqlite_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    yield engine
    await engine.dispose()


@pytest.fixture
def metadata() -> MetaData:
    return MetaData()


@pytest.fixture
def example_table(metadata: MetaData) -> Table:
    return Table(
        "example",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("value", String),
    )


@pytest.fixture(autouse=True)
async def auto_create_tables(
    metadata: MetaData,
    sqlite_engine: AsyncEngine,
    example_table: Table,  # noqa: ARG001
):
    async with sqlite_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    async with sqlite_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
