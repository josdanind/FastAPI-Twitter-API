# Python
from datetime import datetime

# SQLAlchemy
from sqlalchemy import Column,Integer, String, Date
from sqlalchemy import ForeignKey, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ----------
# User model
# ----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    birth_date = Column(Date)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    tweets = relationship("Tweet", back_populates="user")

# -----------
# Tweet model
# -----------
class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)

    user = relationship("User", back_populates="tweets")





