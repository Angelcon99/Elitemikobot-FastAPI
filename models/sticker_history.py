from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import relationship
from database import Base


class StickerHistory(Base):
    __tablename__ = "StickerHistory"

    history_id = Column("HistoryId", BigInteger, primary_key=True, autoincrement=True)

    sticker_id = Column("StickerId", String, nullable=False)
    sticker_option_flag = Column("StickerOptionFlag", Integer, nullable=False)
    sticker_title = Column("StickerTitle", String, nullable=False)
    registed_date_time = Column("RegistedDateTime", DateTime, nullable=False)
    url = Column("Url", String, nullable=False)
    user_id = Column("UserId", BigInteger, ForeignKey("Users.UserId"), nullable=False)

    backed_up_at = Column("BackedUpAt", DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="sticker_histories")

    __table_args__ = (
        Index("idx_sticker_history_lookup", sticker_id, sticker_option_flag),
    )