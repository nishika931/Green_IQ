from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username must be between 3 and 50 characters"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Password must be at least 6 characters"
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)