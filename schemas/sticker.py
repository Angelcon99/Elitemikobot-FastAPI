from pydantic import BaseModel, Field
from datetime import datetime

class StickerRegister(BaseModel):
    sticker_id: int = Field(alias="stickerId")
    sticker_option_flag: int = Field(alias="stickerOptionFlag")
    sticker_title: str = Field(alias="stickerTitle")
    registed_date_time: datetime = Field(alias="registedDateTime")
    url: str
    user_id: int = Field(alias="userId")
    user_name: str = Field(alias="userName")   

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True  # 모델 반환 시에도 snake_case로


class StickerOut(StickerRegister):
    pass