from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "postgresql://Admin_P:12345@localhost:5432/myFirstDatabase"
# Connection postgresql://<user>:<password>@<host>:<port>/<database_name>
# Port: 5432

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This is used to get general info about our database like tables name and more
inspector = inspect(engine)