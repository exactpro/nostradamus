from pydantic import BaseModel, Extra


class UserSerializer(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        orm_mode = True
        extra = Extra.allow
