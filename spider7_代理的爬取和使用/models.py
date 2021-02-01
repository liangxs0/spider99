# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True)
    ip = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    port = Column(String(10, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(20, 'utf8_unicode_ci'), nullable=False)
