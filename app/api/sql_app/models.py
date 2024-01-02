from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BINARY, Float, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid, requests
from sqlalchemy.orm import configure_mappers
configure_mappers()

from .database import Base



class Translator_logs(Base):
    __tablename__ = "translator_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_ip = Column(String(20), nullable=False)
    origin_language = Column(String(20))
    language_to_translate = Column(String(20))
    origin_text = Column(String)
    translated_text = Column(String)
    client_country = Column(String)
    client_city = Column(String)
    zip_code = Column(String)
    using_phone = Column(Boolean, default=False)

    @property
    def to_dict(self):
        return {
            'id': str(self.id),  
            'client_ip': str(self.client_ip),  
            'origin_language': self.origin_language,
            'language_to_translate': self.language_to_translate,
            'origin_text': self.origin_text,
            'translated_text': self.translated_text,
            'client_country': self.client_city,
            'client_city': self.client_city,
            'client_zip_code': self.zip_code,
            'using_phone': self.using_phone
        }

