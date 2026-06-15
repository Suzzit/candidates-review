#! ./venv/bin/python

from models import engine, Base
from models.users import Users

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()