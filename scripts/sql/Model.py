from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    age = Column(Integer)
    address = Column(String(100))

    def __repr__(self):
        return "<User(id='%s',name='%s', age='%s', address='%s')>" % (self.id,
            self.name, self.age, self.address)