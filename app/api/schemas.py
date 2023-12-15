from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    name: str
    surname: str
    password: str
    email: str
    
class UserLogin(UserBase):
    password: str

class ModifyPassowrd():
    password: str # Password that user wants to modify


class EmailBasicStructure():
    to: str
    subject: str
    text: str = None

