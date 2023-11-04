from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        max_length=100,
        description="The email address of the user",
        examples=["example@example.com"],
    )


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool = Field(..., description="To disable user in case")
    first_name: str | None = Field(
        ...,
        description="First name of the user",
        examples=["John"],
        max_length=100,
        min_length=2,
    )
    last_name: str | None = Field(
        ...,
        description="Last name of the user",
        examples=["Doe"],
        max_length=100,
        min_length=2,
    )
    phone_number: str | None = Field(
        ...,
        description="phone number with country code",
        examples=["+989191200824"],
        max_length=50,
        min_length=13,
    )

    class Config:
        from_attributes = True


# Setting fields that are allowed to be updated
class UserUpdate(BaseModel):
    first_name: str | None = Field(
        ..., description="First name of the user", examples=["John"], max_length=100
    )
    last_name: str | None = Field(
        ..., description="Last name of the user", examples=["Doe"], max_length=100
    )
    phone_number: str | None = Field(
        ...,
        description="phone number with country code",
        examples=["+989191200824"],
        max_length=50,
        pattern=r"^\+\d{10,15}$",
    )  # regex to validate phone number

    class Config:
        from_attributes = True
