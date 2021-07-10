from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base, create_session


class UserPredictionsTable(Base):
    __tablename__ = "user_predictions_table"

    id = Column(
        Integer, primary_key=True, index=True, unique=True, autoincrement=True
    )
    settings_id = Column(
        Integer, ForeignKey("user_settings.id", ondelete="CASCADE")
    )
    name = Column(String)
    is_default = Column(Boolean)
    position = Column(Integer)

    user_settings = relationship(
        "UserSettings", back_populates="user_predictions_table"
    )

    def __repr__(self):
        return (
            f"<UserPredictionsTable(id='{self.id}', name='{self.name}', "
            f"is_default='{self.is_default}', position='{self.position}', "
            f"settings_id='{self.settings_id}')>"
        )

    async def create(self):
        with create_session() as db:
            db.add(self)
            db.commit()
            db.refresh(self)
        return self
