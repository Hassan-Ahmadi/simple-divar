from typing import Optional

from pydantic import BaseModel


# Shared properties
class ADBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ADCreate(ADBase):
    title: str
    owner_id: int


# Properties to receive on item update
class ADUpdate(ADBase):
    pass


# Properties to return to client
class AD(ADBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
