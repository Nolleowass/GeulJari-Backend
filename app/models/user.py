from sqlalchemy import Column, Text, VARCHAR, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    account_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(VARCHAR(20), nullable=False)
    user_name = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    profile_image_url = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    
    # source = relationship("Relation", back_populates="user")
    # target = relationship("Relation", back_populates="user")