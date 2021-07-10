from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from database import Base, create_session


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, index=True, unique=True, autoincrement=True
    )
    email = Column(String, unique=True)
    name = Column(
        String,
        unique=True,
    )
    password = Column(String)

    user_settings = relationship(
        "UserSettings",
        uselist=False,
        back_populates="user",
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<User(id='{self.id}', email='{self.email}', name='{self.name}')>"
        )

    async def create(self):
        with create_session() as db:
            db.add(self)
            db.commit()
            db.refresh(self)
        return self
