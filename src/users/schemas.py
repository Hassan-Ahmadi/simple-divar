from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    first_name: str
    last_name: str
    phone_number: str

    class Config:
        from_attributes = True
