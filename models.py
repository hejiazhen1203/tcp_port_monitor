#!/usr/bin/env python
# -*- coding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config
Base = declarative_base()

class Monitor(Base):
    __tablename__ = 'monitor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    httpaddr = Column(String, unique=True, nullable=False)
    success = Column(Integer, default=0, nullable=False)
    faild = Column(Integer, default=0, nullable=False)
    last_commit = Column(String)
    alerts = Column(Integer, default=0, nullable=False)
    coment = Column(Text)
    def __repr__(self):
        return '<Test %r>' % self.name
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
Session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

#
if __name__ == '__main__':

    Base.metadata.create_all(engine)

    # session = Session()
    # test1 = Monitor(name=u"啊129ssh",httpaddr="192.168.10.129:222",coment=u"192ssh端口检查")
    # session.add(test1)
    # session.commit()