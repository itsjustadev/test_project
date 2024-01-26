from aiogram.types.base import String
from sqlalchemy import create_engine, Column, String, Text, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import pytz
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
username = str(os.getenv('USERNAME'))
password = str(os.getenv('PASSWORD'))
host = str(os.getenv('HOST'))
port = str(os.getenv('PORT'))
database = str(os.getenv('DATABASE'))

connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    chat_id = Column(Integer, primary_key=True)
    username = Column(String, default='')
    first_name = Column(String, default='')
    last_name = Column(String, default='')
    registration_date = Column(
        DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Moscow')))


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    user_message = Column(String, default='')
    gpt_message = Column(String, default='')
    response_time = Column(String, default='')
    message_time = Column(
        DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Moscow')))


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_user(chat: int, username, first_name, last_name):
    user = Users(chat_id=chat, username=username, first_name=first_name,
                 last_name=last_name)
    session.merge(user)
    session.commit()


def add_history(user_message, gpt_message, response_time):
    activity = History(user_message=user_message, gpt_message=gpt_message,
                       response_time=response_time)
    session.add(activity)
    session.commit()


session.close()
