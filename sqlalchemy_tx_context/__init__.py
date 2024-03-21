import sqlalchemy

from .sql import proxy_sqlalchemy_query_factory
from .context import transaction, configure


select = proxy_sqlalchemy_query_factory(sqlalchemy.select)
insert = proxy_sqlalchemy_query_factory(sqlalchemy.insert)
update = proxy_sqlalchemy_query_factory(sqlalchemy.update)
delete = proxy_sqlalchemy_query_factory(sqlalchemy.delete)
union = proxy_sqlalchemy_query_factory(sqlalchemy.union)
union_all = proxy_sqlalchemy_query_factory(sqlalchemy.union_all)
exists = proxy_sqlalchemy_query_factory(sqlalchemy.exists)
