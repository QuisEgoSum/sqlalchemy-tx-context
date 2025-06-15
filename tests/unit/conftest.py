from unittest.mock import AsyncMock, MagicMock

import pytest

from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


@pytest.fixture
def mock_engine() -> AsyncMock:
    return AsyncMock(spec=AsyncEngine)


@pytest.fixture
def mock_async_session() -> AsyncMock:
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def mock_async_session_maker(mock_async_session: AsyncMock) -> MagicMock:
    cm = AsyncMock()
    cm.__aenter__.return_value = mock_async_session
    cm.__aexit__.return_value = None

    mock = MagicMock(return_value=cm)
    return mock


@pytest.fixture
def example_table() -> Table:
    metadata = MetaData()

    return Table(
        "example",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("value", String),
    )
