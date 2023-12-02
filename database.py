from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import os

load_dotenv('.env')

SERVER = os.getenv("SERVER")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")

SQLALCHEMY_DATABASE_URL = f"mysql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}"
sql_script_path = 'assets/db_script.sql'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)
    with open(sql_script_path, 'r') as f:
        sql_script = f.read()
    with engine.connect() as con:
        con.execute(sql_script)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()