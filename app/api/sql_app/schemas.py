from pydantic import BaseModel
from typing import Optional

class ItemBaseLog(BaseModel):
    origin_language: Optional[str] = None
    language_to_translate: Optional[str] = None
    origin_text: Optional[str] = None
    translated_text: Optional[str] = None
    client_coutry: Optional[str] = None
    client_city: Optional[str] = None
    client_zip_code: Optional[str] = None
    using_phone: Optional[bool] = None

class CreateItemLod(ItemBaseLog):
    ip: str

class BaseLog(ItemBaseLog):
    ip: str

    class Config:
        orm_mode = True