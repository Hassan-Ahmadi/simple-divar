from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base


class AD(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)
        
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="ads")

    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, onupdate=text('CURRENT_TIMESTAMP'))
