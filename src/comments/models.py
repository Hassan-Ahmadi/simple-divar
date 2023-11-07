from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy import text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text_value = Column(String, unique=True, index=True)

    ad_id = Column(Integer, ForeignKey("ads.id"))
    ad = relationship("AD", back_populates="comments")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")

    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, onupdate=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        UniqueConstraint("ad_id", "user_id", name="unique_ad_user_comment"),)
