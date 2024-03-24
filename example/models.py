from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from example.connection import Base


class Test(Base):
    __tablename__ = 'test'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(36), unique=True)

    def get_id(self):
        return self.id
