from pydantic import Field, BaseModel, EmailStr, field_validator, model_validator

class UserRegisterSchema(BaseModel):
    fullname: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=10)
    email: EmailStr = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=30)
    confirm_password: str = Field(min_length=8, max_length=30)

    @field_validator("*", mode="before")
    def validate_all(value):
        if not value:
            raise ValueError("Please fill all fields")
        return value
    
    @model_validator(mode="before")
    def validate_password(self):
        if self["password"] != self["confirm_password"]:
            raise ValueError("Passwords don't match!")
        return self


class UserSchema(BaseModel):
    id: int
    fullname: str
    username: str
    email: EmailStr
    class Config:
        orm_mode = True
class UserLoginSchema(BaseModel):
    username: str
    password: str

    

    @field_validator("*", mode="before")
    def check_all(value):
        if value is None:
            raise ValueError("All fields  are required")
        return value
    
    