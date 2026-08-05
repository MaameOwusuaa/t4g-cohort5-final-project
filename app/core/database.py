from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base

# creating an instance of declarative_base
Base = declarative_base()




load_dotenv() # loads all environmental variables

# building connection string: connection_str = "db:driver://usertname:password@localhost:3306/dbname"
connection_str = os.environ.get("DATABASE_URL")

# creating an instance of the engine from create_engine
engine = create_engine(connection_str, pool_pre_ping=True)


SessionFactory = sessionmaker(bind=engine)  #configuration for session
db_session = SessionFactory()  # actual session

try:
    with engine.connect() as connection:
        print("Successfully Connected To Database")
        connection.close()
except Exception as e:
    print(f"Failed to connect to the database: {e}")
    raise e 

Base.metadata.create_all(engine)