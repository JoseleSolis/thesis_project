from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine(
    "sqlite:///data.db",
    connect_args={"check_same_thread": False},
)


class Person(Base):
        __tablename__ = 'person'
        id = Column(Integer, primary_key=True)
        name = Column(String(20))
        last_name = Column(String(20))
        

class Item(Base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        serial_number = Column(String(8))
        description = Column(String(256))
        stock_number = Column(Integer)




