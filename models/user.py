from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "Users"

    user_id = Column("UserId", Integer, primary_key=True)
    user_name = Column("UserName", String, nullable=False)
    register_count = Column("RegisterCount", Integer, default=0)
    is_blocked = Column("IsBlocked", Boolean, default=False)
    block_changed_at = Column("BlockChangedAt", DateTime)
    notes = Column("Notes", String)
    
    stickers = relationship("Sticker", back_populates="user")
    sticker_histories = relationship("StickerHistory", back_populates="user")
