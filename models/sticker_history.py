from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import relationship
from database import Base


class StickerHistory(Base):
    __tablename__ = "sticker_history"

    history_id = Column(BigInteger, primary_key=True, autoincrement=True)

    sticker_id = Column(String, nullable=False)
    sticker_option_flag = Column(Integer, nullable=False)
    sticker_title = Column(String, nullable=False)
    registed_date_time = Column(DateTime, nullable=False)
    url = Column(String, nullable=False)
    user_id = Column(BigInteger, ForeignKey("Users.UserId"), nullable=False)

    backed_up_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="sticker_histories")

    __table_args__ = (
        Index("idx_sticker_history_lookup", "sticker_id", "sticker_option_flag"),
    )