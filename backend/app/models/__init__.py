import sqlalchemy as sa
from sqlalchemy import orm


engine = sa.create_engine(
    "sqlite:///candidate.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

Base = orm.declarative_base()
Base.metadata.create_all(bind=engine)