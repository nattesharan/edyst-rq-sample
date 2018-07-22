from sqlalchemy import Column, Integer, String
from app import Base

class summary(Base):
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True)
    url = Column(String(50))
    word_count = Column(Integer())

    def __init__(self,url,word_count):
        self.url = url
        self.word_count = word_count

    def __repr__(self):
        return '<Summary %r>' % (self.url)