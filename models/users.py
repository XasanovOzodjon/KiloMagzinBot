from data.database import Base
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from datetime import datetime
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    created_at = Column(String, nullable=True, default=datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=True, onupdate=datetime.utcnow().isoformat())
    

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, default=None)
    new_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(String, nullable=True, default=datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=True, onupdate=datetime.utcnow().isoformat())

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(String, nullable=True, default=datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=True, onupdate=datetime.utcnow().isoformat())