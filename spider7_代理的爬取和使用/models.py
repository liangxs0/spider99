# coding: utf-8
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(INTEGER(11), primary_key=True, comment='主键')
    ip = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    port = Column(String(10, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    uptime = Column(DateTime, nullable=False)
