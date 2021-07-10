from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base, create_session


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(
        Integer, primary_key=True, index=True, unique=True, autoincrement=True
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="user_settings")
    user_filter = relationship(
        "UserFilter",
        back_populates="user_settings",
        cascade="all, delete, delete-orphan",
    )
    user_qa_metrics_filter = relationship(
        "UserQAMetricsFilter",
        back_populates="user_settings",
        cascade="all, delete, delete-orphan",
    )
    user_predictions_table = relationship(
        "UserPredictionsTable",
        back_populates="user_settings",
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self):
        return f"<UserSettings(id='{self.id}', user_id='{self.user_id}')>"

    async def create(self):
        with create_session() as db:
            db.add(self)
            db.commit()
            db.refresh(self)
        return self
