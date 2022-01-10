from sqlalchemy import Column, Text, VARCHAR, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
Base = declarative_base()


class Relation(Base):
    __tablename__ = "relation"
    relation_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    source_id = Column(Integer)
    target_id = Column(Integer)
    # source = relationship('User', back_populates="source")
    # target = relationship('User', back_populates="target")    