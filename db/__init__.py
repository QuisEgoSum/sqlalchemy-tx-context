import sqlalchemy

from db.sql import proxy_sqlalchemy_query_factory, Execute
from db.context import transaction, configure
from db import types


select = proxy_sqlalchemy_query_factory(sqlalchemy.select)
insert = proxy_sqlalchemy_query_factory(sqlalchemy.insert)
update = proxy_sqlalchemy_query_factory(sqlalchemy.update)
delete = proxy_sqlalchemy_query_factory(sqlalchemy.delete)
union_all = proxy_sqlalchemy_query_factory(sqlalchemy.union)
exists = proxy_sqlalchemy_query_factory(sqlalchemy.exists)

