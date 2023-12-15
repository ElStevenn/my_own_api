from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BINARY, Float, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.orm import configure_mappers
configure_mappers()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    username = Column(String, nullable=False, unique=True)
    name =  Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(BINARY, nullable=False)
    is_active = Column(Boolean, default=False)

    @property
    def to_dict(self):
        """Only returns username, name, suername and email"""
        return {
            "username": self.username,
            "name": self.name,
            "surname": self.surname,
            "email": self.email            
        }