from pydantic import BaseModel, validator

from validators.email import validate_email_pattern, validate_email_uniqueness
from validators.name import validate_name_pattern, validate_name_uniqueness
from validators.validators import (
    validate_for_whitespace,
    validate_symbols_count,
)


class UserSerializer(BaseModel):
    email: str
    name: str
    password: str

    @validator("name",)
    def validate_name(cls, name: str):
        validate_for_whitespace(name, "username")
        validate_symbols_count(string=name, maximum=64, field_name="user")
        validate_name_uniqueness(name)
        validate_name_pattern(name)
        return name

    @validator("email")
    def validate_email(cls, email: str):
        email = email.lower()
        validate_for_whitespace(email, "email")
        validate_symbols_count(string=email, maximum=254, field_name="email")
        validate_email_uniqueness(email)
        validate_email_pattern(email)
        return email

    @validator("password")
    def validate_password(cls, password: str):
        validate_symbols_count(
            string=password, minimum=6, maximum=254, field_name="password"
        )
        return password


class UserCredentialsSerializer(BaseModel):
    credentials: str
    password: str


class AuthResponseSerializer(BaseModel):
    id: str
    name: str
    email: str
    token: str


class VerifyTokenResponse(BaseModel):
    id: str
