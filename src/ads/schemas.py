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


# # Properties to receive on item update
# class ItemUpdate(ItemBase):
#     pass


# Properties shared by models stored in DB
class ADInDBBase(ADBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# # Properties to return to client
# class Item(ItemInDBBase):
#     pass


# # Properties properties stored in DB
# class ItemInDB(ItemInDBBase):
#     pass