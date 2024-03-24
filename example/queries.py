import asyncio

from example.connection import db
from example.models import Test


async def test():
    delete_result = await db.delete(Test).rowcount()

    print('Delete result', delete_result)

    insert_result = await db.insert(Test).values(id=1, name='test 1').execute()
    print(
        'Inserted count',
        insert_result.rowcount,
        type(insert_result)
    )

    select_result = await db.select(Test.__table__).where(Test.id == 1).mapped_all()
    print('Select all', select_result)

    update_result = await db.update(Test)\
        .where(Test.id == 1)\
        .values(name='test 2')\
        .returning(Test.__table__)\
        .mapped_one()
    print('Updated dict', dict(**update_result))


if __name__ == '__main__':
    asyncio.run(test())



