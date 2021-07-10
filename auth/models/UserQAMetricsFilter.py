from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from database import Base, create_session


class UserQAMetricsFilter(Base):
    __tablename__ = "user_qa_metrics_filter"

    id = Column(
        Integer, primary_key=True, index=True, unique=True, autoincrement=True
    )
    settings_id = Column(
        Integer, ForeignKey("user_settings.id", ondelete="CASCADE")
    )
    name = Column(String)
    type = Column(String)

    user_settings = relationship(
        "UserSettings", back_populates="user_qa_metrics_filter"
    )

    def __repr__(self):
        return (
            f"<UserQAMetricsFilter(id='{self.id}', name='{self.name}', "
            f"type='{self.type}', settings_id='{self.settings_id}')>"
        )

    async def create(self):
        with create_session() as db:
            db.add(self)
            db.commit()
            db.refresh(self)
        return self
