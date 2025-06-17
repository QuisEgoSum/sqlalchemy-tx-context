import asyncio
import sys

from collections.abc import Sequence
from typing import Any, Optional, cast

import pytest

from sqlalchemy import CursorResult, Row, Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncEngine

from sqlalchemy_tx_context import SQLAlchemyTransactionContext
from sqlalchemy_tx_context.exceptions import NoSessionError
from tests.integration.fixtures.models import ExampleModel
from tests.integration.types import ExampleTupleType


@pytest.mark.asyncio
async def test_transaction_commit(
    sqlite_engine: AsyncEngine,
    example_table: Table,
) -> None:
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
) -> None:
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
async def test_parallel_sessions(
    sqlite_engine: AsyncEngine,
    example_table: Table,
) -> None:
    db = SQLAlchemyTransactionContext(sqlite_engine)

    async def write_record(value: str) -> None:
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
) -> None:
    db = SQLAlchemyTransactionContext(sqlite_engine, auto_context_on_execute=True)

    insert_result = await db.execute(
        insert(example_table)
        .values(value="Value")
        .returning(example_table.c.id, example_table.c.value),
    )
    # pyright considers tuples().first() incompatible with NamedTuple; mypy accepts it.
    insert_value: Optional[ExampleTupleType] = cast(
        Optional[ExampleTupleType],
        insert_result.tuples().first(),
    )

    assert insert_value is not None

    exists_result = await db.execute(
        select(example_table.c.id, example_table.c.value).where(
            example_table.c.id == insert_value.id,
        ),
    )
    # pyright considers tuples().first() incompatible with NamedTuple; mypy accepts it.
    exists_value: Optional[ExampleTupleType] = cast(
        Optional[ExampleTupleType],
        exists_result.tuples().first(),
    )

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
    # pyright considers tuples().first() incompatible with NamedTuple; mypy accepts it.
    updated_value: Optional[ExampleTupleType] = cast(
        Optional[ExampleTupleType],
        update_result.tuples().first(),
    )

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
) -> None:
    db = SQLAlchemyTransactionContext(sqlite_engine)
    with pytest.raises(NoSessionError):
        await db.execute(select(example_table.c.id))


async def test_nested_transaction(
    sqlite_engine: AsyncEngine,
    example_table: Table,
) -> None:
    db = SQLAlchemyTransactionContext(sqlite_engine)

    async with db.transaction():
        await db.execute(insert(example_table).values(value="outer"))

        try:
            async with db.transaction():
                await db.execute(insert(example_table).values(value="inner"))
                raise RuntimeError("force rollback inner")
        except RuntimeError:
            pass

        await db.execute(insert(example_table).values(value="outer2"))

    async with db.session() as session:
        result = await session.execute(
            select(example_table.c.value).order_by(example_table.c.value),
        )
        values = [row.value for row in result]
        assert values == ["outer", "outer2"]


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Only valid in Python 3.12+")
async def test_execute_typing(sqlite_engine: AsyncEngine) -> None:
    from typing import assert_type

    db = SQLAlchemyTransactionContext(sqlite_engine)

    async with db.transaction():
        insert_result = await db.execute(insert(ExampleModel).values(value="outer"))

        assert_type(insert_result, CursorResult[Any])

        update_result = await db.execute(select(ExampleModel.id, ExampleModel.value))

        typed_rows = update_result.all()

        assert_type(typed_rows, Sequence[Row[tuple[int, str]]])
