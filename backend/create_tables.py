#! ./venv/bin/python

from app.models import engine
from app.models import Base
from app.models import score

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()