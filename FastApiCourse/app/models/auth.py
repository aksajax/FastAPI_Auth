from pydantic import BaseModel,Field,EmailStr,field_validator,ValidationInfo
from typing import Optional

class Login(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    
class Register(BaseModel):
    name : str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)
    
    @field_validator("confirm_password")
    def passwords_match(cls, v, values, info: ValidationInfo):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v