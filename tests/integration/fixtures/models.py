from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class ExampleModel(Base):
    __tablename__ = 'example'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    value: Mapped[str] = mapped_column(String())
