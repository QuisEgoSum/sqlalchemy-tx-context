import asyncio

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from sqlalchemy import Table, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import immutabledict

from sqlalchemy_tx_context import SQLAlchemyTransactionContext
from sqlalchemy_tx_context.exceptions import (
    NoSessionError,
    SessionAlreadyActiveError,
    TransactionAlreadyActiveError,
)


@pytest.mark.asyncio
async def test_session(
    mock_engine: AsyncMock,
    mock_async_session_maker: MagicMock,
) -> None:
    db = SQLAlchemyTransactionContext(mock_engine)

    with pytest.raises(NoSessionError):
        db.get_session(strict=True)

    assert db.get_session(strict=False) is None

    async with db.session() as session:
        assert isinstance(session, AsyncSession)
        assert db.get_session() is session
        assert isinstance(db.get_session(strict=True), AsyncSession)
        assert isinstance(db.get_session(strict=False), AsyncSession)
        assert session.in_transaction() is False

        async with db.new_session() as session2:
            assert isinstance(session2, AsyncSession)
            assert db.get_session() is session2

        assert db.get_session() is session

        with pytest.raises(SessionAlreadyActiveError):
            async with db.session():
                pass

        async with db.session(reuse_if_exists=True) as session3:
            assert isinstance(session3, AsyncSession)
            assert db.get_session() is session3
            assert session is session3

    async with db.session(session_maker=mock_async_session_maker):
        mock_async_session_maker.assert_called_once()
        mock_async_session_maker.reset_mock()

    db2 = SQLAlchemyTransactionContext(
        mock_engine,
        default_session_maker=mock_async_session_maker,
    )

    async with db2.session():
        mock_async_session_maker.assert_called_once()
        mock_async_session_maker.reset_mock()


@pytest.mark.asyncio
async def test_transaction(mock_engine: AsyncMock) -> None:
    db = SQLAlchemyTransactionContext(mock_engine)

    async with db.transaction() as session:
        assert isinstance(session, AsyncSession)
        assert db.get_session() is session
        assert isinstance(db.get_session(strict=True), AsyncSession)
        assert isinstance(db.get_session(strict=False), AsyncSession)
        assert session.in_transaction() is True
        assert session.in_nested_transaction() is False

        async with db.new_transaction() as session2:
            assert isinstance(session2, AsyncSession)
            assert db.get_session() is session2
            assert session is not session2

        assert db.get_session() is session

        with pytest.raises(TransactionAlreadyActiveError):
            async with db.transaction(allow_nested_transactions=False):
                pass

        async with db.transaction():
            assert session.in_nested_transaction() is True

        assert session.in_nested_transaction() is False

    async with db.session() as session:  # noqa: SIM117
        async with db.transaction() as session2:
            assert isinstance(session2, AsyncSession)
            assert db.get_session() is session2
            assert session is session2


@pytest.mark.asyncio
async def test_session_gather(mock_engine: AsyncMock) -> None:
    db = SQLAlchemyTransactionContext(mock_engine)

    async with db.session() as session:

        async def with_new_session() -> None:
            async with db.new_session() as session2:
                assert isinstance(session2, AsyncSession)
                assert db.get_session() is session2
                assert session is not session2

        async def without_new_session() -> None:
            assert db.get_session() is session

        await asyncio.gather(without_new_session(), with_new_session())

        assert db.get_session() is session


@pytest.mark.asyncio
async def test_execute(
    mock_engine: AsyncMock,
    example_table: Table,
    mock_async_session: AsyncMock,
    mock_async_session_maker: MagicMock,
) -> None:
    db = SQLAlchemyTransactionContext(
        mock_engine,
        default_session_maker=mock_async_session_maker,
    )

    select_stmt = select(example_table.c.id)

    with pytest.raises(NoSessionError):
        await db.execute(select_stmt)

    async with db.session():
        await db.execute(select_stmt)
        mock_async_session.execute.assert_called_once_with(
            select_stmt,
            None,
            execution_options=immutabledict(),
            bind_arguments=None,
        )
        mock_async_session.execute.reset_mock()

    async with db.session():
        await db.execute(
            select_stmt,
            {"param": "value"},
            execution_options={"option": "value"},
            bind_arguments={"bind_arg": "value"},
            _parent_execute_state="value",
        )
        mock_async_session.execute.assert_called_once_with(
            select_stmt,
            {"param": "value"},
            execution_options={"option": "value"},
            bind_arguments={"bind_arg": "value"},
            _parent_execute_state="value",
        )
        mock_async_session.execute.reset_mock()


@pytest.mark.asyncio
async def test_execute_with_auto_session(
    mock_engine: AsyncMock,
    example_table: Table,
    mock_async_session: AsyncMock,
    mock_async_session_maker: MagicMock,
) -> None:
    db = SQLAlchemyTransactionContext(
        mock_engine,
        default_session_maker=mock_async_session_maker,
        auto_context_on_execute=True,
    )

    with (
        patch.object(db, 'session', wraps=db.session) as mock_session,
        patch.object(db, 'transaction', wraps=db.transaction) as mock_transaction,
    ):
        select_stmt = select(example_table.c.id)

        await db.execute(select_stmt)

        mock_async_session.execute.assert_called_once_with(
            select_stmt,
            None,
            execution_options=immutabledict(),
            bind_arguments=None,
        )

        mock_session.assert_called_once()
        mock_transaction.assert_not_called()

        mock_async_session.reset_mock()

    with (
        patch.object(db, 'session', wraps=db.session) as mock_session,
        patch.object(db, 'transaction', wraps=db.transaction) as mock_transaction,
    ):
        select_stmt = select(example_table.c.id)

        await db.execute(
            select_stmt,
            {"param": "value"},
            execution_options={"option": "value"},
            bind_arguments={"bind_arg": "value"},
            _parent_execute_state="value",
            force_transaction=True,
        )

        mock_async_session.execute.assert_called_once_with(
            select_stmt,
            {"param": "value"},
            execution_options={"option": "value"},
            bind_arguments={"bind_arg": "value"},
            _parent_execute_state="value",
        )

        mock_session.assert_called_once()
        mock_transaction.assert_called_once()

        mock_async_session.reset_mock()

    with (
        patch.object(db, 'session', wraps=db.session) as mock_session,
        patch.object(db, 'transaction', wraps=db.transaction) as mock_transaction,
    ):
        update_stmt = (
            update(example_table).values(value="value").where(example_table.c.id == 1)
        )

        await db.execute(update_stmt)

        mock_async_session.execute.assert_called_once_with(
            update_stmt,
            None,
            execution_options=immutabledict(),
            bind_arguments=None,
        )

        mock_session.assert_called_once()
        mock_transaction.assert_called_once()

        mock_async_session.reset_mock()

    db2 = SQLAlchemyTransactionContext(
        mock_engine,
        default_session_maker=mock_async_session_maker,
        auto_context_on_execute=True,
        auto_context_force_transaction=True,
    )

    with (
        patch.object(db2, 'session', wraps=db2.session) as mock_session,
        patch.object(db2, 'transaction', wraps=db2.transaction) as mock_transaction,
    ):
        select_stmt = select(example_table.c.id)

        await db2.execute(select_stmt)

        mock_async_session.execute.assert_called_once_with(
            select_stmt,
            None,
            execution_options=immutabledict(),
            bind_arguments=None,
        )

        mock_session.assert_called_once()
        mock_transaction.assert_called_once()

        mock_async_session.reset_mock()
