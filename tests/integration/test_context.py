import asyncio

from typing import Optional

import pytest

from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncEngine

from sqlalchemy_tx_context import SQLAlchemyTransactionContext
from sqlalchemy_tx_context.exceptions import NoSessionError
from tests.integration.types import ExampleTupleType


@pytest.mark.asyncio
async def test_transaction_commit(sqlite_engine: AsyncEngine, example_table: Table):
    db = SQLAlchemyTransactionContext(sqlite_engine)

    async with db.transaction() as session:
        await session.execute(insert(example_table).values(value="Value"))

    async with db.session() as session:
        result = await session.execute(select(example_table.c.value))
        names = [row.value for row in result]
        assert names == ["Value"]


@pytest.mark.asyncio
async def test_transaction_rollback_on_error(
    sqlite_engine: AsyncEngine,
    example_table: Table,
):
    db = SQLAlchemyTransactionContext(sqlite_engine)

    with pytest.raises(RuntimeError):
        async with db.transaction() as session:
            await session.execute(insert(example_table).values(value="Value"))
            raise RuntimeError("fail")

    async with db.session() as session:
        result = await session.execute(select(example_table.c.value))
        names = [row.value for row in result]
        assert names == []


@pytest.mark.asyncio
async def test_parallel_sessions(sqlite_engine: AsyncEngine, example_table: Table):
    db = SQLAlchemyTransactionContext(sqlite_engine)

    async def write_record(value: str):
        async with db.new_session() as new_session:
            await new_session.execute(insert(example_table).values(value=value))
            await new_session.commit()

    await asyncio.gather(
        write_record("log1"),
        write_record("log2"),
    )

    async with db.session() as session:
        result = await session.execute(select(example_table.c.value))
        msgs = sorted(row.value for row in result)
        assert msgs == ["log1", "log2"]


async def test_auto_context_on_execute(
    sqlite_engine: AsyncEngine,
    example_table: Table,
):
    db = SQLAlchemyTransactionContext(sqlite_engine, auto_context_on_execute=True)

    insert_result = await db.execute(
        insert(example_table)
        .values(value="Value")
        .returning(example_table.c.id, example_table.c.value),
    )
    insert_value: Optional[ExampleTupleType] = insert_result.tuples().first()

    assert insert_value is not None

    exists_result = await db.execute(
        select(example_table.c.id, example_table.c.value).where(
            example_table.c.id == insert_value.id,
        ),
    )
    exists_value: Optional[ExampleTupleType] = exists_result.tuples().first()

    assert exists_value is not None
    assert exists_value.value == "Value"

    await db.execute(
        update(example_table)
        .values(value="Value 2")
        .where(example_table.c.id == insert_value.id),
    )

    update_result = await db.execute(
        select(example_table.c.id, example_table.c.value).where(
            example_table.c.id == insert_value.id,
        ),
    )
    updated_value: Optional[ExampleTupleType] = update_result.tuples().first()

    assert updated_value is not None
    assert updated_value.value == "Value 2"

    await db.execute(delete(example_table).where(example_table.c.id == insert_value.id))

    delete_result = await db.execute(
        select(example_table.c.id, example_table.c.value).where(
            example_table.c.id == insert_value.id,
        ),
    )
    deleted_value = delete_result.first()

    assert deleted_value is None


async def test_execute_without_context_should_fail(
    sqlite_engine: AsyncEngine,
    example_table: Table,
):
    db = SQLAlchemyTransactionContext(sqlite_engine)
    with pytest.raises(NoSessionError):
        await db.execute(select(example_table.c.id))


async def test_nested_transaction(
    sqlite_engine: AsyncEngine,
    example_table: Table,
):
    db = SQLAlchemyTransactionContext(sqlite_engine)

    async with db.transaction() as outer_session:
        await outer_session.execute(insert(example_table).values(value="outer"))

        try:
            async with db.transaction() as inner_session:
                await inner_session.execute(insert(example_table).values(value="inner"))
                raise RuntimeError("force rollback inner")
        except RuntimeError:
            pass

        await outer_session.execute(insert(example_table).values(value="outer2"))

    async with db.session() as session:
        result = await session.execute(
            select(example_table.c.value).order_by(example_table.c.value),
        )
        values = [row.value for row in result]
        assert values == ["outer", "outer2"]
