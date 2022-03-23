"""
"""
from sqlalchemy import Column, Integer, ForeignKey, String

from core.ext import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    username = Column(Integer, ForeignKey('users.id'), nullable=False)