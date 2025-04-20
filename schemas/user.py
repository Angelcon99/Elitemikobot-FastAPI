
from pydantic import BaseModel
from sqlalchemy import DateTime


class UserBlockRegister(BaseModel):
    user_id: int
    user_name: str        
    is_block: bool    
    notes: str
    