from sqlalchemy import Column, Text, VARCHAR, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import Date, DateTime

Base = declarative_base()

class Diary(Base):
    __tablename__ = "diary"
    
    diary_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    content = Column(VARCHAR(200), nullable=False) 
    create_at = Column(DateTime, default=current_timestamp())
    account_id = Column(Integer, nullable=False)
    emotion_point = Column(Integer, nullable=False)