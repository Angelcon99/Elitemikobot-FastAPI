from pydantic import BaseModel
from datetime import datetime

class StickerRegister(BaseModel):
    sticker_id: int
    sticker_option_flag: int
    sticker_title: str
    registed_date_time: datetime
    url: str
    user_id: int
    user_name: str

class StickerOut(StickerRegister):
    pass