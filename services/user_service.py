from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserBlockRegister


logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    async def user_exists(db: AsyncSession, user_id: int) -> bool:
        stmt = select(User).where(
            User.user_id == user_id
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None 


    @staticmethod
    async def register_user(db: AsyncSession, user_id: int, user_name: str, skip_commit: bool = False) -> bool:
        try:
            exists = await UserService.user_exists(db, user_id)
            if exists:
                return True
            
            user = User(
                user_id = user_id,
                user_name = user_name
            )

            db.add(user)
            # await db.flush()
            # await db.refresh(user)

            if not skip_commit:            
                await db.commit()

            return True
        
        except Exception as e:
            await db.rollback()
            logger.error(f"유저 등록 중 예외 발생: {e}")
            return False
    

    @staticmethod
    async def update_block_status(db: AsyncSession, dto: UserBlockRegister) -> bool:
        try:
            stmt = select(User).where(User.user_id == dto.user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                return False
            
            user.is_blocked = dto.is_block   # True or Flase
            user.block_changed_at = datetime.now()
            user.notes = dto.notes

            await db.commit()
            return True
        
        except Exception as e:
            await db.rollback()
            logger.error(f"유저 차단 상태 변경 중 예외 발생: {e}")
            return False