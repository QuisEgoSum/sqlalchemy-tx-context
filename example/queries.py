import asyncio

from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession

from example.connection import db
from example.models import Test


class StubException(Exception):
    pass


async def test():
    delete_result = await db.delete(Test).rowcount()

    print('Delete result', delete_result)

    insert_result = await db.insert(Test).values(id=1, name='test 1').execute()
    print('Inserted count', insert_result.rowcount)

    select_result = await db.select(Test.__table__).where(Test.id == 1).mapped_all()
    print('Select all', select_result)

    update_result = await db.update(Test)\
        .where(Test.id == 1)\
        .values(name='test 2')\
        .returning(Test.__table__)\
        .mapped_one()
    print('Updated dict', dict(**update_result))

    async with db.transaction() as tx1:
        assert isinstance(tx1, AsyncSession)
        tx_inserted_1 = await db.insert(Test).values(id=3, name='test 3').returning(Test.__table__).mapped_first()
        print('Insert in tx 1', tx_inserted_1)
        try:
            async with db.transaction() as tx2:
                assert isinstance(tx2, AsyncSessionTransaction)
                await db.insert(Test).values(id=4, name='test 4').execute()
                raise StubException()
        except StubException:
            pass
        async with db.transaction():
            await db.insert(Test).values(id=5, name='test 5').execute()

    assert await db.exists(Test.id).where(Test.id == 3).select().scalar() is True
    assert await db.exists(Test.id).where(Test.id == 4).select().scalar() is False
    assert await db.exists(Test.id).where(Test.id == 5).select().scalar() is True

    async with db.transaction() as tx:
        await db.insert(Test).values(id=6, name='test 6').execute()
        await tx.rollback()

    assert await db.exists(Test.id).where(Test.id == 6).select().scalar() is False


if __name__ == '__main__':
    asyncio.run(test())



