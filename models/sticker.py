from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Sticker(Base):
    __tablename__ = "Stickers"

    sticker_id = Column("StickerId", Integer, primary_key=True)
    sticker_option_flag = Column("StickerOptionFlag", Integer, primary_key=True)
    sticker_title = Column("StickerTitle", String, nullable=False)
    registed_date_time = Column("RegistedDateTime", DateTime, nullable=False)
    url = Column("Url", String, nullable=False)
    user_id = Column("UserId", Integer, ForeignKey("Users.UserId"), nullable=False)

    user = relationship("User", back_populates="stickers")
